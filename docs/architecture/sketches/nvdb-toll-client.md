# Sketch: NvdbTollClient + import job

> Reference sketch for [SPEC #45](https://github.com/wastr-as/wastr-learning-loop/issues/45) Phase 4 and [SPEC #46](https://github.com/wastr-as/wastr-learning-loop/issues/46) Phase 0/1. **Not compiled, not committed code** — a starting point for whoever picks up the implementation in `Wastr.Services.Fleet`. Aligned with [ADR-0012](../adr/0012-nvdb-toll-data-source.md).

## Layout

```
src/Wastr.Services.Fleet.Infrastructure/
├── Toll/
│   ├── Nvdb/
│   │   ├── NvdbTollClient.cs          // HTTP client, paging, retries
│   │   ├── NvdbResponse.cs            // DTOs for NVDB JSON
│   │   ├── NvdbToTollZoneMapper.cs    // NVDB → domain
│   │   └── NvdbConstants.cs           // object type id, attribute ids
│   └── Import/
│       ├── TollImportJob.cs           // orchestration (called by Function)
│       └── TariffFallback.cs          // CSV-backed override table
├── Resources/
│   └── toll-tariff-fallback.csv       // hand-curated overrides; checked in
src/Wastr.Services.Fleet.Function/
└── TollImportFunction.cs              // TimerTrigger weekly
```

## NvdbTollClient

```csharp
namespace Wastr.Services.Fleet.Infrastructure.Toll.Nvdb;

public sealed class NvdbTollClient
{
    private readonly HttpClient _http;
    private readonly ILogger<NvdbTollClient> _log;

    public NvdbTollClient(HttpClient http, ILogger<NvdbTollClient> log)
    {
        _http = http;
        _log = log;
    }

    /// <summary>
    /// Streams all bomstasjon objects within the given bbox, paging transparently.
    /// </summary>
    public async IAsyncEnumerable<NvdbBomstasjon> StreamAsync(
        BoundingBox bbox,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        string? start = null;

        do
        {
            var url = $"/vegobjekter/{NvdbConstants.BomstasjonTypeId}"
                    + $"?kartutsnitt={bbox.MinLon},{bbox.MinLat},{bbox.MaxLon},{bbox.MaxLat}"
                    + $"&srid=4326&inkluder=alle&antall=100"
                    + (start is null ? "" : $"&start={start}");

            using var resp = await _http.GetAsync(url, ct);
            resp.EnsureSuccessStatusCode();

            var page = await resp.Content.ReadFromJsonAsync<NvdbPage>(cancellationToken: ct)
                       ?? throw new InvalidOperationException("Empty NVDB page");

            foreach (var obj in page.Objekter)
                yield return obj;

            start = page.Metadata?.Neste?.Start;
        }
        while (start is not null && !ct.IsCancellationRequested);
    }
}
```

DI registration:

```csharp
// Program.cs in Wastr.Services.Fleet.Api
services.AddHttpClient<NvdbTollClient>(c =>
{
    c.BaseAddress = new Uri("https://nvdbapiles-v3.atlas.vegvesen.no");
    c.DefaultRequestHeaders.Add("X-Client", "wastr");
    c.DefaultRequestHeaders.Add(
        "Accept",
        "application/vnd.vegvesen.nvdb-v3-rev1+json");
})
.AddStandardResilienceHandler();   // .NET 9 built-in: retries, timeouts, circuit breaker
```

## DTOs (minimal, expand as needed)

```csharp
public sealed record NvdbPage(
    List<NvdbBomstasjon> Objekter,
    NvdbMetadata? Metadata);

public sealed record NvdbMetadata(NvdbNeste? Neste);
public sealed record NvdbNeste(string Start);

public sealed record NvdbBomstasjon(
    long Id,
    List<NvdbEgenskap> Egenskaper,
    NvdbGeometri Geometri,
    NvdbObjektMetadata Metadata);

public sealed record NvdbEgenskap(int Id, string Navn, JsonElement? Verdi);
public sealed record NvdbGeometri(string Wkt, int Srid);
public sealed record NvdbObjektMetadata(DateTime SistModifisert);

public static class NvdbConstants
{
    public const int BomstasjonTypeId = 45;

    // Confirm these attribute ids against /vegobjekttyper/45 at implementation time.
    public const int AttrNavn                       = 1078;
    public const int AttrOperator                   = 5530;
    public const int AttrTakstLitenBil              = 9410;
    public const int AttrTakstStorBil               = 9411;
    public const int AttrRushtidstilleggLitenBil    = 9412;
    public const int AttrRushtidstilleggStorBil     = 9413;
    public const int AttrMiljotakstLitenBil         = 9420;
    public const int AttrMiljotakstStorBil          = 9421;
}
```

## Mapper

```csharp
public static class NvdbToTollZoneMapper
{
    public static (TollZone Zone, IReadOnlyList<TollTariff> Tariffs) Map(NvdbBomstasjon n)
    {
        var navn       = GetString(n, NvdbConstants.AttrNavn) ?? $"Bomstasjon {n.Id}";
        var op         = GetString(n, NvdbConstants.AttrOperator) ?? "ukjent";

        var zone = new TollZone
        {
            ExternalId      = $"nvdb:45:{n.Id}",
            Name            = navn,
            Operator        = op,
            Country         = "NO",
            GeometryGeoJson = WktToGeoJson(n.Geometri.Wkt),
            ValidFrom       = DateOnly.FromDateTime(DateTime.UtcNow),
            LastVerifiedAt  = n.Metadata.SistModifisert,
        };

        var tariffs = new List<TollTariff>();

        AddIfPresent(n, NvdbConstants.AttrTakstLitenBil, m =>
            tariffs.Add(new TollTariff(zone.Id, TollVehicleClass.Class1, TimeOfDay.OffPeak, m)));

        AddIfPresent(n, NvdbConstants.AttrTakstStorBil, m =>
            tariffs.Add(new TollTariff(zone.Id, TollVehicleClass.Class2, TimeOfDay.OffPeak, m)));

        // Rush-hour = base + supplement, if the supplement attribute exists
        var baseSmall = GetDecimal(n, NvdbConstants.AttrTakstLitenBil);
        var rushSmall = GetDecimal(n, NvdbConstants.AttrRushtidstilleggLitenBil);
        if (baseSmall is not null && rushSmall is not null)
            tariffs.Add(new TollTariff(zone.Id, TollVehicleClass.Class1, TimeOfDay.RushHour,
                Money.Nok(baseSmall.Value + rushSmall.Value)));

        var baseBig = GetDecimal(n, NvdbConstants.AttrTakstStorBil);
        var rushBig = GetDecimal(n, NvdbConstants.AttrRushtidstilleggStorBil);
        if (baseBig is not null && rushBig is not null)
            tariffs.Add(new TollTariff(zone.Id, TollVehicleClass.Class2, TimeOfDay.RushHour,
                Money.Nok(baseBig.Value + rushBig.Value)));

        AddIfPresent(n, NvdbConstants.AttrMiljotakstLitenBil, m =>
            tariffs.Add(new TollTariff(zone.Id, TollVehicleClass.ZeroEmissionClass1, TimeOfDay.OffPeak, m)));

        AddIfPresent(n, NvdbConstants.AttrMiljotakstStorBil, m =>
            tariffs.Add(new TollTariff(zone.Id, TollVehicleClass.ZeroEmissionClass2, TimeOfDay.OffPeak, m)));

        return (zone, tariffs);
    }

    // GetString / GetDecimal / AddIfPresent / WktToGeoJson helpers omitted for brevity
}
```

## Import job (orchestration)

```csharp
public sealed class TollImportJob
{
    private readonly NvdbTollClient _nvdb;
    private readonly ITollZoneRepository _repo;
    private readonly TariffFallback _fallback;
    private readonly ILogger<TollImportJob> _log;

    public async Task<ImportResult> RunAsync(CancellationToken ct)
    {
        var changes = new ImportResult();

        // Norway split into a handful of bboxes to stay friendly with NVDB paging
        foreach (var bbox in NorwayTiles.All)
        {
            await foreach (var nvdb in _nvdb.StreamAsync(bbox, ct))
            {
                var (zone, tariffs) = NvdbToTollZoneMapper.Map(nvdb);
                var withFallback = _fallback.Apply(zone, tariffs);  // CSV overrides win

                var delta = await _repo.UpsertAsync(zone, withFallback, ct);
                changes.Record(delta);
            }
        }

        if (changes.TariffChangeRatio > 0.02)
            _log.LogWarning("NVDB import flipped {Ratio:P1} of tariffs — manual review recommended",
                changes.TariffChangeRatio);

        return changes;
    }
}
```

## Fallback CSV format

`Resources/toll-tariff-fallback.csv`:

```csv
external_id,vehicle_class,time_of_day,amount_nok,reason,reviewed_at
nvdb:45:12345,Class2,RushHour,68,operator-website-2026-05-20,2026-05-20
nvdb:45:67890,ZeroEmissionClass1,OffPeak,0,nvdb-missing-miljotakst,2026-05-20
```

Loaded into memory at startup. `TariffFallback.Apply()` overlays these on top of NVDB-derived tariffs (by `(external_id, vehicle_class, time_of_day)`).

## Function trigger

```csharp
public sealed class TollImportFunction
{
    private readonly TollImportJob _job;

    [Function("TollImport")]
    public async Task Run(
        [TimerTrigger("0 0 3 * * MON")] TimerInfo timer,  // 03:00 every Monday
        CancellationToken ct)
    {
        var result = await _job.RunAsync(ct);
        // App Insights custom event for dashboarding
    }
}
```

## Testing

- Unit: `NvdbToTollZoneMapper` against captured NVDB JSON fixtures (3 representative stations: a simple urban, an electric-discounted, one with missing rush-hour attribute).
- Integration: `TollImportJob` against a stub `NvdbTollClient` returning the same fixtures + a fallback CSV; assert the 3 reference Oslo routes from SPEC #46 Phase 0 produce expected totals within ±5%.
- Contract: a once-a-week canary test hits live NVDB for one known station and asserts the response shape hasn't changed.

## What's deliberately not here

- No HTTP-level retry loop hand-rolled — relying on `.AddStandardResilienceHandler()` in .NET 9.
- No caching of NVDB responses — import is weekly, freshness over speed.
- No incremental import (only full sweep) — NVDB doesn't expose a delta feed reliably; weekly full is fine at this volume (~few hundred objects nationally).
- No admin UI for the fallback table — edit the CSV in a PR. If the table grows past ~50 rows, revisit.
