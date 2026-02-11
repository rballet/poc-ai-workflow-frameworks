# Escalation Matrix

## Team Ownership Rules

- Payment and checkout incidents (`payment_gateway`, `checkout_timeout`) route to **Platform Reliability** once escalated.
- Logistics incidents (`carrier_misroute`, `warehouse_capacity`) route to **Fulfillment Operations**.
- Account communication remains with the owning account team unless Sev1 escalation is active.

## Sev1 Commander Rules

Wake Sev1 commander only when at least one condition is true:

1. Active unresolved P1 incident.
2. Cascading failures across multiple customers.
3. Explicit compliance/legal trigger.

If none of the above apply, keep case in normal support ownership.

## Enterprise Overlay

For Enterprise accounts:

- Keep **Strategic Accounts** in the escalation loop.
- If order value exceeds $10,000, notify Strategic Accounts on-call even when technical ownership is elsewhere.

## On-Call Source

The `oncall` table is the source of truth for who is on-call right now.
