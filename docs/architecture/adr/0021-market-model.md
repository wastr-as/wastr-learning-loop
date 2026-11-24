# ADR-0021: Market Model — Market Key from the Pickup Address, Party Identifiers, Versioned Codes, Profiles in the Repo, One Shared Package

- **Status:** Proposed
- **Date:** 2026-11-24
- **Deciders:** Siarhei (CTO)
- **Related:** SPEC #119 (this is its Phase 0), signal #114 (Brazil), #115, #118 (receiving facilities), #111 (DiBK report), #51 (conversion factors as versioned files), #88 §13.1 (overlay principle), L-011 (localisation tax is identity and money), ADR-0007 (multi-tenancy), ADR-0015 (reporting)

## Context

Regulated waste documents differ per market: how parties are identified, which waste
codes apply, which thresholds and deadlines count. The Brazil signal (#114) is the
second market, and the code is shaped by Norway in many places (checked on `main`,
2026-11-24):

- `enum WasteTypeCode` (22 values) is **copied in 5 services** (Product, Ordering,
  Matching, Notification, Collector). Adding a fraction took synchronised PRs. It is
  linked to no official code list (NS 9431, EWC/EAL, IBAMA LBR, NBR 10004).
- Only Product knows the market (`enum Country { Norway, Brazil }`). Company,
  Project, Order have none.
- `Company.OrgNr` is a Norwegian organisation number with no scheme or validation.
  `Customer.NationalIdentityNumber` is a free string.
- TEK17 thresholds (300/100 m², 10 t) and the 60 % sorting minimum are constants in
  `WasteReportService`. No record says which classification version it used.
- `Money`, `Currency` and `MeasurementUnit` are copied across services, and weights
  are plain `double` kg, so mass and volume can be mixed by accident.

## Decision

1. **Market key.** `CountryCode` (ISO 3166-1 alpha-2) plus an optional `Subdivision`
   (ISO 3166-2, e.g. `NO-03`, `BR-RJ`), kept as **validated strings, not enums**.
   The **market of an order comes from its pickup address**, not from the company: a
   Norwegian company can work in Sweden. A company has a home country (default for
   its users and sites). A receiving facility has its own country (#118).
2. **Overlay principle.** One global WASTR fraction taxonomy. Country, subdivision,
   municipality, receiver and contract overlays add to it and never overwrite global
   ids (encyclopaedia #88 §13.1).
3. **Party identifiers.** `PartyIdentifier { Scheme, Value }`, a list per party.
   Schemes: `NO_ORGNR`, `BR_CNPJ`, `BR_CPF`, `EU_VAT`, and more later. One validator
   per scheme (check digits). Personal identifiers (CPF, fødselsnummer) are stored
   only where a document legally requires them, encrypted, with a retention rule.
4. **Codes are strings.** The fraction code travels as a string between services
   and unknown values are tolerated (shown raw, never a crash). Product owns the
   catalogue and a versioned `ClassificationMapping { FractionCode, Scheme,
   SchemeVersion, Code, Class?, ValidFrom, ValidTo }`. Every regulated record
   (report, manifest, certificate) **snapshots scheme, version and code**; a new
   catalogue version never rewrites old records.
5. **Quantity.** `Quantity { Value, Unit }` for anything measured or declared.
   Totals are per unit. Mass and volume are never added; a conversion records the
   density, its source and a version.
6. **Regulatory profiles are versioned JSON in the repository**, changed by pull
   request (for example `NO/tek17-waste-v1`, `BR-RJ/mtr-v1`). Each has `version`,
   `validFrom`, `sources`, `validatedBy`, `validatedOn`. An unvalidated profile is
   labelled as such, never hidden. This is the same approach as the conversion
   factor files in #51. Not a database.
7. **Shared code in one NuGet package.** `Wastr.Shared.Markets`, published to
   GitHub Packages. It holds country/subdivision validation, `PartyIdentifier`
   and its validators, `Quantity`, `Money`/`Currency`, and the profile loader (the
   profile files ship as embedded resources, so a profile change is a PR plus a
   package version).

### What this does not decide
- Which Brazilian catalogue the MTR-RJ form requires (answer comes from #115).
- Whether WASTR holds the licensed NS 9431 code list (EWC/EAL is public).
- Who validates a market's profile (a qualified person per market; cost is budgeted
  per market, L-011).
- Templates per market and data-protection profiles (Phase 5 of #119).

### Rollout rules
- Every cross-service contract change is **additive**: accept old and new shapes for
  a period. Deploy order: Product, User, Fleet, Ordering, BFFs, apps.
- Every SQL change updates **both** the service repo's `db/` and
  `global-infra/db/<service>/`. `DestinationType` was missing from the deployed
  script (global-infra#20); this must not repeat.
- `ReceivingFacility.RegistryScheme/RegistryNumber` (#118) use the same scheme names
  and validators; they move into the package as its first consumer and stay valid.

## Alternatives Considered

1. **Enums per market.** Rejected: every new market is a release in every service.
2. **A generic rules engine.** Rejected: premature for two markets, and a
   configuration mistake becomes a legal mistake. Versioned data plus validators
   gives what is needed.
3. **Profiles in a database edited in the Admin app.** Rejected for now: a pull
   request gives review and reproducibility, and thresholds change rarely. See the
   revisit trigger.
4. **Per-service or generated copies instead of a shared package.** Rejected: the
   copies already drifted (waste-type enum, `Money`, `Currency`).
5. **Market from the company's country.** Rejected: wrong for cross-border work and
   for a hauler registered in one country serving another.

## Consequences

### Positive
- A new market is data plus validators, not a release in five repos.
- Every regulated record can say which catalogue and rule version it used.
- Norway benefits without any Brazil work: no five-repo enum sync, a validated
  organisation number, official codes on the #111 report, TEK17 values as reviewed
  data.

### Negative
- Strings move errors from compile time to runtime. Mitigation: validators in the
  package and contract tests.
- A new package to publish and version. Docker builds and CI need credentials for the
  GitHub Packages feed, and local development needs a token.
- JavaScript apps cannot use the package, so form validators stay duplicated in JS
  (server-side validation remains the authority).
- Each market profile needs a qualified reviewer.
- Over-engineering risk if the second market never arrives. Phases 1-2 of #119 are
  worth it for Norway alone; Phases 3-5 for Brazil wait for #115.

## Revisit Trigger

- The second market is not confirmed on #115: build only Phases 1-2 of #119.
- Non-developers need to change profiles often, or there are more than three
  markets: move profiles to a database with an approval step.
- Feed credentials in CI and Docker cost more than the drift they prevent: switch to
  generated copies.

## Definition of Done (Phase 0 of #119)

- [x] Decision recorded (this file) and mirrored as issue #122.
- [ ] Confirmed (Status set to Accepted).
- [ ] `Wastr.Shared.Markets` repository and feed created (start of Phase 1).
