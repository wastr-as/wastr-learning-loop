# ADR-0001: Service Bus for Work, Event Grid for Fan-out

- **Status:** Accepted
- **Date:** 2026-02-12
- **Deciders:** Siarhei (CTO)

## Context

The platform has two distinct asynchronous needs that look similar at first
glance but have opposite semantics:

1. **Work queues.** When a customer order is posted to the marketplace, exactly
   one matching worker must pick it up and process it. Ordered, exactly-once,
   competing-consumers.
2. **Fan-out notifications.** When an order is accepted, multiple independent
   subscribers may want to react: send an email today; SMS, WhatsApp, push
   tomorrow; possibly analytics, billing, audit, AI training pipelines later.

Forcing both onto the same transport leads to either:
- using a queue for fan-out (each new channel = new queue + duplication logic
  in the producer), or
- using a topic for work (loss of exactly-once guarantees, racy consumers).

## Decision

- **Azure Service Bus queues** carry work: marketplace order matching, route
  assignment, evidence post-processing.
- **Azure Event Grid topics** carry domain events for fan-out: `OrderAccepted`,
  `OrderCompleted`, `EvidenceCaptured`, etc.
- The **Notification Service** subscribes to Event Grid and dispatches via
  channel-specific handlers (email today; SMS/WhatsApp/push added without
  touching producers).
- The selection rule is explicit in code review:
  *"must exactly one worker do this?"* → Service Bus.
  *"may zero-to-many subscribers react?"* → Event Grid.

## Alternatives Considered

1. **Service Bus topics + subscriptions for everything** — would technically
   work; rejected because Event Grid's serverless economics and native Azure
   service integrations (Functions, Logic Apps) fit fan-out better.
2. **Kafka / Event Hubs** — rejected: overpowered for current volume; revisit
   when we need replay semantics for ML training pipelines.
3. **In-process events only** — rejected: notification dispatch must survive
   producer restarts and be independently retryable.

## Consequences

**Positive**
- Producers stay dumb — Ordering publishes one event, doesn't know who listens.
- New notification channels are pure additions (new subscriber, new handler).
- Clear semantic boundary: queue = command, topic = event.
- Operational metrics (DLQ depth, subscriber lag) are first-class in Azure.

**Negative**
- Two transports to monitor and budget for.
- Local development requires Service Bus emulator + Event Grid emulator
  (or shared dev namespace).
- Event schema evolution must be backward-compatible (multiple unknown
  consumers).

## Revisit Trigger

- Event volume justifies a streaming platform (Kafka / Event Hubs) for replay
  and exactly-once across consumers.
- A future use-case truly needs ordered fan-out (today this hasn't appeared).
