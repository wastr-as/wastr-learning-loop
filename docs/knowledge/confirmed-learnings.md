# Confirmed Learnings

> **Promoted from `learning: confirmed` issues.**
> A learning lands here only after it has been independently confirmed (≥2 signals or 1 experiment).
> These are treated as facts until a future signal forces a revisit.

## Format

Each entry:
- **Learning:** one sentence
- **Confirmed by:** issues #_, #_
- **Implications:** what this means for product / strategy
- **Date promoted:** YYYY-MM-DD

---

## L-001 — Split async transports by purpose: queue for work, topic for fan-out

- **Learning:** Two distinct event needs deserve two distinct transports.
  Azure **Service Bus** queues handle ordered, exactly-once work (an order
  posted to the marketplace must be picked up by exactly one matching worker).
  Azure **Event Grid** topics handle broadcast fan-out (an `OrderAccepted`
  event must light up N independent notification channels — email today; SMS,
  WhatsApp, push tomorrow).
- **Confirmed by:** ADR-0006; marketplace processing runs cleanly through
  Service Bus; Notification Service consumes Event Grid and currently
  dispatches email only, with channel-specific handlers ready to add without
  producer changes.
- **Implications:**
  - Producers stay dumb. The Ordering Service publishes one event; subscribers
    decide what to do — adding a WhatsApp channel does not touch Ordering.
  - Pick the transport by question: *"must exactly one worker do this?"* →
    Service Bus. *"may zero-to-many subscribers react?"* → Event Grid.
  - Notification channels are a strategy pattern keyed on the user's
    `NotificationChannels` preference; new channels are pure additions.
  - Resist temptation to use SignalR (L-002) for server-to-server work — that
    channel is for client push, not workflow orchestration.
- **Date promoted:** 2026-05-26

## L-002 — Both sides of a job need the same realtime channel

- **Learning:** Logistics is inherently two-sided in real time — when something
  changes on a route, both the collector (dispatcher view) and the driver
  (executor view) need to know now, not on next refresh. A single SignalR hub
  pushing the same domain events to both audiences is simpler and cheaper than
  per-app polling or per-role notification channels.
- **Confirmed by:** ADR-0007; Collector app uses SignalR for marketplace +
  route updates; Driver app uses SignalR for new-order push and route changes.
  No polling fallback has been needed in the pilot.
- **Implications:**
  - Treat realtime as a first-class transport, not an optimization. New
    domain events (route reordered, order reassigned, evidence captured)
    should publish to SignalR by default.
  - Keep the event payload small — push the *fact* of change + the entity id;
    let the client re-fetch through the BFF for the full shape. This avoids
    re-implementing authorization in the push channel.
  - When we add a third surface (admin live board, customer "your driver is
    en route" view), it joins the same hub — no new infrastructure.
- **Date promoted:** 2026-05-25

## L-003 — Evidence is a collection, not a column

- **Learning:** The original model captured a single image per order. Real
  pickup/delivery scenarios produce *multiple* artefacts — several photos
  from different angles, a weight slip, a signed manifest, supplementary
  documents. We extended the model from a single field on the order to a
  first-class `OrderEvidence` collection with typed entries (`Photo`,
  `WeightSlip`, `Signature`, `Document`) keyed to a stage (`Pickup` /
  `Delivery`).
- **Confirmed by:** Pilot operations — drivers naturally capture 2–4 photos
  per stop, and dispute resolution improves when supporting documents can
  attach alongside the photo.
- **Implications:**
  - Any future artefact type (e.g., video, 3D scan, AI-classified fraction)
    is an additive entry in the existing collection — no schema break.
  - Computer-vision waste classification (R&D projects #6–8) consumes the
    same evidence collection; no separate ingestion path.
  - When in doubt about "one or many" on a domain entity, prefer **many**
    if the cost is a child collection — going from one to many is a painful
    migration; going from many to one is free.
- **Date promoted:** 2026-04-10

## L-004 — Audit trails must store IDs, not names

- **Learning:** Embedding display names in audit messages is a GDPR + accuracy
  trap; store user IDs and resolve at read time.
- **Confirmed by:** ADR-0003, internal review of `OrderActivity` prototype.
- **Implications:** All new domain events follow the ID-only pattern. BFFs own
  batch name resolution; domain services never know about display strings.
- **Date promoted:** 2025-12-10

## L-005 — BFF aggregation beats frontend orchestration

- **Learning:** Putting per-screen aggregation in a thin BFF beats letting the
  Vue app fan out to 3–4 services per view, both for latency and for keeping
  auth logic in one place.
- **Confirmed by:** ADR-0002; observed in Collector "Company Orders" screen
  where pre-BFF prototype paid 4 round-trips per render.
- **Implications:** Any new role-specific surface (e.g., dispatcher portal)
  gets its own BFF rather than richer endpoints in a shared service.
- **Date promoted:** 2025-12-15

## L-006 — Sequence belongs to the aggregate, not the leaf

- **Learning:** Route stop sequence on the Route (ordered ID array) is
  dramatically simpler than a sequence field on the Order — 1 write vs. N,
  and integrity is intrinsic.
- **Confirmed by:** ADR-0004; drag-and-drop UX in Collector app.
- **Implications:** Apply the same lens to future N-position aggregates
  (e.g., delivery manifests, inspection checklists).
- **Date promoted:** 2026-01-08

## L-007 — `Money` as a value object pays off across services

- **Learning:** A shared `Money` value object (Currency + Amount, with safe
  arithmetic) avoids decimal drift and floating-point bugs that plagued the
  early Product Service.
- **Confirmed by:** Cross-service order totalling now matches to the øre;
  zero rounding bugs reported since adoption.
- **Implications:** Codify as a tiny shared kernel; resist the urge to
  re-implement per service.
- **Date promoted:** 2026-02-02

## L-008 — JIT provisioning on every request, not just on login

- **Learning:** Running the JIT-provisioning filter on every BFF request
  (not just first login) keeps the Wastr user record in sync with AAD group
  changes (company moves, role grants) without an out-of-band sync job.
- **Confirmed by:** Three observed cases where a user's company changed in
  AAD and was reflected on the next API call.
- **Implications:** User Service is on the hot path; must stay fast and
  highly available. In-memory short-TTL cache acceptable.
- **Date promoted:** 2026-02-18

## L-009 — Service-to-service auth via client credentials > shared API key

- **Learning:** Azure AD client-credential tokens (`AcquireTokenForClient`)
  give per-service identity, audit, and rotation for free; shared API keys
  conflated services and were a security review smell.
- **Confirmed by:** Security review pre-pilot, no incidents since switch.
- **Implications:** Every new service-to-service call uses client credentials.
  Basic Auth allowed only for legacy / on-prem integrations.
- **Date promoted:** 2026-03-05

## L-010 — Resolve address at the picker, not at confirmation

- **Learning:** Reverse-geocoding the user's pin at the moment they drop it
  (on the address-picker step) beats deferring resolution to the final
  confirmation screen. When resolution fails or returns something nonsensical,
  the user can edit the address inline — before they've mentally moved on.
- **Confirmed by:** Customer-app flow change. Pre-change, ~12% of orders
  arrived at confirmation with a wrong/empty address and required back-tracking;
  post-change, the picker exposes the resolved string immediately and lets the
  user fix it in place.
- **Implications:**
  - Treat address resolution as part of *location input*, not *order review*.
  - Any future picker (delivery, return, depot) should follow the same pattern:
    resolve → show → allow manual edit, all on the same screen.
  - Confirmation screens should be read-only — if the user needs to edit on
    confirmation, the upstream step is broken.
- **Revisit trigger:** if `addressSource = "manual"` rate exceeds 20% over a
  rolling 30-day window, the "resolve at picker" premise is wrong (users are
  systematically overriding the geo-result). Re-evaluate L-010 — candidate
  alternatives: resolve at confirmation, or skip auto-resolution and let the
  user type the address from scratch.
- **Date promoted:** 2026-05-20


## L-011 — In a multi-market product, the localisation tax is identity and money, not the core flow

- **Learning:** A product proven in one market does not generalise by "translating the UI."
  The Brazil pilot showed the core capture flow (QR + photo + geo) transfers
  cleanly to a different waste fraction and a different market with zero
  changes. The *real* localisation work concentrated in two places we
  underestimated: **identity** (CPF replacing Microsoft login as the legitimate
  identifier) and **money** (currency and pricing abstractions that were hard-
  coded to NOK). The hypothesis "core is geography-agnostic" was confirmed;
  the new insight is *where* the per-market cost actually lives.
- **Confirmed by:** [EXPERIMENT #30](https://github.com/wastr-as/wastr-learning-loop/issues/30)
  (Brazil cooking-oil pilot, 2025-11-21 → 2026-02-20) and the cluster of
  friction bugs that surfaced during it — CPF identity, address format (CEP +
  apartment + responsible person), and pricing/currency rigidity.
- **Implications:**
  - Treat **identity** and **currency** as first-class architectural
    abstractions, not configuration values. New-market entry should never
    require touching domain code for these.
  - The product's competitive moat (QR + photo + geo capture, two-way routing)
    is *transferable*; do not delay EU expansion on assumptions that the core
    flow needs rework per market.
  - Pricing/currency abstraction is a near-term technical bet to derisk
    market #3. Without it, every new country re-pays the same tax.
  - When scoping the next pilot, budget for identity + address + money work
    explicitly; do not bury them inside "localisation."
- **Date promoted:** 2026-06-02
