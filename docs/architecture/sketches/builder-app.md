# Sketch: Builder app — a third front-end for the construction-company segment

> **Status:** Proposed concept, not approved. Pairs with proposed [ADR-0016](../adr/0016-project-ownership-and-builder-app.md). Raised during SPEC #49 Phase 1 review on 2026-06-03 when it became clear that "Projects" cannot live in the stateless Customer app.

## Why a new app

The platform already serves three operational personas with dedicated apps:

| App | Persona | Auth | State |
|---|---|---|---|
| `Wastr.Apps.Web.Customer` | Homeowner / ad-hoc orderer | Guest (none) | **Stateless** — QR → photo → order, no profile, no history |
| `Wastr.Apps.Web.Collector` | Transporter operations manager | Azure AD (company) | Stateful — routes, drivers, marketplace |
| `Wastr.Apps.Web.Driver` | Driver in the truck | Azure AD (company) | Mostly stateful — assigned routes, pickup/delivery |
| `Wastr.Apps.Web.Admin` | Wastr internal | Azure AD (Wastr tenant) | Stateful — users, companies, products |

A **fourth persona** has emerged from SPEC #49 — the **builder-side operations user**:

- Works for a construction company (Veidekke, Skanska, AF Gruppen, "Byggmester X AS")
- Runs 1..N concurrent construction projects
- Needs to:
  - Create / close projects (start date, site address, NS 9431 metadata)
  - See **all orders across all employees of the company** grouped by project
  - Pull **per-project ESG reports** (CO₂ saved, kg per fraction, NS 9431 export)
  - Generate **project-scoped QR posters** to hand out on site
  - Invite colleagues from the same company

This persona is **structurally different** from a homeowner:

- Has a company identity (Azure AD via the builder's own tenant or Vipps for Business)
- Is a recurring user, not single-touch
- Needs admin-style screens, not a 3-step wizard
- ESG/NS 9431 reporting is the **selling point**, not a side feature

Cramming these screens into the Customer app would:

1. Destroy the zero-friction QR-first UX that makes the Customer app work
2. Force a login wall in front of every QR scan
3. Mix two incompatible session models (stateless guest vs. long-lived company member)

## Proposed shape

```
Wastr.Apps.Web.Builder
├── Vue 3 + Vite + Pinia + Tailwind   ← same template as Collector
├── MSAL (Azure AD) — company-scoped via AAD group → CompanyId
├── Routes
│   ├── /projects                      list + create
│   ├── /projects/:id                  overview (orders, totals, status)
│   ├── /projects/:id/orders           order list + filters
│   ├── /projects/:id/esg              NS 9431 report + CO₂ summary
│   ├── /projects/:id/qr               print-ready poster (PDF)
│   └── /team                          invite colleagues into company
└── Backend
    └── Builder BFF — either reuse Collector BFF pattern in a new
        Wastr.Services.Builder repo, or extend Ordering with /api/builder/*
```

## How a builder places an order (the killer flow)

```
Builder employee in app  ──►  Creates project "Storgata 12 - rehab"
       │
       ▼
App generates QR poster   ──►  https://order.wastr.no/q/{projectId}
       │                       (project belongs to Company X)
       ▼
Worker on site scans QR   ──►  Lands in Customer app (stateless, as today)
       │                       URL pre-fills ProjectId
       ▼
Worker takes photo +      ──►  POST /api/order with ProjectId
order, no login                Ordering Service validates ProjectId belongs
                               to a real project, copies CompanyId from the
                               Project → Order
       │
       ▼
Builder sees the order    ──►  Real-time appears in /projects/:id/orders
under the project              (SignalR push)
```

Key property: **the Customer app gains a single query param**, no new screen, no login. All complexity lives in the Builder app.

## Domain implications

This concept depends on the proposed ownership change in [ADR-0016](../adr/0016-project-ownership-and-builder-app.md):

- `Project.CompanyId` (not `CustomerId`) — partition key in Cosmos
- `CreatedBy` keeps the user id for audit only
- `Order.ProjectId` set on QR-scoped guest orders → server copies
  `Project.CompanyId` to `Order.CompanyId` so company-scoped queries Just Work
- A guest customer scanning a project QR is permitted to attach the order to
  that project even without an account (the project owns the relationship,
  not the customer)

## Out of scope for this sketch

- Pricing / invoicing per project (later — Phase 3)
- Multi-tenant builder hierarchies (parent + subsidiary) — not needed v1
- Cost forecasting per project — depends on route-cost engine maturity
- White-labelling the QR poster — graphics task, not architectural

## Open questions to resolve before scaffolding

1. **Identity provider** — do small Norwegian builders have Azure AD tenants?
   Most don't. Likely answer: **Vipps for Business** as primary IdP, AAD as
   the option for larger contractors. Confirms ADR-0010 direction.
2. **BFF placement** — new `Wastr.Services.Builder` service vs. `/api/builder/*`
   surface inside Ordering? Prefer separate service to match Collector/Driver
   symmetry, but bigger ops cost.
3. **Company creation flow** — who creates a "Company" record when the first
   builder employee signs up? JIT from Vipps for Business orgnr claim is the
   obvious answer; needs User Service work.
4. **Project visibility** — all employees of the company see all projects, or
   role-based (project members vs. company admins)? v1: all employees.
5. **Pricing model** — per-project license is in the business plan. App must
   eventually enforce subscription state; defer to Phase 2.

## Effort sketch (informational, not a commitment)

| Slice | Where | Rough scope |
|---|---|---|
| 1. Domain pivot — `Project.CustomerId` → `CompanyId` | Ordering | Small — no prod data yet |
| 2. Order auto-link via QR param | Customer + Ordering | Small |
| 3. Builder app scaffold + Projects CRUD UI | new repo | Medium |
| 4. Builder BFF (or Ordering extension) | new/Ordering | Medium |
| 5. Company creation via Vipps for Business | User Service | Medium-Large |
| 6. ESG/NS 9431 per-project report | Ordering + Builder | Medium |
| 7. Project QR poster generator | Builder | Small |

## Next step

Decide on ADR-0016 (Project ownership). If accepted, do slice 1 immediately
(no migration risk) and defer 3–7 to a real planning round with pilot input.
