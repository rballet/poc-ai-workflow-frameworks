# Meridian Tech — Incident Log

## INC-2025-042: Network Partition in Portland Datacenter

- **Date**: 2025-01-08 03:22 UTC
- **Severity**: P1
- **Status**: Resolved
- **Affected Server**: prod-api-03
- **Duration**: 47 minutes
- **Root Cause**: A firmware bug in the top-of-rack switch (Arista 7280R3) caused a spanning tree reconvergence event, resulting in a network partition between racks R-400 through R-420. Traffic to and from affected servers was dropped for the duration.
- **Resolution**: Network engineering team applied an emergency firmware patch (EOS 4.32.1F-hotfix) to the affected switch. Traffic was restored at 04:09 UTC after the switch completed its reboot cycle.
- **Follow-up Actions**: Scheduled firmware audit of all Arista switches across all datacenters. Added STP reconvergence monitoring to the alerting stack.
- **Post-Incident Review**: Completed 2025-01-10, led by SRE team.

## INC-2025-038: Memory Exhaustion on Helios Payment Service

- **Date**: 2025-01-03 14:15 UTC
- **Severity**: P2
- **Status**: Resolved
- **Affected Server**: prod-api-01
- **Duration**: 23 minutes
- **Root Cause**: A memory leak in the connection pool library (hikaricp 5.1.0) caused gradual memory exhaustion over 72 hours. The JVM eventually triggered an OutOfMemoryError, crashing the payment processing worker.
- **Resolution**: The on-call engineer restarted the service and applied a configuration change to limit the connection pool size. A permanent fix was deployed the following day with an upgraded library version (hikaricp 5.2.1).
- **Follow-up Actions**: Added JVM heap usage alerts at 80% and 90% thresholds. Scheduled dependency audit for all Java services.
- **Post-Incident Review**: Completed 2025-01-06, led by Payments Engineering team.

## INC-2025-031: SSL Certificate Expiry on Staging

- **Date**: 2024-12-20 09:00 UTC
- **Severity**: P3
- **Status**: Resolved
- **Affected Server**: staging-01
- **Duration**: 2 hours
- **Root Cause**: The SSL certificate for staging.meridian.internal expired. The cert-manager renewal job had been silently failing for two weeks due to a misconfigured ACME endpoint.
- **Resolution**: Manually renewed the certificate and fixed the cert-manager configuration.
- **Follow-up Actions**: Added certificate expiry monitoring with 30-day and 7-day warnings.
- **Post-Incident Review**: Completed 2024-12-22, led by Platform Infrastructure team.

## INC-2025-027: Slow Query Performance on Titan

- **Date**: 2024-12-12 18:30 UTC
- **Severity**: P2
- **Status**: Resolved
- **Affected Server**: prod-api-02
- **Duration**: 1 hour 15 minutes
- **Root Cause**: A missing database index on the `inventory_transactions` table caused full table scans during the evening batch import. Query latency spiked from 50ms to over 8 seconds, triggering upstream timeouts.
- **Resolution**: Added the missing composite index on `(warehouse_id, created_at)`. Query latency returned to normal within minutes of the index build completing.
- **Follow-up Actions**: Implemented query performance regression testing in CI. Added slow query log monitoring.
- **Post-Incident Review**: Completed 2024-12-15, led by Supply Chain Engineering team.
