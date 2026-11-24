# ADR-0022: Compliance Documents — One Manifest per Order, Held by the Hauler Company, Stored in Cosmos DB in Ordering

- **Status:** Proposed
- **Date:** 2026-11-24
- **Deciders:** Siarhei (CTO)
- **Related:** SPEC #116 (manifest, MTR), SPEC #117 (certificate, CDF), #119 and ADR-0021 (market model), #120 (Norwegian hazardous-waste declaration), #111 (report and weighing), #113 (receiver weight import), #115 (demand test), ADR-0005 (Cosmos for Ordering), ADR-0011 (Fleet service with its own datastore), ADR-0015 (what we do not claim), ADR-0016 (project ownership)

## Context

#116 and #117 add two records that WASTR **prepares and tracks but never issues**: a
manifest per movement of waste (Brazil: MTR) and a certificate of destination
(Brazil: CDF). They need an official reference and PDF, a history of divergences, an
N:N link between certificates and manifests, an audit trail, and strict company
isolation. Two questions must be answered before building: **what one manifest
represents**, and **where the data lives**.

Facts that shape the answer:

- Norway is the first market. The MTR/CDF work is a **demo for a municipality in Rio
  de Janeiro**, and the demand is unvalidated (#115). The choice must be cheap and
  reversible.
- Ordering uses Cosmos DB (ADR-0005). Containers today: `orders` (`/id`),
  `order_activities` (`/OrderId`), `routes` (`/CollectorId`), `route_tracks`
  (`/RouteId`), `projects` (`/CompanyId`), created in
  `global-infra/services/ordering/main.tf`. The service connects with a connection
  string.
- An `Order` has one customer, one pickup address, a `ProjectId`, and, once accepted
  and routed, the hauler's `CompanyId`, `RouteId` and `DriverId`. A `Project` has its
  own `CompanyId` (the builder, ADR-0016).
- What is measured today (#111): the driver records a **crane weight per order** at
  pickup (a real per-order measurement, but a crane scale is less accurate than a
  certified weighbridge). The receiving station's **weighbridge weighs the whole
  load**, not each order. #111 shares that load weight out over the orders of the
  drop-off in proportion to crane weight (`share = weighbridge x crane / sum of crane
  weights`); this is an allocation, not a measurement. It is refused when any order
  of the drop-off has no crane weight, and the #111 report falls back to the crane
  weight when there is no usable weighing. A named review resolves mismatches per
  weighing.
- From the #115 desk check: the generator is the legal issuer of an MTR and the
  hauler confirms and carries it; the RJ receipt deadline is 7 days, the CDF 90 days.
- #120 (Norwegian hazardous-waste declaration) has the same shape: a reference per
  consignment, from generator to receiver.

## Decision

1. **One manifest per order.** An order has one generator, one pickup address and,
   once routed, one planned receiver, which is the legal unit of an MTR (one
   generator, one transporter, one receiver). A route drop-off that takes several
   orders gives several manifests; each stores `OrderId`, `RouteId` and the drop-off.
   The weighing is **not** measured per order, so the received quantity follows the
   rules in decision 6. If an order is split
   between two receivers, a second manifest is created from the same order, so the
   key is `OrderId` plus a sequence (usually 1:1). A hauler-issued "romaneio" (one
   route, many generators) is a later kind and not part of v1.
2. **The hauler company holds the record.** A manifest exists only for a routed order,
   so the hauler's `CompanyId` is always known and is the partition key. The
   generator (`Project.CompanyId`) reads it through a secondary query on
   `GeneratorCompanyId`, built when the builder app needs it.
3. **Storage: Cosmos DB in Ordering**, one new container `compliance-documents`,
   partition key `/CompanyId`, holding typed documents:
   - `manifest`: parties, vehicle, items, planned receiver, official reference,
     status, outcome of the receipt;
   - `certificate`: official number, receiver, items, attachment reference;
   - `link`: certificate item to manifest item (N:N, one document per link);
   - `event`: one audit entry.

   All documents of a company share a partition, so a certificate with its links and
   events is written in **one transactional batch** (same partition, up to 100
   operations), and the queue "received, no CDF, past deadline" is a single-partition
   query. Tenant isolation follows: every read carries the caller's `CompanyId` as the
   partition key.
4. **Attachments in Blob Storage**, a new private container `compliance-documents`.
   Each file has a SHA-256 checksum and a versioned blob name; a replacement keeps the
   earlier version. Files are served through short-lived links issued by the API
   (the pattern used for permit proofs in Fleet).
5. **Audit and no deletion.** Every change appends an `event` (user id, time, reason,
   before and after values; names resolved on read, ADR-0008) in the same batch as the
   change. There is no delete endpoint: records are cancelled or superseded. This is
   enforced by the application, not by the database (the service holds a full-access
   connection string).
6. **Demo marking.** Records created in demo mode carry `IsPrototype`, and every PDF
   says it is prepared by WASTR and not an official document (spec RN-08). The RJ
   rules come from a profile that is marked not validated (ADR-0021, decision 6).
7. **Cheap to move later.** A repository interface per aggregate, links as explicit
   documents (relational-shaped), no Cosmos types in the API contract, and the code in
   its own `Compliance` area of Ordering.
8. **Three quantities per item, never overwritten, and a received quantity that is
   not faked.** Each manifest item keeps:

   | Quantity | Source | Rule |
   |---|---|---|
   | Declared | crane weight at pickup | never overwritten; a correction is a new event |
   | Received | first available of: (a) the receiver's own per-manifest figure, entered or imported through #113, source `Receiver`; (b) the weighbridge share, source `Allocated` and labelled "allocated by crane weight"; (c) unknown | what the receiver accepted; the declared quantity is **never** shown as received, unlike the #111 report, which falls back to crane weight for reporting |
   | Certified | the CDF (#117) | what was destined |

   Further rules:
   - **Divergence is judged per load, not per order.** The allocation gives every order
     of a drop-off the same percentage, so it cannot say which order or generator was
     wrong. The tolerance check and the named review from #111 act on the weighing;
     all manifests of that drop-off are marked divergent together, with one
     justification (a user, a date, a reason).
   - **No allocation without crane weights.** If any order of the drop-off has no
     crane weight, no manifest of that drop-off gets an allocated quantity, and the
     received quantity stays unknown until the receiver's figure is entered.
   - **A receiver figure replaces the allocation** (for example when each order is
     weighed or reported separately), and the allocation is kept in the history.
   - **Mixed fractions or classes in one weighing are not split by weight.** If the
     drop-off mixes waste classes (for example hazardous and non-hazardous), received
     quantities need the receiver's figures. How often this occurs is not known.
   - **The weighbridge is the authority** (certified), the crane weight is the
     generator's declaration. The user interface says which is which.
   - Mass and volume are never added (ADR-0021, decision 5).

### Norway
The record shape (parties, items, official reference, receipt, audit) is the same for
a Norwegian hazardous-waste declaration (#120). Which `Kind`s exist is decided in
those specs; this ADR only requires that the container and the model do not rule it
out. #120 starts with discovery, so nothing is built for Norway here.

### Rollout
- `global-infra`: Cosmos container (`services/ordering/main.tf`), blob container,
  `COSMOSDB__CONTAINERS__COMPLIANCEDOCUMENTS` and the storage setting for Ordering.
  Cosmos documents need no SQL script, so the `db/` rule does not apply.
- Deploy order: global-infra, then Ordering, then the Collector BFF and app.

## Alternatives Considered

1. **New Compliance service with Azure SQL** (the ADR-0011 pattern). The better fit
   for relational, audit-heavy data: foreign keys, unique constraints, joins for the
   queue and reports. Cost: a new repository, CI, infrastructure, SQL migrations kept
   in two places, and consistency with Ordering state (the manifest depends on order,
   route and weighing). Not worth it for an unvalidated demo. It is the move if the
   triggers below fire.
2. **A second datastore (SQL) inside Ordering.** Two operational profiles in one
   deployable and still no joins to the Cosmos data. Rejected.
3. **Embed manifests in Order or Route documents.** Breaks on the N:N link with
   certificates, on the 2 MB document limit, and on the growth of audit events; it
   also mixes the operational order with a legal record. Rejected.
4. **Granularity per route drop-off.** Mixes generators in one document, so the
   issuer is unclear. **Per project:** one record for many trips, so a divergence
   cannot be tied to a movement. Both rejected.
5. **Partition by order id** (like `orders`). Reads of one manifest are cheap, but
   the awaiting-CDF queue and per-company listing become cross-partition and a
   certificate cannot be written atomically with links to several manifests.
   Rejected.
6. **Store the allocated weight as the received quantity, as the #111 report does.**
   Simple, but it presents an estimate (a proportional share) as a measurement and
   hides that every order in a load shows the same deviation. Rejected for manifests;
   the report keeps its own rule.
7. **Weigh each order separately at the receiver.** The only real per-order
   measurement, but it needs a weighbridge pass per order. Not assumed; supported when
   the receiver provides the figure (decision 8).

## Open Questions

1. When one truck arrives with several generators' MTRs and one weighing, how does the
   receiver record the quantity per MTR in Rio de Janeiro (own figure per MTR, or a
   proportional split)? To be asked of the RJ contact. It decides whether an
   allocation is acceptable there; for the demo it is labelled as an allocation.
2. How often does one weighing cover mixed waste classes in our Norwegian
   operations? Check against real routes before relying on the allocation.

## Consequences

### Positive
- No new service: one Cosmos container and one blob container.
- Change and audit entry are atomic; tenant isolation follows from the partition key.
- The same record can carry Norwegian declaration references (#120).
- Reuses what exists: order, route, weighing allocation (#111), the attachment pattern
  from Fleet.

### Negative
- No foreign keys or unique constraints; they are enforced in code and covered by
  tests.
- The generator side and any authority-wide report are cross-partition queries, which
  cost more RUs; acceptable at pilot volume.
- Immutability is a code rule, not tamper-evident: whoever has the connection string
  can change a document.
- Ordering grows; keeping the code in its own `Compliance` area is what keeps a later
  extraction possible.
- A manifest cannot exist before the order has a hauler `CompanyId`, so there is no
  "draft before acceptance".
- Per-order received quantities are mostly estimates unless the receiver reports
  them. The manifest shows this (`Allocated` versus `Receiver`), so it looks less
  precise than the #111 report, which is the honest outcome.
- Deviations cannot be traced to a single order or generator when only the load is
  weighed.

## Revisit Trigger

- A second party (receiver, generator, authority) must read or write in its own right
  (#113, builder app): reconsider a separate service with SQL.
- Cross-company reporting or joins become routine, or a logical partition approaches
  20 GB.
- An authority or customer audit requires tamper-evidence (hash chain or immutable
  storage).
- The RJ receiver (or Norwegian practice) shows that an allocation is not accepted as
  the received quantity: require the receiver's per-manifest figure before a manifest
  can be marked received.
- The demand test fails (#115): stop and keep only the Norwegian reference (#120).

## Definition of Done

- [x] Decision recorded (this file) and mirrored as issue #125.
- [ ] Confirmed (Status set to Accepted).
- [ ] Container and blob container added in global-infra with the first #116 slice.
