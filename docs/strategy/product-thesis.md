# Product Thesis

> **Why this problem, why us, why now.**

## The Problem

Construction & demolition waste (CDW) logistics in Norway is fragmented, manual
and undocumented:

- ~70% of SMB transporters coordinate jobs by phone, paper, and spreadsheet.
- Empty-running (tomkjøring) routinely exceeds 30% of truck-km — trucks return
  empty after deliveries instead of carrying waste back.
- Construction sites lose hundreds of admin hours per project to waste
  coordination and weigh-slip chasing.
- Builders cannot produce structured NS 9431 / ESG reports without after-the-fact
  reconstruction.

## Why It Matters Now

- **Regulation:** EU 70% CDW recycling target by 2030; Norwegian implementation
  is tightening NS 9431 documentation requirements.
- **Market:** ~70% of Norwegian CDW operators still phone + spreadsheet; the
  ground is uncontested by purpose-built software.
- **Technology:** AI cost curve makes route optimization and image-based waste
  classification economically viable at SMB scale (margins of NOK 200–500k/yr
  per truck, not Fortune-500 budgets).

## The Insight

The bottleneck is not weighing, billing or compliance — it is **coordination at
the source**. If we capture {photo + geolocation + waste fraction} at the moment
of the job request (zero-app, QR-initiated), the rest of the chain — matching,
routing, documentation, ESG reporting — becomes a database problem rather than
a phone-tree problem.

This inverts the usual "digitize the back office first" approach.

## The Solution (one paragraph)

Wastr is a neutral, vendor-agnostic data infrastructure for CDW logistics:
builders place pickup orders via a QR-initiated web flow (no app install); a
matching service routes orders to nearby SMB transporters; drivers execute
pickups via a mobile-friendly app with evidence capture; the platform produces
NS 9431-compliant documentation automatically. Two-way logistics (outgoing
materials + return waste) is the technical core IP.

## What Is Actually Shipped Today (MVP)

- QR-initiated customer ordering with geolocation capture.
- Multi-tenant Collector app with company / personal order views, drag-and-drop
  route builder, real-time updates via SignalR.
- Driver app with pickup / delivery flows and **single-photo evidence capture**
  (one photo + GPS + optional notes per stage). Richer evidence types
  (multi-photo, weight-slip OCR, signature, structured documents) are scaffolded
  in the domain model but not yet exposed in the UI.
- Order lifecycle (Pending → Accepted → InProgress → Completed) with immutable
  audit trail.
- Service-to-service Azure AD identity, JIT user provisioning, company isolation.
- Event-driven notifications (email/SMS) via Azure Service Bus + Functions.

## On the Roadmap (Not Yet Shipped)

- Two-way routing engine PoC (research project #5).
- Computer-vision waste classification (research projects #6–8).
- Richer evidence capture — multi-photo, weight-slip OCR, signature, structured
  documents (domain model ready; UI work pending).
- Full ESG / NS 9431 reporting dashboard.
- Neutral multi-actor API standard (research project #9).
- **Smart route planner** — auto-assignment of orders to drivers based on
  capacity / waste-type / schedule / geography, pre-accept simulation at the
  marketplace ("where does this fit in your existing routes?"), pluggable
  optimization strategy (time / distance / toll-aware / CO₂), and Norwegian
  bomstasjon cost integration. Directional bet anchoring near-term routing
  choices — see [#44](https://github.com/wastr-as/wastr-learning-loop/issues/44).

## Why Us

- **Denis Pozhinsky (CEO)** — construction & project management background,
  direct line to Oslo builders and transporters.
- **Siarhei Karabitski (CTO)** — 15+ years building production .NET systems
  at Telenor, Rystad Energy, Statens vegvesen.
- **Philip Hansteen (advisor)** — ex-Equinor Techstars; ESG and partnerships.
- **Research network** — NTNU, SINTEF Digital & AI, TØI, BI, Simula, OsloMet
  AI Lab, Lindum.

## What We Believe That Others Don't

1. **The wedge is the order, not the weight.** Sensor-led and weigh-slip-led
   approaches arrive too late in the chain to fix coordination.
2. **Neutrality is a moat.** A vendor-agnostic platform can connect independent
   transporters across company silos in a way no transporter-owned tool can.
3. **Two-way optimization is the real ML problem.** Single-leg VRP is solved;
   bidirectional reverse-logistics with dynamic demand is open territory.
4. **QR + no-app onboarding beats sensor + hardware.** Zero-friction wins at
   SMB scale.

## The Emission-Reduction Thesis (Research-Grounded)

WASTR's sustainability story rests on **three independent, stacking levers** — each
cuts emissions on a different axis, each is backed by peer-reviewed waste-logistics
research. Grounding these in literature (rather than round-number projections) is what
makes the ESG / Innovasjon Norge / SmartOslo narrative defensible. Comparable studies
and emission factors are filed as signal
[#76](https://github.com/wastr-as/wastr-learning-loop/issues/76).

1. **Optimize routing for fuel/energy, with gradient + load as factors on top of
   distance.** Distance stays the primary driver of fuel; the engine adds **gradient and
   load** as weighting factors so it minimizes energy rather than raw km. Tavares et al.
   2009 (Cape Verde, 3D GIS) found that on hilly terrain a slightly longer, flatter route
   can beat a shorter, steeper one — the fuel objective (distance × gradient × load)
   diverges from pure shortest-path. Directly relevant to Oslo topography (Holmenkollen,
   Ekeberg, Grefsen) and a differentiator vs. naive shortest-path competitors. Feeds the
   Two-Way Routing Engine PoC (R&D #5) and the smart route planner
   ([#44](https://github.com/wastr-as/wastr-learning-loop/issues/44)) — the cost function
   should weight distance by gradient and load, not replace it.
2. **Consolidate loads + right-size vehicles (per-ton lever).** Per-ton collection
   intensity swings ~7× (≈5→35 kg CO₂-eq/ton), driven mostly by truck volume, engine
   power and fill — fuller, right-sized vehicles are more efficient *before* any route
   change. This is a distinct lever from empty-running avoidance and validates the
   consolidated / bidirectional-load thesis (Demir & Maçin, Çorlu case study).
3. **Driver behaviour is a cheap, high-impact lever.** Eco-driving alone — no fleet or
   route change — cut İETT Istanbul's diesel by **3.58M L in one year** (~15–20% class
   savings). No competitor (Sensorita, iSekk, phone/spreadsheet) addresses this; it's a
   low-cost driver-app feature (eco-nudges, idling alerts) with a defensible ESG story.

**Supporting evidence.** Fuel type matters (natural gas ≈ 1.90 vs. diesel 2.25 kg
CO₂-eq/km, López et al. 2009) — surface per-transporter fuel mix in ESG reports without
favouring anyone, consistent with the neutrality moat. WASTR's headline "160 t CO₂ on
180,000 km" implies ~0.89 kg CO₂/km, **conservative** vs. a loaded diesel packer
(2.25 kg/km), so the figure is more likely under- than over-stated.

**Evidence gap = moat.** Every quantified study above is *municipal household waste*
(fixed-route packer trucks). There is essentially no published per-km/per-ton dataset for
ad-hoc **CDW skip/bag** logistics — exactly the whitespace R&D projects #1–#5 target, and
the core argument for the FoU partnerships (NTNU / SINTEF / TØI). The direction
(optimization → 10–25%+ savings) transfers; absolute CDW factors still need our own
telemetry (SPEC #48) to confirm.
