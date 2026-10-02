# Trust Boundaries

## Purpose

Trust boundaries define where identity, context, permissions, data classification and destinations must be re-evaluated.

A request crossing a boundary is not automatically trusted because an earlier control succeeded.

## Boundary Model

| Boundary | Trusted Side | Untrusted or Restricted Side | Required Control |
|---|---|---|---|
| User to agent | Authenticated business context | Unverified request intent | Identity and purpose validation |
| Agent to gateway | Registered agent profile | Unknown or expired agent | Agent trust evaluation |
| Context to policy engine | Approved system context | External documents or instructions | Context validation |
| Agent to tool | Approved tool scope | Unlisted or high-risk tool | Tool allowlist and approval |
| Agent to data | Authorized classification and department | Restricted or unrelated data | Least-privilege access |
| Data to output | Sanitized result | Sensitive or restricted fields | DLP and masking |
| Application to destination | Approved internal destination | External or untrusted endpoint | Egress control |
| Decision to audit | Structured decision event | Missing or incomplete evidence | Audit completeness check |

## Trust Attributes

The decision engine may consider:

- agent identity;
- agent origin;
- owner and department;
- trust state;
- requested tool;
- requested data classification;
- request volume;
- destination;
- session history;
- previous violations;
- masking availability;
- approval requirement;
- policy version.

## Boundary Principles

A valid identity does not override:

- a data-classification restriction;
- a tool restriction;
- a destination restriction;
- a behavioural-risk signal;
- a session restriction;
- a human-approval requirement.

## Re-evaluation Requirements

Controls should be re-evaluated when:

- the requested data scope changes;
- the requested tool changes;
- a new destination is introduced;
- the request volume increases;
- the session accumulates violations;
- the agent changes state;
- the output contains restricted fields;
- the policy version changes.

## Expected Outcomes

Crossing a trust boundary may result in:

- `ALLOW`;
- `ALLOW_WITH_MASKING`;
- `LIMIT`;
- `HUMAN_APPROVAL`;
- `BLOCK`;
- incident creation.

## Governance Responsibility

The owner of each boundary must define:

- the allowed actors;
- the allowed data;
- the allowed tools;
- the permitted destinations;
- the required evidence;
- the escalation path;
- the review frequency.
