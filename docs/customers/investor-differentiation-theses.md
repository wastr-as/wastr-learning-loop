# Investor Differentiation Theses

> **Status: hypotheses, not validated results.** Nothing below is a measured WASTR outcome.
> Each thesis names the evidence needed to confirm or kill it. Re-read after the first Oslo
> transporter pilot and update with `[SIGNAL]` / `[EXPERIMENT]` links.
>
> Last researched: October 2026. Competitor claims come from company websites and press
> releases (marketing, not independent evaluation). Re-verify before external use.

## Why this document exists

The Loggit / Omlo comparison showed that "digital ordering + tracking + dashboard" is
**not** a sufficient differentiator. Omlo already sells an integrated flow of ordering,
logistics, registration, sorting and reporting to municipalities, with a pilot-first model
([Omlo – For kommuner og IKS](https://omlo.no/for-kommuner)). Adjacent construction-waste
players cover more of the same ground:

| Player | What the public source says | Implication for WASTR |
|---|---|---|
| **Wastebox** (Veolia / Saubermacher) | App-based skip ordering; orders go directly to available, favourably located drivers; web portal with orders, costs, delivery notes in real time (2018 launch) — [Saubermacher press release](https://saubermacher.com/en/press/wastebox-biz-goes-germany/) | Digital ordering + dispatch is established |
| **Schüttflix** | Platform connecting construction companies, material suppliers, waste-management companies and carriers — [Schüttflix](https://www.schuettflix.com/global/en/) | "Materials out, waste back" is not uncontested |
| **CheckSammy** (US) | "Full visibility and verified outcomes" from pickup to final disposition — [CheckSammy platform](https://checksammy.com/platform) | Traceability is valuable but not unique |
| **Excess Materials Exchange** | B2B surplus/reuse marketplace with buyer matching and ESG impact reporting; priced packages from €5,500 — [EME](https://www.excess.company/) | Reuse matching exists; priced pilot packages are a useful WTP benchmark |
| **Loopfront** (NO) | Early surveying of materials, internal reuse, external marketplace (Norwegian listings) — [Loopfront](https://www.loopfront.com/product) | Reuse cataloguing in Norway is already served |

**Do not claim** that routing software only handles fixed routes, or that digital ordering,
traceability or reuse matching are novel. The defensible claim is a **specific segment, a
specific operating model, and measured economics**.

## Core thesis

> **WASTR makes small, scattered pickups profitable by coordinating demand, independent
> haulers and receiving facilities — not merely by digitising the booking.**

Omlo validates that coordinated, traceable collection has buyers. It does not prove WASTR's
own economics. The investor "WOW" is evidence that previously unattractive jobs become
commercially worthwhile.

---

## Thesis 1 — Shared pickup network; flexibility earns a discount *(strongest core thesis)*

**Idea.** Offer customers three choices: *priority* (narrow window), *flexible* (wider window,
lower price), *scheduled local round* (join an already planned collection). Behind it, WASTR
combines compatible orders across **participating** haulers. Haulers stay white-label and
opt in which jobs or spare capacity to share.

**Demo.** A map of small jobs that are expensive to serve separately → add a customer willing
to wait a day, another hauler's spare capacity and an open receiving facility → WASTR outputs a
feasible route with lower cost per completed pickup and acceptable hauler earnings.

**Why it could matter.** A *local*, compatibility-dependent network effect: more compatible
orders improve density for existing participants. Constrained by vehicle type, lifting
equipment, material restrictions, time windows and geography — not "every user improves
everything".

**Revenue hypothesis.** Fee on successfully coordinated work, or a paid coordination tier.
Avoid a hidden marketplace commission on haulers' existing customers if the promise is
"keep your customers".

**Main risk.** Haulers resist sharing work or capacity. Start with opt-in overflow and
spare-capacity offers; never expose customer lists or competitors' prices.

**Novelty.** Shared dispatch is not new (see Wastebox, Schüttflix). The bet is
**white-label participation + customer flexibility + cross-hauler economics for small
irregular loads**.

## Thesis 2 — Margin assistant before the waste is mixed *(best companion to Thesis 1)*

**Idea.** Intervene before disposal decisions are locked in. Compare
**collection + handling + treatment fees + expected surcharges − confirmed material revenue**,
not just distance or the cheapest gate fee. A cheaper facility may be farther away, queue, or
reject the load.

**Demo.** A contractor starts a mixed-waste booking; WASTR offers two *deliverable*
alternatives with what must be separated, whether another bag/pickup is needed, which receiver
has agreed to accept it, and the quoted total.

**Data moat.** Repeated real outcomes: declared material → actual accepted material → weight →
handling time → treatment charge → final margin. This improves quoting, exception prediction
and destination choice. The advantage is the outcome data, not an image classifier on the
booking form.

**Revenue hypothesis.** Paid quoting/operations functionality; gain-sharing only where savings
can genuinely be established.

**Main risk.** Missing or unreliable receiving-facility data. Start with a few contracted
facilities and explicit acceptance rules. Photos can assist triage; they cannot certify
composition, weight or absence of hazardous substances.

**Novelty.** EME already markets profitable reuse options. WASTR's narrower opening is
**small-load, executable collection decisions that include real transport and treatment costs**.

## Thesis 3 — Sold before it becomes waste: demand-led reuse with delivery included *(best demo, build later)*

**Idea.** Capture **demand first** ("this contractor needs this quantity/spec next week below
this delivered price") and match it to upcoming surplus before it enters a mixed container.
Result: a fulfilled reuse order, not another listing.

**Demo.** A project lists suitable surplus → confirmed buyer, specification, collection
deadline, delivered price, seller proceeds or avoided disposal cost, confirmed transport plan.

**Strategy.** Competitors exist (Loopfront, EME). **Partner with marketplaces; supply the
difficult fulfilment layer** — small-load collection, scheduling, delivery.

**Revenue hypothesis.** Fulfilment fee or transparent transaction fee.

**Main risk.** Inspection, dismantling, storage and delivery can consume the apparent value.
Start with one low-complexity category (e.g. identifiable unopened surplus products), not
structural components needing qualification.

## Thesis 4 — Documentation that closes the job *(strongest near-term reason to pay)*

**Idea.** A pickup is "fully documented" only when evidence reconciles:
**booking → pickup → receiver confirmation → measured quantity → receipt → project allocation.**
Missing evidence surfaces immediately; project reports are generated from the underlying
records. Stretch goal: pickup, receipt and invoice reconcile automatically and only
exceptions go to a person.

**Regulatory grounding (TEK17, Norway).**
- Final-report documentation must be supported by weigh slips, receipts or electronic
  confirmations with date, sender/receiver, waste/reuse type and quantity —
  [DiBK § 9-9](https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-9).
- Waste plans apply to defined projects (e.g. new build > 300 m² BRA, rehab > 100 m² BRA,
  demolition > 100 m² BRA, or > 10 tonnes C&D waste) — **not every small renovation** —
  [DiBK § 9-6](https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-6).
- The **70 % rule is sorting into clean waste types by weight**, not proof that 70 % was
  recycled. Combustible "sorted" material does not count as a clean fraction —
  [DiBK § 9-8](https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-8).

**Keep three states separate:** *collected* → *received* → *treatment verified*. A QR scan and a
photo do not establish final recycling.

**Revenue hypothesis.** Project or portfolio subscription for contractors with recurring
projects.

---

## Recommended build order

| Stage | Build | What it proves |
|---|---|---|
| 1 | Reliable cost, acceptance and evidence capture | WASTR understands each job's real economics and outcome |
| 2 | Flexible collection windows + opt-in shared dispatch | Coordination lowers cost and improves hauler earnings |
| 3 | Priced separation / destination recommendations | WASTR changes decisions before cost is incurred |
| 4 | Reuse fulfilment via partners | The same network serves higher-value material movements |

Prove **one dense local operation first**. The Oslo big-bag / Rio cooking-oil multi-stream story
stays a long-term expansion thesis; different streams need different equipment, rules and
receivers.

## Investor proof to design the pilot around

Compare ordinary dispatch with WASTR-coordinated work in one compact area with a few haulers,
adjusting for job mix. Set targets **before** the pilot. Measure:

- Contribution margin per completed pickup
- Kilometres and driver time per comparable job
- Customer uptake of flexible windows
- On-time completion and rejected-load rate
- Manual coordination minutes per job
- Evidence completeness (collected / received / verified)
- Repeat usage **and willingness to pay**

Do **not** present the projected 25 % empty-running reduction as an achieved result; it remains
an internal projection until telemetry actuals exist (see ADR-0015 and the empty-run North
Star).

## Suggested pitch line

> "WASTR is building a shared pickup network for independent haulers. Customers get better
> prices for flexible collection, haulers get better-filled routes without giving up their
> brand, and contractors get documented outcomes. We start with small construction-waste
> pickups in Oslo."

Ambition line: *"We want to make small material flows economical to collect, recover and reuse."*

## Open questions

- Will independent haulers opt in to sharing spare capacity, and under what incentive?
- What share of customers accept a wider window for a discount, and at what discount?
- Which receiving facilities will contractually publish acceptance rules and fees?
- Is the first paying buyer the contractor (documentation) or the hauler (coordination)?
- Revenue model: this document assumes a mix of subscription, coordination fee and
  fulfilment fee; the current platform brief assumes monthly licence + per-vehicle /
  per-project licence. Decide which is tested first.

## Sources

- Omlo – For kommuner og IKS: https://omlo.no/for-kommuner
- Loggit – Tjenester: https://www.loggit.eco/tjenester
- Wastebox Germany (Saubermacher press release): https://saubermacher.com/en/press/wastebox-biz-goes-germany/
- Schüttflix: https://www.schuettflix.com/global/en/
- CheckSammy platform: https://checksammy.com/platform
- Excess Materials Exchange: https://www.excess.company/
- Loopfront: https://www.loopfront.com/product
- DiBK TEK17 § 9-6 (waste plan): https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-6
- DiBK TEK17 § 9-8 (sorting requirement): https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-8
- DiBK TEK17 § 9-9 (final report documentation): https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-9
