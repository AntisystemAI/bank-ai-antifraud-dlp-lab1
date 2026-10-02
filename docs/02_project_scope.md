# Project Scope

## Purpose

This project demonstrates a policy-controlled security architecture for AI agents operating on synthetic banking transaction data.

The scope covers the translation of business risk into security controls, agent permissions, executable scenarios, audit evidence and measurable acceptance criteria.

## In Scope

- Synthetic customers, accounts and transactions.
- Fictional banking profiles.
- Internal and external AI-agent profiles.
- Identity and trust evaluation.
- Input and context validation.
- Tool permission control.
- Data-access control.
- Behavioural risk evaluation.
- DLP and sensitive-field masking.
- Outbound destination control.
- Audit records and incident creation.
- Human approval for elevated-risk requests.
- REST API and interactive dashboard.
- Docker-compatible deployment.
- Optional PostgreSQL persistence.
- Automated tests and repeatable demonstration scenarios.

## Out of Scope

- Real banking systems.
- Real customer information.
- Real credentials or payment data.
- Execution of financial transactions.
- Production IAM integration.
- Production fraud operations.
- Connection to any specific bank.
- Regulatory certification.
- Replacement of an enterprise SOC, DLP or fraud platform.

## Primary Stakeholders

| Stakeholder | Responsibility |
|---|---|
| Business owner | Defines the legitimate business purpose and acceptable risk |
| Data owner | Approves data classification, access scope and retention requirements |
| Security owner | Maintains control objectives, policies and risk thresholds |
| AI-agent owner | Ensures that the agent operates within its approved purpose |
| Engineering team | Implements the API, policy engine and deployment |
| Incident analyst | Investigates blocked events and reconstructs evidence |
| Executive reviewer | Assesses risk posture, outcomes and limitations |

## Deliverables

- Eight-layer security architecture.
- Fictional AI-agent permission model.
- Threat and trust-boundary analysis.
- Synthetic data governance model.
- Executable policy evaluation engine.
- Repeatable security scenario catalogue.
- Audit and incident model.
- Public dashboard and API documentation.
- Automated test validation.
- Documented limitations and implementation roadmap.

## Acceptance Boundary

The MVP is successful when a request can be evaluated, assigned a decision, explained with reason codes, recorded for audit and escalated to an incident or human approval when required.

## Success Criteria

The project scope is considered covered when:

- the business problem is clearly defined;
- the security architecture is documented;
- the eight control layers are described;
- AI-agent permissions are explicit;
- security scenarios are repeatable;
- decisions include explainable reason codes;
- high-risk requests can require human approval;
- critical events can create incidents;
- the public demonstration uses synthetic data only;
- the deployment does not require integration with a real banking system.
