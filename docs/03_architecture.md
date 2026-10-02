# Architecture

## Architectural Objective

The architecture places a policy decision point between an AI agent and protected synthetic banking data or tools.

The agent does not receive unrestricted access to data, tools or outbound destinations. Each request is evaluated against applicable security controls before execution.

## Logical Flow
```mermaid
flowchart LR
    U[Business Request] --&gt; A[AI Agent]
    A --&gt; G[Agent Gateway]
    G --&gt; P[Policy Engine]
    P --&gt; L[Eight Security Layers]
    L --&gt; D[Decision Engine]

    D --&gt;|ALLOW| X[Execute Request]
    D --&gt;|ALLOW_WITH_MASKING| M[Sanitize and Execute]
    D --&gt;|LIMIT| R[Execute Within Limits]
    D --&gt;|HUMAN_APPROVAL| H[Human Review]
    D --&gt;|BLOCK| B[Block and Create Incident]

    D --&gt; Q[Audit and Metrics]

```
## Reference Components
| Component | Responsibility |
|---|---|
| FastAPI application | Exposes health, evaluation, scenario, audit, incident and metrics endpoints |
| Agent registry | Stores fictional agent profiles and trust attributes |
| Policy loader | Loads versioned policies and classification rules |
| Security engine | Evaluates requests against the security control model |
| Decision engine | Produces the final decision, risk score and reason codes |
| Scenario catalogue | Provides repeatable security demonstrations |
| Decision repository | Persists decisions when database mode is enabled |
| Incident repository | Stores synthetic incidents when persistence is enabled |
| Dashboard | Presents runtime status, agents, scenarios and metrics |
| PostgreSQL | Provides optional persistence and audit storage |
| GitHub Actions | Runs automated validation |
| Docker | Provides reproducible packaging and deployment |

##Request Processing
A request follows these logical stages:
Receive the business request and agent context.
Identify the agent, owner, role and trust state.
Validate the input and external context.
Check the requested tool against the agent allowlist.
Evaluate data scope, classification and volume.
Calculate behavioural and transaction risk.
Detect sensitive fields and determine whether masking is possible.
Validate the destination and egress channel.
Produce a final decision and reason codes.
Create audit evidence and an incident when required.

## Decision Outputs
A decision may contain:
final decision;
risk score;
risk level;
reason codes;
triggered control layers;
policy version;
audit metadata;
incident identifier when required.
## Runtime Modes
The project supports two demonstration modes:
Runtime-only mode for a lightweight public deployment.
PostgreSQL-backed mode for local persistence and audit demonstrations.
The public deployment may use runtime-only storage. Runtime records must not be presented as a permanent compliance archive.
## Design Principles
The architecture follows these principles:
least privilege;
deny by default for unapproved access;
separation of duties;
explainable decisions;
defence in depth;
human approval for elevated-risk operations;
synthetic data by default;
auditable control outcomes.
Authentication alone is not sufficient for approval. The request purpose, agent permissions, data classification, volume, destination and session behaviour must also be evaluated.
