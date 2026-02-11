DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS shipments;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS support_cases;
DROP TABLE IF EXISTS oncall;

CREATE TABLE customers (
  customer_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  tier TEXT NOT NULL,
  region TEXT NOT NULL,
  owner_team TEXT NOT NULL
);

CREATE TABLE orders (
  order_id TEXT PRIMARY KEY,
  customer_id TEXT NOT NULL,
  created_at TEXT NOT NULL,
  total_usd REAL NOT NULL,
  status TEXT NOT NULL,
  warehouse TEXT NOT NULL
);

CREATE TABLE shipments (
  order_id TEXT PRIMARY KEY,
  shipped_at TEXT,
  delivered_at TEXT,
  delay_hours INTEGER NOT NULL,
  delay_reason TEXT NOT NULL
);

CREATE TABLE incidents (
  incident_id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL,
  severity TEXT NOT NULL,
  category TEXT NOT NULL,
  opened_at TEXT NOT NULL,
  resolved_at TEXT
);

CREATE TABLE support_cases (
  case_id TEXT PRIMARY KEY,
  customer_id TEXT NOT NULL,
  order_id TEXT NOT NULL,
  priority TEXT NOT NULL,
  status TEXT NOT NULL,
  opened_at TEXT NOT NULL,
  customer_waiting_hours INTEGER NOT NULL,
  last_update_hours INTEGER NOT NULL
);

CREATE TABLE oncall (
  team TEXT PRIMARY KEY,
  primary_engineer TEXT NOT NULL,
  secondary_engineer TEXT NOT NULL
);

INSERT INTO customers (customer_id, name, tier, region, owner_team) VALUES
  ('C001', 'Northwind Hospitals', 'Enterprise', 'us-east', 'Strategic Accounts'),
  ('C002', 'BlueTrail Retail', 'Growth', 'eu-west', 'Commercial'),
  ('C003', 'Acme Health', 'Enterprise', 'us-west', 'Strategic Accounts'),
  ('C004', 'Horizon Foods', 'Starter', 'us-east', 'SMB');

INSERT INTO orders (order_id, customer_id, created_at, total_usd, status, warehouse) VALUES
  ('ORD-100', 'C001', '2026-02-01T09:10:00Z', 12000, 'delivered', 'WH-ATL'),
  ('ORD-101', 'C002', '2026-02-02T10:15:00Z',  8000, 'delivered', 'WH-DUB'),
  ('ORD-102', 'C003', '2026-02-03T08:20:00Z', 15000, 'failed',    'WH-PDX'),
  ('ORD-103', 'C001', '2026-02-04T11:45:00Z',  6000, 'delivered', 'WH-ATL'),
  ('ORD-104', 'C003', '2026-02-05T13:00:00Z',  7000, 'delivered', 'WH-PDX'),
  ('ORD-105', 'C004', '2026-02-05T14:00:00Z',  1200, 'delivered', 'WH-IAD'),
  ('ORD-106', 'C002', '2026-02-06T15:30:00Z',  4000, 'failed',    'WH-DUB'),
  ('ORD-109', 'C001', '2026-02-07T09:00:00Z',  9500, 'delivered', 'WH-ATL');

INSERT INTO shipments (order_id, shipped_at, delivered_at, delay_hours, delay_reason) VALUES
  ('ORD-100', '2026-02-01T12:00:00Z', '2026-02-02T07:00:00Z',  2, 'none'),
  ('ORD-101', '2026-02-02T14:00:00Z', '2026-02-03T13:00:00Z',  5, 'none'),
  ('ORD-103', '2026-02-04T13:00:00Z', '2026-02-05T08:00:00Z',  0, 'none'),
  ('ORD-104', '2026-02-05T16:00:00Z', '2026-02-07T19:00:00Z', 30, 'carrier_misroute'),
  ('ORD-105', '2026-02-05T16:30:00Z', '2026-02-07T22:00:00Z', 40, 'weather_hold'),
  ('ORD-109', '2026-02-07T12:00:00Z', '2026-02-08T10:00:00Z', 12, 'none');

INSERT INTO incidents (incident_id, order_id, severity, category, opened_at, resolved_at) VALUES
  ('INC-9001', 'ORD-102', 'P1', 'payment_gateway', '2026-02-03T08:35:00Z', NULL),
  ('INC-9002', 'ORD-104', 'P2', 'carrier_misroute', '2026-02-06T01:00:00Z', '2026-02-06T03:10:00Z'),
  ('INC-9003', 'ORD-109', 'P2', 'pick_pack_error',  '2026-02-08T11:00:00Z', '2026-02-08T12:30:00Z'),
  ('INC-9004', 'ORD-106', 'P1', 'fraud_review',     '2026-02-06T16:00:00Z', NULL),
  ('INC-9005', 'ORD-105', 'P3', 'weather_hold',     '2026-02-07T00:15:00Z', '2026-02-07T02:00:00Z');

INSERT INTO support_cases (
  case_id, customer_id, order_id, priority, status, opened_at, customer_waiting_hours, last_update_hours
) VALUES
  ('CASE-778', 'C003', 'ORD-102', 'high',   'open', '2026-02-03T08:45:00Z', 26, 7),
  ('CASE-779', 'C001', 'ORD-109', 'medium', 'open', '2026-02-08T12:40:00Z', 10, 2),
  ('CASE-780', 'C002', 'ORD-106', 'high',   'open', '2026-02-06T16:10:00Z',  5, 1);

INSERT INTO oncall (team, primary_engineer, secondary_engineer) VALUES
  ('Strategic Accounts', 'Dana Li', 'Marco Weiss'),
  ('Commercial', 'Omar Santos', 'Lina Hoffmann'),
  ('SMB', 'Chloe Reed', 'Aaron Fox'),
  ('Platform Reliability', 'Nikhil Batra', 'Ivy Chen'),
  ('Fulfillment Operations', 'Rosa Kim', 'Ethan Cole');
