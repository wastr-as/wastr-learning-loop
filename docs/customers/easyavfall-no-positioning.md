# Easyavfall.no - Analysis and Positioning

> **Status: hypothesis / desk research.** Based on Easyavfall's public website, terms and the first screen of its business-ordering flow. No customer interview or operational data. Internal dispatch software, integrations, capacity, margins and pain points are **unknown**. Public capabilities are not evidence of an unmet need or willingness to pay.

_Written: 2026-10-21 · Segment: transporter · Lane: b2b · Domain: customer_

## The signal

Unlike [Hente](hente-no-positioning.md), where Denis received a direct statement about existing logistics software, this is a **public-source assessment only**. Easyavfall presents itself as an established Greater-Oslo collection operator with digital ordering and a PROFF customer portal. Do not classify it as a phone/spreadsheet operator, or infer its internal dispatch system from its customer-facing website.

## What Easyavfall publicly offers

Sources checked 2026-10-21: [homepage and FAQ](https://www.easyavfall.no/), [services](https://www.easyavfall.no/tjenester), [terms](https://www.easyavfall.no/vilkar-og-betingelser), [ordering entry](https://bestilling.easyavfall.no/), [business-ordering first screen](https://bestilling.easyavfall.no/bedrift). Terms state last updated 2026-01-01. Marketing statements below are company claims, not audited performance.

| Area | Public evidence | Implication for WASTR |
|---|---|---|
| Geography and customers | Greater Oslo and surrounding municipalities; private customers, professionals and housing-association clean-ups | Strong overlap with our initial geography and contractor segment |
| Bags and containers | Small, medium and large bags; services page advertises containers from 5 to 35 m3 | A broader operational range than a narrow bag-collection pilot needs |
| Bag compatibility | Collects bags of all colours; FAQ qualifies this as bags approved for crane lifting | A pilot need not require switching to WASTR-branded bags; this is not the same as multi-operator neutrality |
| Digital ordering | Public entry offers PRIVAT / PROFF / DUGNAD. PROFF opens an address-first flow with order/time stages and company lookup | Another generic online-ordering front end is not a compelling proposition |
| PROFF portal | Advertises ordering in under 30 seconds, invoice copies and order status; services page explicitly lists a digital customer portal | Do not pitch basic order visibility or invoice access as missing. Speed and authenticated features were not tested |
| Business relationship | Tailored agreements, named contact, invoicing arrangement, collection priority and free initial site assessment | Easyavfall already sells contractor convenience and project support, not just truck capacity |
| Documentation | FAQ says all collected waste is weighed at reception and waste reports can be supplied; terms section 15 offers type/quantity documentation on request and recurring reporting by agreement | Do not assume a reporting gap or claim verified compliance. Explore project attribution or multi-operator consolidation only if customers identify a problem |
| Collection constraints | Large/small crane vehicles; terms require disclosure of access restrictions, limit standard bag placement to 10 m from a suitable truck position, and allow extra charges for special equipment or sorting errors | Structured information before dispatch is a plausible opportunity, not a demonstrated defect in their current process |
| Materials and waste | Homepage offers material delivery/lifting while a crane is on site; services include crane transport and delivery of reusable materials to reuse actors on request | "Materials out, waste back" is not novel as a service concept. Automated, multi-operator coordination would need separate proof |
| Sustainability | Advertises approved receiving facilities, sorting guidance and training for tradespeople/project managers | Generic "simpler, greener waste handling" overlaps its existing pitch; fleet emissions and fuel mix remain unknown |

**Service-promise caution:** the FAQ says collection is normally the next day, depending on location/workload; terms section 9 says normally **1-4 working days in Oslo unless otherwise agreed**. Do not resell next-day collection as guaranteed.

**Research boundary:** inspected the public PROFF entry screen without entering customer details or submitting an order. Later checkout, photo capture, logged-in portal, API availability and actual operational performance were not verified. Absence from the inspected screen is not evidence that a capability is missing.

## Where WASTR stands

The [product thesis](../strategy/product-thesis.md) and [pilot learnings](pilot-learnings.md) support source-level capture as our starting point: QR/mobile ordering, location, photos, waste selection and order/evidence workflows. They do not establish repeatable customer acquisition, positive Oslo unit economics or measured route savings. Advanced two-way optimisation and full reporting remain roadmap in the documented thesis.

Position WASTR as a **small commercial experiment around a confirmed gap**, not a replacement for Easyavfall's portal, dispatch or customer relationships.

## Connection points (ranked)

1. **New, qualified contractor demand -> Easyavfall fulfils (best first angle).** Bring jobs from contractor or property-management relationships Easyavfall does not already serve. Easyavfall chooses acceptable fractions, locations, timing and pricing. Incremental contribution matters, not gross lead count. This fails if WASTR merely redirects their existing customers or cannot acquire new ones economically.
2. **Better-prepared jobs -> fewer calls and avoidable exceptions (best operational angle).** Test a job brief with site photos, exact pickup point, bag count/type, fraction, access restrictions, contact and project reference. Ask what their portal already captures first. Easyavfall reviews feasibility; photos are not a substitute for a site assessment, and WASTR must not promise automated safety or hazardous-waste assessment.
3. **Contractor/project coordination across operators (conditional, medium term).** A builder using several providers may value one source record and consistent project references, with Easyavfall retaining its own system. The value would be cross-provider coordination, not a replacement waste report. Interview builders as well as Easyavfall; treat this as co-design, not a shipped integration.
4. **Compatible materials/waste jobs -> capacity experiment (later).** Their existing material-handling services make them a relevant discovery partner for two-way logistics. Start with selected, manually reviewed combinations and record marginal time, distance and cost. Do not infer spare capacity, feasible backhauls or optimisation demand from the service menu.

**Do not lead with:** "you need an app", faster online ordering, invoice visibility, generic waste reports, AI classification, guaranteed route savings, or the claim that nobody combines material delivery with waste collection.

## How this differs from Hente

| Question | Hente evidence | Easyavfall evidence | Positioning consequence |
|---|---|---|---|
| Existing logistics software? | Reported to Denis; vendor and coverage unknown | Internal system unknown; public ordering and advertised customer portal | Both weaken the generic digitisation pitch, but only Hente has the reported internal-software statement |
| Contractor workflow? | Business collections and documentation advertised | Explicit PROFF portal, invoice/status access, named contact and tailored agreements | A duplicate contractor portal is particularly hard to justify to Easyavfall |
| Sustainability angle? | Electric transport advertised | Sorting, approved reception and reuse services advertised; fleet unknown | Do not transfer Hente's fleet claims to Easyavfall |
| Two-way-logistics connection? | Not established in the Hente assessment | Material delivery/lifting and reuse transport explicitly advertised | Useful operational research partner candidate, but a challenge to novelty claims about the basic service concept |

Neither assessment establishes willingness to pay for WASTR. Both suggest testing a fulfilment-partner relationship before pitching a software subscription.

## Relationship and commercial boundaries

Start with a **referral model**: Easyavfall accepts the job, contracts with and invoices the customer, and keeps dispatch in its existing tools. WASTR prepares the lead and coordinates the initial handoff.

- Agree what counts as a WASTR-originated customer and how existing accounts, repeat orders and attribution are handled.
- Agree any referral fee, customer-data use, support ownership, cancellations, extra charges and dispute handling before the first job.
- Use the handoff Easyavfall prefers; do not require duplicate entry in a second operator app. Measure WASTR's manual coordination rather than hiding it.
- Keep an Easyavfall-owned channel distinct from a WASTR-originated channel. No exclusivity or preferential marketplace ranking is needed for a bounded pilot.
- An API integration, reseller arrangement or white-label product is a later decision, not a prerequisite.

## Discovery questions (before any demo)

1. Which additional contractor jobs would you actually want, and in which areas/time windows?
2. What does the PROFF portal already capture, and what still requires calls, photos by message or re-entry?
3. Which access, sorting, bag-selection or project-reference issues cause the most extra work? Can we review anonymised recent examples?
4. Would genuinely new, pre-qualified jobs be useful if your team kept its current tools and customer relationship?
5. What is the lowest-effort handoff, and which commercial/data boundaries would you require?
6. How often do you already combine material delivery with waste collection, and what prevents more of it?

Ask about dispatch software, vendor and imports/APIs after establishing an economic or operational problem.

## Proposed pilot (test parameters, not promises)

Four weeks, one agreed Greater-Oslo area, selected **non-hazardous contractor bag jobs**, target **20-30 genuinely new completed jobs**, subject to confirmed capacity. Exclude containers, special lifts and material/waste combinations initially so the result is interpretable.

- Easyavfall defines acceptance rules, price, service window and capacity; confirms each job and controls dispatch.
- WASTR acquires customers, captures agreed information and absorbs initial coordination work.
- Before starting, agree minimum contribution per job and maximum added admin time. Record baseline handling time/exceptions on comparable jobs where available; do not claim improvement without a comparison.
- **Measure:** qualified leads -> accepted -> completed incremental jobs; Easyavfall contribution after incremental transport, handling, disposal, admin and any WASTR fee; WASTR acquisition/coordination cost and fee revenue; admin minutes; clarification calls, failed visits, cancellations and sorting/access exceptions.
- **Continue only if:** completed jobs meet the agreed contribution/admin thresholds and both sides want a repeat. Volume alone is not success; 20-30 jobs is an early feasibility test, not proof of route savings.
- **Stop or redesign if:** no genuinely new demand, capacity is unavailable, duplicate admin outweighs value, or acquisition cost has no credible path to sustainable economics.
- Keep any homeowner test separate as `lane: b2c`; do not count it as the B2B pilot outcome.

## Suggested opening

> We see that you already have digital ordering, a PROFF portal and waste reporting. We are not proposing to replace those. We would like to test whether we can bring you new contractor jobs in an agreed area, prepared with the information your team needs, while you keep customer contracting and dispatch. Would a small trial be worth discussing if we measure margin and extra administration, not just order volume?

## Segmentation takeaway and open questions

Easyavfall is a **digitally enabled fulfilment-partner candidate**, not a validated software buyer. Together with Hente, it supports more careful segmentation, not a market-wide conclusion or a product pivot.

Unknown: internal systems and integrations; spare capacity; acquisition appetite; current job-information quality; frequency/cost of exceptions; customer demand for cross-provider coordination; willingness to share data or pay a referral fee.

The defensible WASTR hypothesis is **profitable new demand plus better source information and, eventually, neutral coordination across operators**. None of these benefits is proven for Easyavfall.
