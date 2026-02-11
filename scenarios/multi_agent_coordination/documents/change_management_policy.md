# Change Management Policy

## Change Freeze Windows

Production deploys are NOT permitted during the following periods:

- Fridays after 14:00 UTC through Monday 06:00 UTC
- During any active Sev1 incident
- Company-wide maintenance windows (announced 48 hours in advance)

Any deploy during a freeze window is a **policy violation** and requires a post-incident review.

## Change Ticket Requirements

All production deployments MUST have an associated change ticket (CHG-xxxx):

- **Critical tier services**: Require 2 approvers before merge and deploy
- **Standard tier services**: Require 1 approver
- **Internal tier services**: Self-approval permitted but ticket still required

A deploy without a change ticket is a **policy violation**.

## Rollback SLA

- **Critical tier services**: Rollback must begin within 15 minutes of detecting a production issue caused by the deploy
- **Standard tier services**: Rollback must begin within 30 minutes
- If a rollback is not available (rollback_available = false), the team must document an alternative remediation plan within the same SLA window

## Emergency Change Process

When a change must be made during a freeze window or without a ticket (e.g., to resolve a Sev1 incident):

1. The incident commander must explicitly authorize the change
2. A retroactive change ticket must be filed within 4 hours
3. The change must be documented in the incident timeline
4. A post-incident review must assess whether the emergency change was justified
