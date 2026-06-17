# ADR-0020: Frontend (SPA) telemetry via build-time connection-string injection

- **Status:** Accepted
- **Date:** 2026-06-17
- **Deciders:** Siarhei (CTO)
- **Issue:** –

## Context

The WASTR frontends report telemetry to Azure Application Insights using the
client-side `@microsoft/applicationinsights-web` SDK. Unlike the backend
services (App Services / containers) — which read
`APPLICATIONINSIGHTS_CONNECTION_STRING` from an **app setting at runtime** (see
ADR-0003 for the secret-handling pattern) — a Single Page App has **no server
process at the edge**. The telemetry runs in the visitor's browser, so the
connection string must physically exist **inside the shipped JavaScript bundle**.

This is sharpest for the **landing page** (`wastras.com`):

- It is a **global marketing site**, not per-tenant. It is an Azure **Static Web
  App** (`stapp-wastr`) deployed from GitHub Actions, and lives in the
  `global-infra/shared-resources` Terraform root (alongside ACR and function
  storage) — **not** in the per-tenant root.
- A Static Web App's `app_settings` only reach its managed API/Functions
  backend, **never** the static client bundle — so the runtime-app-setting
  pattern used by the container frontends does not apply.

Two questions had to be answered: (1) which App Insights resource does a global
site report to, and (2) how does the connection string reach the bundle.

## Decision

1. **Dedicated, environment-agnostic telemetry resource for the landing site.**
   `appi-wastr-landing` (+ `law-wastr-landing` Log Analytics workspace) is
   provisioned in `shared-resources` in RG `wastr-shared-services-rg`. The
   global site does **not** reuse any tenant-scoped App Insights.

2. **Connection string injected at build time via a CI secret.**
   The deploy workflow exposes the repo secret `VITE_APP_INSIGHTS_CONNECTION`
   as a build env var; Vite bakes it into the bundle (`import.meta.env`).
   The app initialises App Insights only when that value is present.

3. **The secret is set manually (one-time), not via Terraform.**
   Terraform owns the Azure resource and **outputs** the connection string
   (`landing_appinsights_connection_string`, `sensitive`). Setting the GitHub
   Actions secret is a documented one-liner run once:
   ```pwsh
   $cs = terraform output -raw landing_appinsights_connection_string
   gh secret set VITE_APP_INSIGHTS_CONNECTION \
     --repo wastr-as/Wastr.Apps.Web.Landing --body $cs
   ```

4. **Manual SPA route tracking.** `enableAutoRouteTracking` is **off**; page
   views are emitted from `router.afterEach` so client-side navigations are not
   double-counted.

## Alternatives Considered

1. **Terraform `integrations/github` provider to set the Actions secret**
   (originally implemented, then reverted) — rejected as over-engineering for
   this case: the connection string is effectively immutable for the resource's
   lifetime, so it automates a one-time action. The cost is a long-lived GitHub
   PAT (a *more* sensitive, more frequently rotated secret than the value being
   automated), apply-time coupling (a shared-resources `apply` would fail on an
   expired PAT or GitHub outage even when only touching ACR/storage), and a
   blast-radius blur between Azure provisioning and GitHub repo config. Revisit
   if we manage **many** repo secrets across **many** repos.
2. **Static Web App `app_settings`** — rejected: not visible to the client
   bundle; only reaches the managed API backend.
3. **Reuse a tenant App Insights for the landing site** — rejected: the landing
   page is global; binding it to one tenant's resource is wrong and couples a
   marketing site to tenant lifecycle.
4. **Runtime `config.json` / `/api` config fetch** — rejected here: adds moving
   parts to avoid a rebuild that we essentially never need, since the value is
   stable.

## Consequences

**Positive**

- Single source of truth: Terraform owns `appi-wastr-landing`; the connection
  string is always available via a TF output.
- No extra provider, no PAT bootstrap, no GitHub coupling in the infra apply.
- Clean ownership boundary: TF owns Azure, CI owns the repo secret.

**Negative**

- **Build-time gotcha:** because the value is baked into the bundle, changing
  or first-setting the secret requires a **redeploy** to take effect.
  Re-running the latest workflow run is sufficient (secrets are read at run
  time): `gh run rerun --repo wastr-as/Wastr.Apps.Web.Landing <runId>`, then
  hard-reload (Ctrl+F5).
- One manual step on resource (re)creation — acceptable given the value's
  immutability.
- The connection string is, by design, public in client-side JS (this is how
  browser App Insights works; it is an ingestion key, not a secret granting
  read access).

## Verify

- Browser DevTools → Network → filter `track` (POST to
  `dc.services.visualstudio.com`, status 200).
- Azure `appi-wastr-landing` → Logs: `pageViews | where timestamp > ago(30m)`.

## Monitoring & alerting (provisioned in IaC)

Interpretation and verification are **not** a manual daily chore — they are
provisioned as code in `global-infra/shared-resources`:

- **Workbook** `WASTR Landing — Analytics` (`landing-workbook.json`) pins:
  traffic & top pages, the **conversion funnel** (`hero_calculator_clicked` →
  `calc_started` → `calc_completed` → `save_cta_clicked`), bounce rate,
  exceptions, and load performance (p50/p95). Read the funnel top-to-bottom:
  the largest step-to-step drop-off is where the page loses people.
- **Alerts** (`azurerm_monitor_scheduled_query_rules_alert_v2`, gated on
  `landing_alert_email` so a missing address never blocks `apply`):
  - **No telemetry in 2h** — early warning that a deploy broke the build-time
    connection-string injection (no `pageViews` ingested).
  - **Exception spike** — > 10 client-side errors in 15 min.

**Cadence**
- *Per deploy:* 60-second smoke check — confirm a `track` 200 in DevTools, then
  `exceptions | where timestamp > ago(1h)` shows nothing new.
- *Weekly:* glance at the workbook.
- *Monthly / after calculator or CTA changes:* review the funnel for movement.
- *Otherwise:* rely on the alerts; don't hand-poll.

> Note: only methods actually wired into views emit data today
> (`hero_calculator_clicked`, `calc_started`, `calc_completed`,
> `save_cta_clicked`, `project_cta_clicked`). Other SDK helpers in
> `analytics.ts` (`trackCTA`, `trackSegmentSwitch`, `trackFormSubmission`,
> `trackOutboundLink`, `trackScrollDepth`) exist but are not yet called.

## Revisit Trigger

- If we accumulate **many** CI-managed repo secrets across repos (the
  `github` Terraform provider then becomes worth its bootstrap cost).
- If a frontend needs to **change** its telemetry target without a rebuild
  (move to runtime config fetch).
