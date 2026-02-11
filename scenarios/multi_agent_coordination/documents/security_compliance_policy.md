# Security and Compliance Policy

## Vulnerability Remediation

- **Critical severity**: Must be remediated within 24 hours of scan detection
- **High severity**: Must be remediated within 7 days
- **Medium severity**: Must be remediated within 30 days
- **Low severity**: Tracked and addressed in next planned maintenance

Overdue critical vulnerabilities are reported to the CISO weekly and may trigger service deployment freezes.

## Firewall Rule Management

All firewall rule changes MUST comply with these requirements:

1. A change ticket (CHG-xxxx) must be filed and approved before modification
2. Changes to production clusters require security team approval
3. Automated scanners (bot-scanner@security-automation) may ONLY modify rules using pre-approved templates
4. Pre-approved templates are limited to: blocking known-malicious IPs, rate-limiting by source CIDR
5. Any rule that OPENS a port to an external CIDR (non-10.0.0.0/8) is NOT a pre-approved template and requires manual approval

A firewall change without a ticket or outside pre-approved templates is a **compliance violation**.

## Access Log Monitoring

- Access logs are analyzed in real-time by the anomaly detection system
- Anomaly scores range from 0.0 (normal) to 1.0 (highly anomalous)
- An anomaly score above 0.7 on ANY access log entry triggers automatic security review
- Three or more entries with anomaly_score > 0.7 within 30 minutes triggers a security incident

## Regional Compliance: EU (GDPR)

Services deployed in EU regions (eu-west-1, eu-central-1) have additional requirements:

- All data in transit must be encrypted (TLS 1.2+)
- PII-handling services must log all access for audit purposes
- Any potential data exposure in EU regions must be reported to the DPO within 24 hours
- The order-service in eu-west-1 processes customer PII (names, addresses, payment references)

## Incident Security Assessment

Every Sev1 and Sev2 incident response MUST include a security posture assessment:

1. Check for open vulnerabilities on the affected service
2. Review recent firewall rule changes on the affected cluster
3. Analyze access logs for anomalous patterns during the incident window
4. Document findings in the incident timeline with domain = "security"
