-- Multi-Agent Coordination Scenario: NimbusOps Cloud Infrastructure
-- Two incident storylines embedded in consistent, cross-referenced data.

-- ===== Infrastructure Domain =====

CREATE TABLE clusters (
    cluster_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    region TEXT NOT NULL,
    environment TEXT NOT NULL,
    provider TEXT NOT NULL,
    node_count INTEGER NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO clusters VALUES
    ('CL-001', 'prod-us-east-1', 'us-east-1', 'production', 'aws', 12, 'healthy'),
    ('CL-002', 'prod-eu-west-1', 'eu-west-1', 'production', 'aws', 8, 'degraded'),
    ('CL-003', 'staging-us-east-1', 'us-east-1', 'staging', 'aws', 4, 'healthy'),
    ('CL-004', 'prod-us-west-2', 'us-west-2', 'production', 'gcp', 6, 'healthy'),
    ('CL-005', 'prod-ap-south-1', 'ap-south-1', 'production', 'azure', 3, 'healthy');

CREATE TABLE services (
    service_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    cluster_id TEXT NOT NULL,
    team_owner TEXT NOT NULL,
    tier TEXT NOT NULL,
    port INTEGER NOT NULL,
    replicas INTEGER NOT NULL,
    cpu_limit_mcores INTEGER NOT NULL,
    memory_limit_mb INTEGER NOT NULL,
    last_deploy_at TEXT NOT NULL
);

INSERT INTO services VALUES
    ('SVC-001', 'api-gateway', 'CL-001', 'Platform', 'critical', 8080, 4, 2000, 4096, '2026-02-08T10:00:00Z'),
    ('SVC-002', 'auth-service', 'CL-001', 'Identity', 'critical', 8081, 3, 1000, 2048, '2026-02-10T16:30:00Z'),
    ('SVC-003', 'payment-service', 'CL-001', 'Payments', 'critical', 8082, 3, 1500, 3072, '2026-02-05T09:00:00Z'),
    ('SVC-004', 'order-service', 'CL-002', 'Commerce', 'critical', 8083, 3, 1000, 2048, '2026-02-07T11:00:00Z'),
    ('SVC-005', 'notification-service', 'CL-002', 'Commerce', 'standard', 8084, 2, 500, 1024, '2026-02-06T14:00:00Z'),
    ('SVC-006', 'analytics-pipeline', 'CL-004', 'Data', 'standard', 9090, 2, 2000, 8192, '2026-02-09T08:00:00Z'),
    ('SVC-007', 'cdn-edge', 'CL-005', 'Platform', 'standard', 443, 6, 500, 512, '2026-02-01T12:00:00Z'),
    ('SVC-008', 'user-profile', 'CL-001', 'Identity', 'standard', 8085, 2, 500, 1024, '2026-02-04T15:00:00Z');

CREATE TABLE dependencies (
    source_service_id TEXT NOT NULL,
    target_service_id TEXT NOT NULL,
    dependency_type TEXT NOT NULL,
    PRIMARY KEY (source_service_id, target_service_id)
);

INSERT INTO dependencies VALUES
    ('SVC-001', 'SVC-002', 'sync'),
    ('SVC-001', 'SVC-003', 'sync'),
    ('SVC-001', 'SVC-004', 'sync'),
    ('SVC-003', 'SVC-002', 'sync'),
    ('SVC-004', 'SVC-005', 'async'),
    ('SVC-004', 'SVC-003', 'sync'),
    ('SVC-005', 'SVC-006', 'async'),
    ('SVC-001', 'SVC-008', 'sync'),
    ('SVC-008', 'SVC-002', 'sync');

CREATE TABLE recent_deploys (
    deploy_id TEXT PRIMARY KEY,
    service_id TEXT NOT NULL,
    deployed_at TEXT NOT NULL,
    deployed_by TEXT NOT NULL,
    change_ticket TEXT,
    image_tag TEXT NOT NULL,
    rollback_available BOOLEAN NOT NULL
);

INSERT INTO recent_deploys VALUES
    ('DEP-101', 'SVC-001', '2026-02-08T10:00:00Z', 'alice@nimbusops.io', 'CHG-5501', 'api-gw:v3.1.0', 1),
    ('DEP-102', 'SVC-002', '2026-02-10T16:30:00Z', 'bob@nimbusops.io', NULL, 'auth:v2.4.1-rc3', 1),
    ('DEP-103', 'SVC-003', '2026-02-05T09:00:00Z', 'carol@nimbusops.io', 'CHG-5480', 'payment:v4.0.2', 1),
    ('DEP-104', 'SVC-004', '2026-02-07T11:00:00Z', 'dave@nimbusops.io', 'CHG-5495', 'orders:v2.8.0', 1),
    ('DEP-105', 'SVC-006', '2026-02-09T08:00:00Z', 'eve@nimbusops.io', 'CHG-5510', 'analytics:v1.3.0', 0),
    ('DEP-106', 'SVC-007', '2026-02-01T12:00:00Z', 'frank@nimbusops.io', 'CHG-5450', 'cdn:v5.2.1', 1);

-- ===== Security Domain =====

CREATE TABLE vulnerability_scans (
    scan_id TEXT PRIMARY KEY,
    service_id TEXT NOT NULL,
    scanned_at TEXT NOT NULL,
    severity TEXT NOT NULL,
    cve_id TEXT,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    remediation_deadline TEXT
);

INSERT INTO vulnerability_scans VALUES
    ('SCAN-201', 'SVC-004', '2026-02-08T06:00:00Z', 'critical', 'CVE-2025-31337', 'Remote code execution in container base image', 'open', '2026-02-09T06:00:00Z'),
    ('SCAN-202', 'SVC-002', '2026-02-09T06:00:00Z', 'medium', 'CVE-2025-28100', 'Information disclosure in JWT parsing library', 'mitigated', NULL),
    ('SCAN-203', 'SVC-001', '2026-02-09T06:00:00Z', 'low', NULL, 'Outdated TLS cipher suite configuration', 'open', '2026-03-01T00:00:00Z'),
    ('SCAN-204', 'SVC-003', '2026-02-09T06:00:00Z', 'high', 'CVE-2025-29555', 'SQL injection in legacy query builder', 'open', '2026-02-12T00:00:00Z'),
    ('SCAN-205', 'SVC-006', '2026-02-10T06:00:00Z', 'medium', NULL, 'Unencrypted internal metrics endpoint', 'false_positive', NULL);

CREATE TABLE access_logs (
    log_id TEXT PRIMARY KEY,
    service_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    source_ip TEXT NOT NULL,
    action TEXT NOT NULL,
    user_agent TEXT,
    anomaly_score REAL NOT NULL
);

INSERT INTO access_logs VALUES
    ('LOG-301', 'SVC-004', '2026-02-10T14:05:00Z', '198.51.100.42', 'allow', 'python-requests/2.31', 0.85),
    ('LOG-302', 'SVC-004', '2026-02-10T14:06:00Z', '198.51.100.42', 'allow', 'python-requests/2.31', 0.91),
    ('LOG-303', 'SVC-004', '2026-02-10T14:07:00Z', '198.51.100.43', 'allow', 'python-requests/2.31', 0.88),
    ('LOG-304', 'SVC-004', '2026-02-10T14:10:00Z', '198.51.100.42', 'rate_limit', 'python-requests/2.31', 0.95),
    ('LOG-305', 'SVC-001', '2026-02-10T15:00:00Z', '10.0.1.50', 'allow', 'internal-health-check/1.0', 0.02),
    ('LOG-306', 'SVC-002', '2026-02-10T16:35:00Z', '10.0.1.100', 'allow', 'internal-service/auth-client', 0.05),
    ('LOG-307', 'SVC-003', '2026-02-10T17:00:00Z', '10.0.1.100', 'allow', 'internal-service/payment-client', 0.10),
    ('LOG-308', 'SVC-004', '2026-02-10T14:12:00Z', '203.0.113.99', 'deny', 'curl/8.4.0', 0.72);

CREATE TABLE firewall_rules (
    rule_id TEXT PRIMARY KEY,
    cluster_id TEXT NOT NULL,
    direction TEXT NOT NULL,
    source_cidr TEXT NOT NULL,
    dest_port INTEGER NOT NULL,
    protocol TEXT NOT NULL,
    action TEXT NOT NULL,
    last_modified_at TEXT NOT NULL,
    modified_by TEXT NOT NULL
);

INSERT INTO firewall_rules VALUES
    ('FW-401', 'CL-001', 'ingress', '0.0.0.0/0', 443, 'tcp', 'allow', '2026-01-15T10:00:00Z', 'alice@nimbusops.io'),
    ('FW-402', 'CL-001', 'ingress', '10.0.0.0/8', 8080, 'tcp', 'allow', '2026-01-15T10:00:00Z', 'alice@nimbusops.io'),
    ('FW-403', 'CL-002', 'ingress', '0.0.0.0/0', 443, 'tcp', 'allow', '2026-01-20T09:00:00Z', 'dave@nimbusops.io'),
    ('FW-404', 'CL-002', 'ingress', '198.51.100.0/24', 8083, 'tcp', 'allow', '2026-02-10T12:00:00Z', 'bot-scanner@security-automation'),
    ('FW-405', 'CL-002', 'egress', '0.0.0.0/0', 443, 'tcp', 'allow', '2026-01-20T09:00:00Z', 'dave@nimbusops.io'),
    ('FW-406', 'CL-004', 'ingress', '10.0.0.0/8', 9090, 'tcp', 'allow', '2026-01-25T14:00:00Z', 'eve@nimbusops.io');

-- ===== Shared: Incidents and Timeline =====

CREATE TABLE incidents (
    incident_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    affected_service_id TEXT NOT NULL,
    opened_at TEXT NOT NULL,
    identified_at TEXT,
    resolved_at TEXT,
    commander TEXT NOT NULL,
    root_cause TEXT
);

INSERT INTO incidents VALUES
    ('INC-4001', 'payment-service 503 errors after auth-service deploy', 'sev1', 'mitigating', 'SVC-003', '2026-02-10T17:15:00Z', '2026-02-10T18:00:00Z', NULL, 'alice@nimbusops.io', NULL),
    ('INC-4002', 'order-service degraded performance in eu-west-1', 'sev2', 'investigating', 'SVC-004', '2026-02-10T14:30:00Z', NULL, NULL, 'dave@nimbusops.io', NULL);

CREATE TABLE incident_timeline (
    entry_id TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    author TEXT NOT NULL,
    domain TEXT NOT NULL,
    entry_text TEXT NOT NULL
);

INSERT INTO incident_timeline VALUES
    ('TL-001', 'INC-4001', '2026-02-10T17:15:00Z', 'monitoring-bot', 'infrastructure', 'Alert: payment-service error rate spiked to 45% (503 responses). Threshold: 5%.'),
    ('TL-002', 'INC-4001', '2026-02-10T17:18:00Z', 'alice@nimbusops.io', 'operations', 'Incident commander assigned. Paging Payments team.'),
    ('TL-003', 'INC-4001', '2026-02-10T17:45:00Z', 'carol@nimbusops.io', 'infrastructure', 'payment-service itself looks healthy. Upstream auth-service responding with p99 latency 8200ms (baseline: 120ms).'),
    ('TL-004', 'INC-4001', '2026-02-10T18:00:00Z', 'bob@nimbusops.io', 'infrastructure', 'Confirmed: auth-service deploy v2.4.1-rc3 at 16:30 introduced latency regression. Rollback initiated.'),
    ('TL-005', 'INC-4001', '2026-02-10T18:05:00Z', 'alice@nimbusops.io', 'operations', 'Note: Identity team (auth-service owners) were not paged until 18:00 -- 45 minute delay from incident open.'),
    ('TL-006', 'INC-4002', '2026-02-10T14:30:00Z', 'monitoring-bot', 'infrastructure', 'Alert: order-service p95 latency increased to 4500ms in eu-west-1 (baseline: 200ms).'),
    ('TL-007', 'INC-4002', '2026-02-10T14:45:00Z', 'dave@nimbusops.io', 'operations', 'Incident opened. Investigating order-service degradation. No recent deploys to this service.'),
    ('TL-008', 'INC-4002', '2026-02-10T15:10:00Z', 'security-bot', 'security', 'Anomalous traffic detected on SVC-004 port 8083 from 198.51.100.0/24. Multiple requests with anomaly_score > 0.8.'),
    ('TL-009', 'INC-4002', '2026-02-10T15:30:00Z', 'dave@nimbusops.io', 'operations', 'Firewall rule FW-404 found: port 8083 opened to 198.51.100.0/24 by bot-scanner@security-automation at 12:00 today. No change ticket associated.'),
    ('TL-010', 'INC-4002', '2026-02-10T16:00:00Z', 'security-bot', 'security', 'Reminder: SCAN-201 (CVE-2025-31337, critical) for order-service is past remediation deadline (was 2026-02-09T06:00:00Z).');
