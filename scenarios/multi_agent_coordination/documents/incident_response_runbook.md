# Incident Response Runbook

## Severity Definitions

- **Sev1**: Customer-facing outage or data loss. Multiple services or customers affected.
- **Sev2**: Degraded service performance. Single service or limited customer impact.
- **Sev3**: Internal tooling issue or cosmetic defect. No customer impact.

## Response SLAs

### Sev1 Response

1. Engage incident commander within 5 minutes of alert
2. Page ALL affected service owners immediately
3. Establish bridge call within 10 minutes
4. Post status update to stakeholders every 15 minutes
5. Root cause must reference both infrastructure evidence and security posture

### Sev2 Response

1. Notify team lead within 15 minutes of alert
2. Single-threaded investigation by owning team
3. Post status update every 30 minutes
4. Escalate to Sev1 if escalation triggers are met (see below)

## Escalation Triggers: Sev2 to Sev1

A Sev2 incident MUST be escalated to Sev1 if ANY of the following are true:

1. Cascading impact detected -- the affected service has downstream dependents that are also degraded
2. Incident remains in "investigating" status for more than 60 minutes without identification
3. Anomalous access patterns suggest active exploitation (anomaly_score > 0.7 in access logs)
4. Explicit compliance or legal trigger (e.g., GDPR data exposure in EU region)

## Post-Mortem Requirements

- **Sev1**: Post-mortem document required within 48 hours. Must include root cause, timeline, action items.
- **Sev2**: Post-mortem required within 1 week if unresolved for more than 2 hours.
- **Sev3**: Optional post-mortem at team discretion.

## Communication Protocol

- Sev1: Notify VP Engineering and customer success within 30 minutes
- Sev2: Notify engineering manager within 1 hour
- All incidents must be logged in the incident tracking system with accurate timeline entries
