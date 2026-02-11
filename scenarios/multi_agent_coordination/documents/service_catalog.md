# Service Catalog

## Service Tier Definitions

| Tier | Uptime SLA | Description |
|------|-----------|-------------|
| Critical | 99.99% | Customer-facing services that directly impact revenue or authentication |
| Standard | 99.9% | Supporting services with indirect customer impact |
| Internal | Best-effort | Internal tools and pipelines |

## Team Ownership Directory

| Team | Services | On-Call Primary | On-Call Secondary |
|------|----------|----------------|-------------------|
| Platform | api-gateway, cdn-edge | Alice Chen | Frank Liu |
| Identity | auth-service, user-profile | Bob Kumar | Grace Park |
| Payments | payment-service | Carol Davis | Henry Zhao |
| Commerce | order-service, notification-service | Dave Wilson | Irene Santos |
| Data | analytics-pipeline | Eve Martinez | Jack Thompson |

## Dependency and Blast Radius

### api-gateway (Critical)
- Direct upstream: None (entry point)
- Direct downstream: auth-service (sync), payment-service (sync), order-service (sync), user-profile (sync)
- Blast radius: ALL customer-facing traffic routes through this service

### auth-service (Critical)
- Direct upstream: api-gateway, payment-service, user-profile
- Direct downstream: None
- Blast radius: Authentication failure cascades to all services that require auth tokens

### payment-service (Critical)
- Direct upstream: api-gateway, order-service
- Direct downstream: auth-service (sync)
- Blast radius: Payment processing halts if this service is down

### order-service (Critical)
- Direct upstream: api-gateway
- Direct downstream: notification-service (async), payment-service (sync)
- Blast radius: Order placement and status queries fail

### notification-service (Standard)
- Direct upstream: order-service
- Direct downstream: analytics-pipeline (async)
- Blast radius: Customer notifications delayed but orders still process

## Capacity Thresholds

- CPU sustained above 80% for 5 minutes: Alert
- CPU sustained above 90% for 5 minutes: Page on-call
- Memory above 85%: Alert
- Memory above 95%: Page on-call and trigger auto-scaling if available
