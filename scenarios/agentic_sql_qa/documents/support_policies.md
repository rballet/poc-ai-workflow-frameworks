# Support Policies

## Shipping Credit Policy

An order is eligible for a shipping credit when all of the following are true:

1. Status is `delivered`.
2. Delivery delay is **24 hours or more**.
3. Delay reason is **not** weather, customs hold, or force majeure.

Credit caps by account tier:

- Enterprise: 15% of order total (max $1500)
- Growth: 10% of order total (max $500)
- Starter: 5% of order total (max $100)

## Failed Order Refund Policy

- `payment_gateway` incidents on failed orders: full refund and immediate escalation.
- `fraud_review` incidents on failed orders: no automatic refund; manual review required.
- `pick_pack_error` on delivered orders: goodwill credit only.
  - Enterprise: 8% of order total
  - Non-enterprise: 5% of order total

## Auto-Escalation Triggers

Escalate immediately if **any** condition is met:

- Unresolved P1 incident older than 15 minutes.
- Enterprise customer waiting more than 24 hours.
- High-priority open case with no agent update for more than 6 hours.
