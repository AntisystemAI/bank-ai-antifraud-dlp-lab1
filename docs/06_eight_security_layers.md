# Eight Security Layers

## Control Model

The eight layers form a defence-in-depth model. Each layer addresses a different failure mode in an AI-enabled banking workflow.

The layers are evaluated as part of one policy-controlled decision process. The final decision may be affected by one or more triggered controls.

## Layer Catalogue

| Layer | Name | Objective | Example Control |
|---|---|---|---|
| 1 | Identity and Trust | Establish whether the actor and agent are trusted | Agent profile, origin, owner and trust state |
| 2 | Input and Context Control | Detect unsafe or manipulated instructions | Untrusted-context and policy-bypass detection |
| 3 | Tool Access Control | Restrict tools available to an agent | Tool allowlist and elevated-tool approval |
| 4 | Data Access Control | Enforce least-privilege access | Role, department, classification and scope checks |
| 5 | Transaction Risk | Detect abnormal request behaviour | Volume, frequency, fragmentation and session risk |
| 6 | DLP and Masking | Prevent exposure of sensitive fields | Restricted-field detection and sanitization |
| 7 | Egress Control | Control where information can be sent | Destination validation and export blocking |
| 8 | Monitoring and Response | Make decisions observable and actionable | Audit, incidents, containment and review |

## Layer 1: Identity and Trust

This layer evaluates:

- agent identity;
- agent type;
- owner;
- department;
- origin;
- trust state;
- session validity.

A valid identity does not automatically grant access to all data or tools.

## Layer 2: Input and Context Control

This layer evaluates:

- request purpose;
- untrusted instructions;
- conflicting document content;
- attempts to bypass policy;
- suspicious context supplied by an external source.

## Layer 3: Tool Access Control

This layer evaluates:

- requested tool;
- agent allowlist;
- tool sensitivity;
- tool ownership;
- approval requirement;
- tool invocation frequency.

## Layer 4: Data Access Control

This layer evaluates:

- data classification;
- department ownership;
- requested scope;
- record volume;
- role permissions;
- purpose limitation.

## Layer 5: Transaction Risk

This layer evaluates:

- transaction amount;
- request frequency;
- repeated access;
- abnormal volume;
- fragmented collection;
- session history;
- previous policy violations.

## Layer 6: DLP and Masking

This layer evaluates:

- sensitive field presence;
- restricted identifiers;
- account information;
- transaction details;
- masking availability;
- output classification.

When policy allows, a request may continue only after sensitive fields are masked.

## Layer 7: Egress Control

This layer evaluates:

- destination;
- channel;
- recipient;
- external or internal classification;
- export volume;
- restricted data in the outgoing payload.

## Layer 8: Monitoring and Response

This layer provides:

- decision logging;
- reason codes;
- incident creation;
- session restriction;
- escalation;
- audit reconstruction;
- operational metrics.

## Control Outcomes

The layers support the following outcomes:

- permit a low-risk request;
- permit a request after masking;
- restrict volume or scope;
- require human approval;
- block the request;
- create a synthetic security incident.

## Implementation Note

The policy engine, scenario catalogue and API responses provide implementation evidence for the MVP.

The documentation describes the target control model, governance interpretation and expected operating behaviour.
