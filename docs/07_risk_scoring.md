# Risk Scoring

## Purpose

Risk scoring converts multiple security signals into an explainable decision input.

The score is a synthetic demonstration of policy-based risk aggregation. It is not a validated fraud model and must not be interpreted as a production fraud score.

## Risk Signals

The engine may consider:

- identity and trust state;
- untrusted input or document context;
- unauthorized tool request;
- requested data classification;
- requested record volume;
- cross-department access;
- external destination;
- repeated session violations;
- fragmented collection behaviour;
- availability of masking;
- need for human approval;
- previous incidents.

## Hard Policy Rules

Risk scoring should be interpreted together with hard policy rules.

A high score can support approval escalation or blocking. A hard policy violation can block a request even when other signals appear normal.

Examples of hard policy conditions include:

- prohibited agent access;
- prohibited tool invocation;
- external export of restricted data;
- invalid destination;
- missing approval for a critical operation;
- access outside the permitted department.

## Decision Outcomes

| Outcome | Meaning |
|---|---|
| `ALLOW` | Request is within the approved scope |
| `ALLOW_WITH_MASKING` | Request is allowed after sensitive fields are protected |
| `LIMIT` | Request is reduced by volume, scope or frequency |
| `HUMAN_APPROVAL` | An authorized person must review the request |
| `BLOCK` | Request violates policy or exceeds the trust boundary |

## Explainability Requirements

Each evaluated request should expose:

- final decision;
- risk score;
- risk level;
- reason codes;
- triggered control layers;
- policy version;
- audit metadata;
- incident identifier when applicable.

## Session Risk

Repeated violations should increase the risk associated with the current session.

Session-risk signals may include:

- repeated blocked requests;
- repeated attempts to access restricted data;
- repeated unapproved tool calls;
- repeated external-export attempts;
- fragmented requests designed to bypass a limit.

## Governance

Risk thresholds and policy rules must be reviewed when:

- scenario results change;
- false positives increase;
- new tools are introduced;
- data classifications change;
- a new outbound channel is approved;
- incident analysis identifies a control gap;
- agent permissions are expanded.

The active policy version returned by the API should be treated as the source of truth for each decision.

## Limitations

The risk score does not represent:

- real financial loss;
- customer impact;
- regulatory risk;
- a production fraud probability;
- a statistically calibrated model;
- a substitute for professional investigation.
