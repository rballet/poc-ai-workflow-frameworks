# Meridian Tech — SLA Policies

## Overview

Service Level Agreements (SLAs) define uptime guarantees and incident response commitments. Each datacenter is assigned an SLA tier based on its infrastructure capabilities, redundancy level, and the criticality of hosted workloads. SLA tiers are reviewed quarterly by the VP of Engineering.

## SLA Tiers

### Platinum Tier

- **Uptime Guarantee**: 99.99% (≤ 4.3 minutes downtime per month)
- **Incident Response Time**: 15 minutes for P1, 30 minutes for P2
- **Resolution Target**: 1 hour for P1, 4 hours for P2
- **Monitoring**: Continuous, 10-second polling intervals
- **Failover**: Automatic failover with hot standby
- **Backup Frequency**: Every 15 minutes (continuous replication)
- **Applies To**: us-east region datacenters

The Platinum tier is reserved for workloads that require the highest availability, such as payment processing systems and financial APIs. It includes automatic failover capabilities and continuous data replication.

### Gold Tier

- **Uptime Guarantee**: 99.95% (≤ 21.6 minutes downtime per month)
- **Incident Response Time**: 30 minutes for P1, 1 hour for P2
- **Resolution Target**: 2 hours for P1, 8 hours for P2
- **Monitoring**: Continuous, 30-second polling intervals
- **Failover**: Manual failover with warm standby
- **Backup Frequency**: Every hour
- **Applies To**: us-west region datacenters

The Gold tier covers production workloads that need high availability but can tolerate brief interruptions. Manual failover procedures are documented and tested monthly.

### Silver Tier

- **Uptime Guarantee**: 99.9% (≤ 43.2 minutes downtime per month)
- **Incident Response Time**: 1 hour for P1, 4 hours for P2
- **Resolution Target**: 4 hours for P1, 24 hours for P2
- **Monitoring**: Continuous, 60-second polling intervals
- **Failover**: No automatic failover
- **Backup Frequency**: Every 6 hours
- **Applies To**: us-central region datacenters

The Silver tier is used for internal tools, staging environments, and non-customer-facing services. It provides basic monitoring and daily backups but no failover capabilities.

## Escalation Policy

All SLA tiers follow the same escalation hierarchy:
1. On-call engineer for the owning team (auto-paged via PagerDuty)
2. Team lead (paged after 15 minutes without acknowledgment)
3. VP Engineering (paged after 30 minutes without acknowledgment)

## SLA Violation Consequences

- **Platinum**: SLA credits issued at 10x the hourly rate for each hour of breach
- **Gold**: SLA credits issued at 5x the hourly rate for each hour of breach
- **Silver**: No financial penalties; tracked in quarterly review only
