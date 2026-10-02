# Banking AI Antifraud & Data Loss Prevention Lab

## Executive Summary

Portfolio MVP demonstrating a policy-controlled security architecture for protecting synthetic banking transaction data from internal and external AI-agent risks.

The project combines antifraud analytics, data-loss prevention, identity and access control, tool governance, egress protection, auditability and incident response into one eight-layer control model.

This portfolio case connects business risk, operating model, security controls, measurable outcomes and implementation governance.

## Quick Navigation

- [MVP Status](#mvp-status)
- [Demonstration Results](#demonstration-results)
- [Architecture](#architecture)
- [Eight Security Layers](#eight-security-layers)
- [Threat Model and Governance](#threat-model-and-governance)
- [Acceptance Criteria](#acceptance-criteria)
- [Documentation Map](#documentation-map)
- [Public Dashboard](https://bank-ai-antifraud-dlp-lab.onrender.com/dashboard)
- [Swagger API](https://bank-ai-antifraud-dlp-lab.onrender.com/docs)

## Leadership Scope

The project demonstrates capabilities in:

- defining a security strategy for AI-enabled banking workflows;
- translating business risks into control requirements;
- designing a target operating model for internal and external AI agents;
- establishing governance for access, data classification and outbound transfer;
- defining measurable acceptance criteria and security KPIs;
- coordinating architecture, data, engineering, testing and incident response;
- communicating technical risk to business and security stakeholders.

This is an independent portfolio project based on synthetic data and fictional banking profiles. It does not represent the internal architecture, policies or systems of any real financial institution.

## Project Positioning

This project demonstrates how a banking security initiative can be translated from business risk into an operating model, control architecture, implementation backlog, test scenarios and measurable acceptance criteria.

The focus is not only on individual security mechanisms, but on the governance model required to control AI-enabled workflows involving sensitive transaction data.

## Business Outcomes

The target outcomes of the project are:

- reduce unauthorized access to sensitive banking data;
- prevent excessive data retrieval by AI agents;
- enforce least-privilege access to tools and datasets;
- detect suspicious agent behavior and repeated policy violations;
- prevent sensitive data from reaching untrusted channels;
- provide complete auditability for security decisions;
- support human approval for high-risk operations;
- establish measurable criteria for control effectiveness.

## Scope of Responsibility

The portfolio case covers:

- business problem definition;
- target security architecture;
- threat and trust-boundary analysis;
- synthetic data governance;
- AI-agent permission design;
- eight-layer control model;
- policy and approval workflow;
- incident response model;
- testing and acceptance criteria;
- security and operational metrics;
- comparative assessment of two fictional banking profiles.

## MVP Status

**Status:** MVP implemented and publicly deployed as an independent portfolio demonstration.

| Capability | Current result |
|---|---|
| Security architecture | Eight-layer policy-controlled security model |
| Scenario validation | 11/11 scenarios passed |
| AI-agent governance | Five fictional agent profiles with permission boundaries |
| Risk evaluation | Risk score, risk level, reason codes and incident identifiers |
| Security decisions | `ALLOW`, `ALLOW_WITH_MASKING`, `LIMIT`, `HUMAN_APPROVAL`, `BLOCK` |
| API layer | FastAPI REST API with OpenAPI documentation |
| Interactive dashboard | Public security dashboard |
| API documentation | Swagger UI and ReDoc |
| Deployment | Docker-compatible application deployed on Render |
| Data model | Synthetic banking transactions and fictional bank profiles |
| Persistence | Optional PostgreSQL decision and audit storage |
| Automation | GitHub Actions workflow and automated validation |
| Repository status | Public GitHub repository with documented architecture and scenarios |

### Public Demo

- [Security Dashboard](https://bank-ai-antifraud-dlp-lab.onrender.com/dashboard)
- [Swagger API Documentation](https://bank-ai-antifraud-dlp-lab.onrender.com/docs)
- [ReDoc API Documentation](https://bank-ai-antifraud-dlp-lab.onrender.com/redoc)
- [Health Check](https://bank-ai-antifraud-dlp-lab.onrender.com/health)

### Demonstrated Controls

The MVP demonstrates policy enforcement for:

- excessive transaction-data requests;
- cross-department access attempts;
- repeated policy violations;
- external data-export attempts;
- unauthorized tool invocation;
- untrusted document context;
- fragmented data collection;
- restricted fields and classification boundaries;
- policy-bypass instructions;
- human approval for high-risk operations;
- incident creation for critical events.

The public demonstration uses synthetic data and fictional banking profiles. PostgreSQL persistence is implemented as an optional integration and may be disabled in the public demo configuration to keep the deployment portable.

## Demonstration Results

### Local MVP Validation

The local Docker environment was validated with PostgreSQL persistence enabled.

| Check | Result |
|---|---|
| Application health | `status: ok` |
| Application version | `0.3.0` |
| Security policy version | `1.0.0` |
| Loaded agents | 5 |
| Loaded scenarios | 11 |
| PostgreSQL persistence | Enabled |
| Database status | Connected |
| Scenario execution | 11/11 passed |
| Critical combined scenario | `BLOCK` |
| Critical risk score | 100 |
| Incident creation | Confirmed |
| Synthetic environment | Enabled |

### Decision Outcomes

The scenario suite validates the following policy outcomes:

| Decision | Demonstrated meaning |
|---|---|
| `ALLOW` | Low-risk request is permitted |
| `ALLOW_WITH_MASKING` | Request is permitted after sensitive fields are masked |
| `LIMIT` | Request is restricted by volume, scope or frequency |
| `HUMAN_APPROVAL` | Request requires review by an authorized person |
| `BLOCK` | Request is denied and may generate a security incident |

The combined incident scenario produced the following result:
```text
Scenario: combined_incident
Expected decision: BLOCK
Actual decision: BLOCK
Risk score: 100
Passed: true
Incident created: true

```
## Architecture

The platform implements a policy-controlled security architecture for AI agents operating on synthetic banking data.

The control model separates business intent, agent identity, data access, tool invocation, outbound transfer, risk evaluation, auditability and incident response.

### End-to-End Control Flow
```mermaid
flowchart LR
    A[Business Request] --&gt; B[AI Agent]
    B --&gt; C[Identity and Trust]
    C --&gt; D[Input and Context Control]
    D --&gt; E[Tool Access Control]
    E --&gt; F[Data Access Control]
    F --&gt; G[Behavioral Risk Evaluation]
    G --&gt; H[DLP and Masking]
    H --&gt; I[Egress Control]
    I --&gt; J[Decision Engine]
    J --&gt; K{Final Decision}
    K --&gt;|ALLOW| L[Execute Request]
    K --&gt;|ALLOW_WITH_MASKING| M[Execute Sanitized Request]
    K --&gt;|LIMIT| N[Execute Within Limits]
    K --&gt;|HUMAN_APPROVAL| O[Human Review]
    K --&gt;|BLOCK| P[Block and Create Incident]
    J --&gt; Q[Audit Record]
    P --&gt; R[Containment and Response]
```

### Security Decision Model
MVP Status The engine produces:

- final decision;
- risk score;
- risk level;
- reason codes;
- layer-by-layer results;
- policy version;
- audit metadata;
- incident identifier when required.

The supported decision types are:

| Decision | Meaning | Typical control outcome |
| --- | --- | --- |
| `ALLOW` | Request is permitted | Low-risk request within the approved scope |
| `ALLOW_WITH_MASKING` | Request is permitted after sanitization | Sensitive fields are masked before release |
| `LIMIT` | Request is permitted with restrictions | Data volume, scope or frequency is reduced |
| `HUMAN_APPROVAL` | Request requires a human decision | Context is untrusted or risk is elevated |
| `BLOCK` | Request is denied | Policy violation, unauthorized tool or unsafe destination |

### Implementation Status

| Area | Status |
|---|---|
| Eight-layer architecture | Implemented and documented |
| Agent profiles | Implemented |
| Scenario evaluation | Implemented |
| Risk scoring | Implemented |
| DLP and masking | Implemented |
| Egress control | Implemented |
| Incident creation | Implemented |
| PostgreSQL persistence | Optional integration |
| Public dashboard | Deployed |
| Real banking integration | Out of scope |
| Production readiness | Not claimed |

### Eight Security Layers

| Layer | Control objective | Example control |
| --- | --- | --- |
| 1. Identity and Trust | Establish whether the actor and agent are trusted | Agent profile, owner, origin and trust state |
| 2. Input and Context Control | Detect unsafe or manipulated instructions | Untrusted documents and policy-bypass detection |
| 3. Tool Access Control | Restrict which tools an agent may invoke | Tool allowlist and high-risk tool approval |
| 4. Data Access Control | Enforce least privilege over data | Role, department, classification and scope checks |
| 5. Behavioral Risk | Detect suspicious or abnormal behavior | Repeated violations, excessive volume and fragmentation |
| 6. DLP and Masking | Prevent exposure of sensitive fields | Restricted-field detection and masking |
| 7. Egress Control | Control where data may be sent | External destination and export restrictions |
| 8. Monitoring and Response | Make decisions observable and actionable | Audit records, incidents and containment actions |

### Trust Boundaries

The architecture distinguishes between:

- internal and external agents;
- trusted and untrusted context;
- approved and unapproved tools;
- authorized and unauthorized departments;
- synthetic and sensitive data classifications;
- internal and external destinations;
- normal and anomalous session behavior.

A request may pass one control and still be denied by a later layer. For example, an authenticated internal agent may still be blocked when it requests data from another department or attempts to export sensitive content externally.

### Control Plane and Data Plane

The **control plane** contains:

- agent profiles;
- access policies;
- data classifications;
- tool permissions;
- risk thresholds;
- approval rules;
- incident response actions;
- audit and metrics definitions.

The **data plane** contains:

- synthetic customers;
- accounts;
- transactions;
- employees;
- documents;
- agent events;
- tool calls;
- security decisions;
- security incidents.

This separation allows security policies to be reviewed and changed independently from the synthetic business data used by the demonstration.

### Reference Components

| Component | Responsibility |
| --- | --- |
| FastAPI API | Exposes health, agent, scenario, evaluation, audit, incident and metrics endpoints |
| Security Engine | Evaluates requests through the eight security layers |
| Policy Loader | Loads versioned security policies and classification rules |
| Scenario Catalog | Provides normal, suspicious and incident-oriented test cases |
| Decision Repository | Persists security decisions and incidents when PostgreSQL mode is enabled |
| Dashboard | Presents health, agents, scenarios, metrics and runtime results |
| PostgreSQL | Optional persistence layer for decisions, incidents and audit data |
| GitHub Actions | Validates syntax, tests, scenarios and required API routes |
| Docker | Packages the application for reproducible deployment |


## Threat Model and Governance

The project is designed around a governance model for AI-enabled workflows that process sensitive transaction data.

The objective is not only to block individual requests, but to establish accountable, measurable and reviewable controls for the complete agent lifecycle.

### Protected Assets

The security model protects:

- synthetic transaction records;
- customer and account identifiers;
- restricted transaction fields;
- employee and department information;
- analytical reports;
- internal tools and datasets;
- security decisions;
- audit records;
- incident evidence;
- temporary approvals and session state.

### Threat Scenarios

| Threat | Business risk | Primary controls |
|---|---|---|
| Excessive transaction-data request | Unnecessary exposure of sensitive records | Data-volume limits, masking and approval |
| Cross-department access attempt | Unauthorized access to another business area | Department scope and authorization checks |
| Repeated policy violations | Escalation from isolated misuse to coordinated abuse | Session risk, containment and incident creation |
| External data-export attempt | Sensitive information reaches an untrusted destination | Egress control, DLP and blocking |
| Unauthorized tool invocation | Agent performs an operation outside its permission scope | Tool allowlist and policy enforcement |
| Untrusted document context | External instructions influence a protected workflow | Context validation and human approval |
| Fragmented data collection | Small requests are combined to bypass volume controls | Behavioral analysis and repeated-violation detection |
| Restricted-field access | Classified fields are exposed without authorization | Classification checks and masking |
| Policy-bypass instruction | Agent attempts to override security controls | Instruction analysis and blocking |

### Governance Responsibilities

| Role | Responsibility |
|---|---|
| Business owner | Defines the legitimate business purpose and acceptable risk |
| Data owner | Approves data classification, access scope and retention requirements |
| Security owner | Maintains control objectives, risk thresholds and response rules |
| AI-agent owner | Ensures that the agent operates only within its approved purpose |
| Human approver | Reviews high-risk requests before execution |
| Incident analyst | Investigates blocked events and reconstructs the evidence chain |
| Platform owner | Maintains API, deployment, availability and technical controls |
| Auditor or reviewer | Verifies that decisions are explainable, traceable and policy-consistent |

### Risk Acceptance Model

A request must not be approved only because the agent is authenticated.

The final decision must consider:

- the identity and trust level of the agent;
- the business purpose of the request;
- the requested tool;
- the data classification;
- the requested volume;
- the destination;
- the current session history;
- previous policy violations;
- the availability of masking;
- the need for human approval.

High-risk activity must result in one of the following outcomes:

| Outcome | Governance meaning |
|---|---|
| Allow | The request is within the approved business and security scope |
| Allow with masking | The business purpose is valid, but sensitive fields must be protected |
| Limit | The request is valid only within a reduced volume or scope |
| Human approval | A responsible person must review the request before execution |
| Block | The request violates policy or exceeds the trust boundary |
| Contain | The session or agent requires additional investigation and restriction |

### Control Effectiveness Metrics

The portfolio evaluates control effectiveness through measurable indicators:

| Metric | Purpose |
|---|---|
| Unauthorized request block rate | Measures whether prohibited activity is stopped |
| Human approval rate | Shows how often elevated-risk activity requires review |
| Sensitive-data masking rate | Measures protection of restricted fields |
| Repeated-violation detection rate | Measures behavioral monitoring effectiveness |
| External-export prevention rate | Measures egress-control effectiveness |
| Incident creation accuracy | Measures whether critical events generate incidents |
| Audit completeness | Measures whether the decision chain can be reconstructed |
| False-positive review rate | Identifies controls that may require policy tuning |
| Mean time to contain | Measures response speed after critical detection |
| Policy coverage | Shows which threat scenarios are represented by executable tests |

### Evidence and Auditability

For every security decision, the system should make it possible to reconstruct:
```text
Who initiated the request
→ When the request occurred
→ Which agent processed it
→ Which tool was requested
→ Which data was requested
→ How many records were involved
→ Where the result was intended to go
→ Which security layer made the decision
→ Which policy rules were triggered
→ Whether data was masked
→ Whether an incident was created
→ What happened after the decision

```
## Acceptance Criteria

The MVP is considered functionally complete when:

- all eight security layers are represented in the architecture;
- every critical scenario has an expected decision;
- blocked requests return explainable reason codes;
- high-risk requests can require human approval;
- sensitive fields can be masked;
- external destinations are evaluated;
- repeated violations increase session risk;
- critical events create incidents;
- decisions and incidents can be audited;
- the complete decision chain can be reconstructed;
- the public demonstration uses synthetic data only;
- deployment can run without a mandatory banking-system integration.

## Documentation Map

### Business and Architecture

- [Business Problem](docs/01_business_problem.md)
- [Project Scope](docs/02_project_scope.md)
- [Architecture](docs/03_architecture.md)
- [Threat Model](docs/04_threat_model.md)
- [Trust Boundaries](docs/05_trust_boundaries.md)

### Security Controls

- [Eight Security Layers](docs/06_eight_security_layers.md)
- [Risk Scoring](docs/07_risk_scoring.md)
- [Incident Response](docs/08_incident_response.md)
- [Metrics](docs/09_metrics.md)
- [Limitations](docs/10_limitations.md)

### Agents and Testing

- [Agent Permission Matrix](agents/agent_permission_matrix.md)
- [Testing Directory](testing/)

### Project Governance

- [Project Roadmap](ROADMAP.md)
- [Disclaimer](DISCLAIMER.md)
