# ADR-0008: Immutable Audit Trail — Store IDs, Resolve Names at Read Time

- **Status:** Accepted
- **Date:** 2025-12-10
- **Deciders:** Siarhei (CTO)

## Context

Early prototype embedded user display names into `OrderActivity.Message`
("Order accepted by Lars Hansen"). Two problems emerged quickly:

1. **Names change.** Users rename, marry, leave the company. The audit trail
   then contained either stale names or required destructive rewrites.
2. **GDPR / right-to-be-forgotten.** Names in audit messages must be redactable;
   embedded strings are a nightmare to find.

## Decision

- All `CreatedBy` / `UpdatedBy` / `CapturedBy` fields store **user IDs** (Guid).
- `OrderActivity.Message` contains only the status description ("Status changed
  to Accepted") — never a person's name.
- BFFs resolve IDs → names at **read time** via `POST /api/user/batch/names`
  and populate transient `CreatedByName` properties on outbound DTOs.
- If the User Service is unavailable, names degrade to `null` — never break
  the order read.

## Alternatives Considered

1. **Denormalize name at write time, plus update job on rename** — rejected:
   eventual-consistency hazard, every rename triggers a fan-out write.
2. **Embed `{ id, snapshotName }` tuple at write time** — rejected: snapshot
   immediately becomes stale and misleading, defeating the purpose.

## Consequences

**Positive**
- Audit trail is genuinely immutable.
- Rename is a User-Service-only operation.
- GDPR redaction = soft-delete the user row; names automatically vanish.

**Negative**
- Every read pays a batch lookup round-trip (mitigated by batching + cache).
- Tests must inject a name-resolver double, not assert on string output.

## Revisit Trigger

- We add cross-tenant reporting that needs frozen historical names (e.g., for
  legal disputes) — at that point, consider an immutable `audit_log_snapshot`
  store separate from operational reads.
