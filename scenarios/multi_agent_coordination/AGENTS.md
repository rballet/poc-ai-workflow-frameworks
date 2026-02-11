# Multi-Agent Coordination Scenario

Multi-agent incident response requiring coordination across infrastructure, security, and operations specialists.

## Overview
- Scenario type: `multi_agent_coordination`
- Profile: `multi_agent_coordination` (agent coverage, coordination success metrics)
- Questions require synthesizing evidence from multiple specialist domains
- Tests native multi-agent orchestration primitives per framework

## Specialist Domains

- **Infrastructure**: servers, clusters, deploys, service dependencies (SQL)
- **Security**: vulnerability scans, access logs, firewall rules (SQL)
- **Runbook**: change management policy, incident response procedures, compliance (markdown docs)

## Assets
- `spec.yaml` — scenario config with baseline (single-agent) and capability (multi-agent) modes
- `questions.yaml` — 10 questions: 3 easy (single-domain), 3 coordination (two-domain), 4 hard coordination (all three domains)
- `data/seed.sql` — 9 tables with two embedded incident storylines
- `documents/` — 4 policy documents (change management, incident response, security compliance, service catalog)
- `AGENTS.md` — this file

## Configuration (spec.yaml)
- Embedding: `text-embedding-3-small`
- LLM: `gpt-5-mini`
- Baseline mode: single agent, 3 tool calls max
- Capability mode: multi-agent, 15 tool calls / 15 steps max
