# Banking AI Antifraud & Data Loss Prevention Lab

## Executive Summary

Portfolio MVP demonstrating a policy-controlled security architecture for protecting synthetic banking transaction data from internal and external AI-agent risks.

The project combines antifraud analytics, data-loss prevention, identity and access control, tool governance, egress protection, auditability and incident response into one eight-layer control model.

This portfolio case connects business risk, operating model, security controls, measurable outcomes and implementation governance.

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
