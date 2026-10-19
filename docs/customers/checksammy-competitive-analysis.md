# CheckSammy — Competitive Analysis

> **Status: desk research, October 2026.** Based on CheckSammy's public website, a dated
> investment announcement and independent press. Company claims are marketing, not audited
> evidence. Nothing here has been verified through customer, hauler or competitor interviews.
> Re-verify before any external use.

## Why this document exists

CheckSammy ([checksammy.com](https://checksammy.com/)) looks very similar to WASTR. It did
not surface in roughly a year of validation. This note records what it actually offers, how
long it has existed, how much it overlaps with WASTR, why it may have been missed, and what
changes in our positioning. It complements
[investor-differentiation-theses.md](./investor-differentiation-theses.md).

**Bottom line.** CheckSammy does not invalidate the customer problem. It does invalidate
treating "independent haulers + digital coordination + traceability + sustainability data" as
a novel model. It is a core business-model comparator, not only a traceability comparator.

There is no evidence that CheckSammy copied WASTR. Its documented business predates our
validation period.

## What CheckSammy is (public record)

| Fact | Source |
|---|---|
| Founded 2018 | [About page](https://checksammy.com/about), [ESG Today](https://www.esgtoday.com/circularity-startup-checksammy-raises-45-million-to-scale-waste-diversion-sustainability-solutions/) |
| 24 Jan 2024: $45M strategic investment led by I Squared Capital, with Zero Infinity Partners and a TriplePoint Capital credit facility | [Investor-hosted press release](https://isquaredcapital.com/news/checksammy-secures-45m-strategic-investment-to-expand-waste-diversion-from-landfills/) |
| "Two-sided marketplace connecting independent waste haulers and service providers with enterprise customers"; on-demand, same-day bulk waste removal across North America | Same press release |
| Revenue "growing 40x since first commercializing in 2020" (company-reported) | Same press release |
| Planned sustainability software "Veridiant": diversion analytics, carbon inset/offset, materials marketplace, ESG-stack integration | Same press release |
| Current site: managed marketplace, owned "ZeroPoint" processing facilities, state-certified scales, GPS-confirmed pickups, photo documentation, automatic ESG documentation | [Homepage](https://checksammy.com/), [platform](https://checksammy.com/platform) |
| Markets commercial construction-debris recycling, with claimed 30–40 % cost reductions (marketing claim, unverified) | [Blog](https://checksammy.com/blog/commercial-construction-debris-recycling) |
| Claims a network of 25,000+ recycling and sustainability facilities | [About page](https://checksammy.com/about) |
| AI agents for voice/chat/email order handling | [Analytics page](https://checksammy.com/platform/analytics) |

Inconsistency to be aware of: the About page says Vancouver, Canada; the press release and
ESG Today describe a Dallas / Texas-based company. Do not state a headquarters in external
material without checking.

## Overlap with WASTR

| Dimension | CheckSammy | WASTR today | Overlap |
|---|---|---|---|
| Independent hauler network | Yes, two-sided marketplace | Multi-tenant collector app; no live paid hauler network | **Direct** |
| Ordering / matching / scheduling | Managed matching, scheduling, QC, payment | QR ordering + matching service | **Direct** |
| Evidence | GPS, photos, certified scales, chain of custody | Single photo + GPS per stage; richer evidence scaffolded, not shipped | **Strong** (they are ahead) |
| Sustainability reporting | Automatic audit-ready reports | ESG / NS 9431 reporting on roadmap | **Strong** (they are ahead) |
| Material recovery / reuse | Recovery, recommerce, materials marketplace | Roadmap only | Overlap |
| Construction waste | Explicit offering | Core segment | **Direct** |
| Owned processing infrastructure | Yes (ZeroPoint) | None; neutrality is a stated principle | Difference |
| Geography | North America | Oslo (and exploratory Brazil) | No geographic overlap |

Caveat: public pages show what they claim, not that every feature works as advertised, which
customers use it, or whether it is offered in Europe.

## Why it may have been missed (hypothesis)

The full competitor-search log was not available when this was written, so this is inference,
not a finding.

- [Product thesis](../strategy/product-thesis.md) names Sensorita, iSekk and
  phone/spreadsheet workflows as the comparison set and states that the ground is
  "uncontested by purpose-built software". That framing is Norway-centric.
- CheckSammy describes itself as bulk-junk removal, managed waste services, waste diversion
  and "Sustainability-as-a-Service". A search for Norwegian construction-waste booking would
  not return it.
- Earlier in this analysis cycle CheckSammy appeared in a comparison table as a traceability
  example. Its independent-hauler marketplace made it a business-model comparator, which was
  under-weighted at the time.

## What may still differentiate WASTR (all unproven)

1. **Software for haulers vs. a managed service for enterprises.** CheckSammy's proposition is
   "tell us what you need; we manage providers and guarantee the outcome". WASTR could instead
   let haulers run their own brand and keep their customers, optionally sharing capacity.
   *Not verified:* whether CheckSammy offers white-label tooling privately. This difference
   collapses if WASTR sells jobs under its own brand and subcontracts them.
2. **Neutrality toward receiving facilities.** CheckSammy emphasises owned infrastructure.
   Neutrality is only a moat if customers benefit (for example better destination choice).
3. **A local segment not served economically by a North American enterprise service:** small
   Norwegian haulers and renovation contractors. This can support a good business; it does not
   by itself establish venture-scale defensibility.

## Investor-facing implications

- Their funding **helps**: institutional investors have backed this category, so it is not "too
  small or boring".
- It **raises the bar**: they backed an operating business with reported revenue growth, not a
  roadmap.
- The honest pitch is not "nobody has built this". It is: "the model has precedent; here is
  the segment we serve better, the mechanism that makes us better, and the paid evidence".

## Claims to retire or qualify

| Existing claim | Action |
|---|---|
| "The ground is uncontested by purpose-built software" (product thesis) | Qualify: true at most for Norwegian SMB construction hauling, not for the model |
| "Neutrality is a moat" | Re-test; state what customer outcome neutrality improves |
| "Two-way optimisation is open territory" | Check literature and competitors before repeating |
| "Digital ordering", "traceability", "ESG documentation" as differentiators | Do not use; these are table stakes |

## Actions

1. Add CheckSammy to the competitor set and re-run a **model-based** competitor search (bulk
   waste, managed waste services, waste diversion, hauler marketplaces), not just
   Norway-specific queries.
2. Verify CheckSammy's commercial model from their partner/hauler materials and any public
   customer cases: who owns the customer, fees to haulers, minimum job size, facility choice,
   European presence.
3. Test one decisive hypothesis with Oslo haulers: would they pay for WASTR to manage their
   existing customers and optionally share capacity, even if WASTR brought no new leads?
4. Correct unsupported uniqueness claims in the product thesis and any pitch material.
5. Define paid-adoption and job-economics metrics before the pilot (see the pilot metrics in
   [investor-differentiation-theses.md](./investor-differentiation-theses.md)).
6. File this as a `[SIGNAL]` issue and link it from the product-thesis revisit.

## Open questions

- Does CheckSammy (or a similar operator) plan or already have European operations?
- Which other companies describe themselves with non-obvious terms (managed waste,
  diversion, Sustainability-as-a-Service) and operate hauler marketplaces?
- Is the first paying WASTR customer a hauler (coordination software) or a contractor
  (documentation)? The answer changes which competitors matter most.

## Sources

- CheckSammy homepage: https://checksammy.com/
- CheckSammy platform: https://checksammy.com/platform
- CheckSammy about: https://checksammy.com/about
- CheckSammy analytics / AI agents: https://checksammy.com/platform/analytics
- CheckSammy pricing: https://checksammy.com/pricing
- CheckSammy construction-debris article: https://checksammy.com/blog/commercial-construction-debris-recycling
- $45M announcement (24 Jan 2024): https://isquaredcapital.com/news/checksammy-secures-45m-strategic-investment-to-expand-waste-diversion-from-landfills/
- ESG Today coverage: https://www.esgtoday.com/circularity-startup-checksammy-raises-45-million-to-scale-waste-diversion-sustainability-solutions/
