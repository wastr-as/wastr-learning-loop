# Hente.no — Analysis and Positioning

> **Status: hypothesis.** Based on one second-hand report (Denis's conversation) and Hente's public website. Hente's software vendor, integrations, capacity and pain points are **unknown**. Nothing below is validated.

_Written: 2026-10-21 · Segment: transporter · Lane: b2b · Domain: customer_

## The signal

Denis spoke to Hente.no (2026-10-20). They said they **already have logistics-management software**, which is what WASTR had tried to offer them.

## What Hente publicly offers

Sources: [homepage](https://www.hente.no/), [operating terms](https://www.hente.no/vilkar), [electric crane truck](https://www.hente.no/innsikt/elektrisk-kranbil). These are company claims, not audited performance.

| Area | Hente's public offering | Implication for WASTR |
|---|---|---|
| Ordering | Online bag collection: choose bag, fraction and collection day; fixed price per bag; invoice after collection | "Order waste collection online" is not a differentiator |
| Services | Bag collection and 5 / 10 / 20 m³ containers in Oslo | Strong overlap with WASTR's initial waste flows and geography |
| Business customers | Planned or ad hoc collections, tailored arrangements | They already serve the segment we want to reach |
| Documentation | Advertises fractions, weight, final destination, recycling rate, traceability | Do not assume they need another reporting dashboard |
| Sustainability | Advertises 100% electric transport and an electric crane truck | "Greener collection" is a weak pitch to them |
| Operational constraints | Terms cover sorting errors, extra charges, waiting time, bag placement and crane-truck access | Better information **before dispatch** is a plausible opportunity — frequency and cost unknown |

## Where WASTR stands

Strongest documented starting point: **capturing the job at source** (QR/mobile order, location, photos, waste type, evidence workflow). Not established: customer-acquisition volume, measured route savings. Full reporting and advanced optimisation are still roadmap (see [product thesis](../strategy/product-thesis.md)). Sell a **small, measurable commercial experiment**, not a mature AI platform.

## Connection points (ranked)

1. **New demand → Hente fulfils (best first angle).** WASTR sources customers Hente does not already reach (small contractors, renovation projects, property managers). Value to Hente is extra contribution margin, not a software subscription. Routing Hente's *existing* customers through WASTR only adds friction.
2. **Better-prepared jobs → fewer clarification calls and collection exceptions (best operational angle).** Structured capture of photos, exact location, access/placement, fraction, quantity and instructions. Pursue only if Hente confirms a real gap. Human review first; no unverified AI classification claims.
3. **Project relationships → Hente as preferred collector (medium term).** WASTR could organise a contractor's waste across several operators while Hente keeps its internal tools. Project-based functionality is still being explored — co-design, not an available product.
4. **Compatible extra stops → better capacity use (later).** More jobs do not automatically mean better routes; measure incremental margin, not job count. Do not lead with "AI routing" or savings percentages.

## Relationship risk

WASTR can look like both partner and future competitor (customer interception, commoditised pricing, duplicate order entry, data use).

| Model | Boundary |
|---|---|
| Hente's own customers using a WASTR workflow | Hente keeps the commercial relationship |
| Customers originated by WASTR | Agree up front who sells, invoices, handles support, refunds and repeat orders |

Recommendation: start with a **referral model** where Hente contracts and invoices the customer. A WASTR-as-reseller model is a separate later agreement. See also the two-channel (operator's own channel vs. WASTR's channel) framing in the Oslo pilot pitch material.

## Discovery questions (before any demo)

1. Which jobs would you like more of — and which do you avoid?
2. What still happens by phone, email or manual re-entry despite your software?
3. What most often causes a collection to take longer or go wrong?
4. Would genuinely new, pre-qualified jobs interest you if your team kept its current tools?
5. How could we hand those jobs over with the least extra work?

Ask about the software vendor, imports or APIs only afterwards — an integration is not a value proposition.

## Proposed pilot (test parameters, not promises)

Four weeks, one agreed Oslo area, selected non-hazardous bag jobs, target 20–30 genuinely new completed jobs.

- Hente defines acceptable jobs, pricing and capacity and keeps its dispatch system.
- WASTR sources customers and prepares order information; absorbs initial coordination work.
- Agree customer-data handling and commercial responsibilities up front.

**Measure:** completed incremental jobs · Hente's contribution after costs and any WASTR fee · WASTR acquisition and coordination cost · extra admin per job · clarification calls, cancellations and exceptions.

**Stop if** WASTR cannot source demand, or Hente is fully booked with better-margin work.

## Segmentation takeaway

The current [hauler pitch](../../../Wastr.Apps.Web.Landing.B2B/src/data/content.en.ts) targets operators running on phone / email / spreadsheets. Hente appears **outside that profile**. One conversation should refine targeting, not trigger a product pivot.

## Open questions

- Which software does Hente use, and what does it not cover?
- Does Hente have spare capacity, and where/when?
- Does Hente want more B2B volume, and of what kind?
- Is Hente a representative "digitised operator", or an outlier?
