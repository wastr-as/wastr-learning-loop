# Sketch: Routing service — criteria currently in use

> Snapshot of what `Wastr.Services.Routing` actually optimises for **as of 2026-06-04**, after SPEC #47 Phase 1 landed end-to-end (Routing service, Collector BFF, RoutePlannerModal map + Optimise button). Aligned with [ADR-0013](../adr/0013-route-engine-or-tools.md) and [ADR-0018](../adr/0018-route-plan-immutability-driver-executes.md).
>
> This is a "what's wired today vs. what the contract supports" view — useful for triaging the next polish steps and for the R&D portfolio (projects #3–5, #10).

## TL;DR

The solver model is a full CVRP+VRPTW; the **contract** exposes capacity, time windows, multi-vehicle, depot, departure time, toll preference. The **caller (Collector planner)** currently passes only a small subset, so the effective behaviour today is a **TSP with service time, single vehicle, Azure-Maps-traffic-aware durations**.

The gap between contract and UI is intentional Phase 1 scope — the constraint plumbing is already in place server-side.

## Objective

- **Minimise total travel time (seconds)** across all vehicles.
- Arc cost = duration from the Azure Maps route-matrix (real road network, truck profile via Geolocation Service).
- Single-objective. No CO₂, no toll, no balance-across-vehicles term yet.

## Solver configuration

| Setting | Value | Source |
|---|---|---|
| First-solution strategy | `PathCheapestArc` | `OrToolsRouteOptimisationService` |
| Metaheuristic | `GuidedLocalSearch` | `OrToolsRouteOptimisationService` |
| Time limit | **10 s** | `SolverOptions.TimeLimitSeconds` (`appsettings.json`) |
| Unassigned-stop penalty | configurable | `SolverOptions.UnassignedStopPenalty` |

Disjunctions are added per stop so an over-constrained request returns partial solutions plus `UnassignedOrderIds` instead of hard-failing.

## Criteria matrix

Legend: ✅ wired UI → solver · ⚠ defaulted/hardcoded by Collector BFF · ❌ contract supports it, UI sends nothing.

| # | Criterion | How it enters the model | Status today |
|---|-----------|-------------------------|--------------|
| 1 | Travel time between points | `CostMatrix` from Geolocation (Azure Maps route-matrix) | ✅ always |
| 2 | Avoid toll roads | Forwarded to Azure Maps route-matrix | ❌ hardcoded `false` in `RoutePlannerModal.runOptimise()` |
| 3 | Departure time (traffic-aware) | Forwarded to Azure Maps | ❌ not sent |
| 4 | Depot location | Index 0; all vehicles start + end here | ⚠ defaulted to **first stop's coordinates** (TSP round-trip approximation) |
| 5 | Number of vehicles | One OR-Tools vehicle per `VehicleInput` | ⚠ hardcoded to **1** (id = selected driver) |
| 6 | Vehicle capacity (kg) | `AddDimensionWithVehicleCapacity` | ❌ omitted → effectively infinite (`long.MaxValue/4`) |
| 7 | Stop demand (kg) | Per-stop demand in the capacity dimension | ❌ `defaultDemandKg = 0` for every stop |
| 8 | Vehicle shift window (`ShiftStartUtc` / `ShiftEndUtc` / `MaxRouteSeconds`) | Bounds the time dimension per vehicle | ❌ omitted |
| 9 | Per-stop time window | Hard interval on the time dimension | ❌ omitted (open windows) |
| 10 | Service time at each stop | Added to the time dimension at every visit | ✅ `defaultServiceSeconds = 600` (10 min/stop) |
| 11 | Drop penalty (`AddDisjunction`) | Stop can be skipped at fixed cost → returned in `UnassignedOrderIds` | ✅ baseline `SolverOptions.UnassignedStopPenalty` |

## Not in the model at all yet

- **Two-way / reverse logistics** (outgoing materials + return waste). The core IP differentiator from the R&D roadmap (projects #3–5, #10). Today's solver is one-way pickup VRP only.
- **Pickup-and-delivery (PDP) precedence** — needed once a job has both a "drop empty container" and "collect full container" leg.
- **Dynamic per-vehicle cost coefficients** — no `SetFixedCostOfVehicle`, no `SetGlobalSpanCostCoefficient` for balance.
- **Driver skills / vehicle ↔ waste-fraction compatibility.**
- **Reception-site gate fees + opening hours.**
- **CO₂ / emissions** as an objective term — ADR-0014 metric exists but isn't fed into the cost callback.
- **Toll cost** as an objective term — the toll preference flag exists in the contract but the cost-coefficient blend from ADR-0013 (α·duration + β·toll + γ·CO₂ + δ·empty-km) isn't implemented.

## Effective behaviour observed today

> *"Given N stops, one virtual vehicle, no capacity limits, no time windows, 10 minutes service per stop, and Azure-Maps-derived driving durations — find the visit order that minimises total time on a round trip starting and ending at stop #1's coordinates."*

i.e. a **TSP-with-service-time**, single vehicle, traffic-snapshot-aware durations. Good enough as a planner-side preview tool; **not yet a real CVRP/VRPTW** in production behaviour.

## Suggested next polish steps (by value)

1. **Depot picker** in the planner (collector's yard) → fixes the artificial "depot = first stop" choice.
2. **Per-driver vehicle profile** in Fleet service (capacity, shift window) → auto-populates `VehicleInput` so capacity + shift become real.
3. **Send `DepartAt`** = now or scheduled start → unlocks traffic-aware durations rather than current-time snapshots.
4. **Per-order `DemandKg`** from the product weight estimate → activates the capacity dimension.
5. **Per-order time window** from customer-preferred slot → activates VRPTW.
6. **Multi-vehicle support** in the planner → unlocks real CVRP and the route-splitting UX.
7. **Toll + CO₂ cost-coefficient blend** in the solver → realises ADR-0013's α·duration + β·toll + γ·CO₂ + δ·empty-km objective.
8. **Two-way routing PoC** (R&D #5) — the actual competitive moat.

## Pointers

- Solver: [`OrToolsRouteOptimisationService.cs`](https://github.com/wastr-as/Wastr.Services.Routing/blob/main/src/Wastr.Services.Routing.Infrastructure/Optimisation/OrToolsRouteOptimisationService.cs)
- Matrix client: [`GeolocationMatrixClient.cs`](https://github.com/wastr-as/Wastr.Services.Routing/blob/main/src/Wastr.Services.Routing.Infrastructure/Geolocation/GeolocationMatrixClient.cs)
- BFF wrapper: `Wastr.Services.Collector → CollectorController.OptimiseRoute` (commit `1d02a5b`)
- UI caller: `Wastr.Apps.Web.Collector → RoutePlannerModal.runOptimise()` (commit `84f3cda`)
- Map preview: `Wastr.Apps.Web.Collector → RoutePlannerModal` (commit `106ec28`)
