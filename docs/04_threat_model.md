# Threat Model

## Objective

The threat model identifies how an AI-enabled banking workflow could misuse synthetic transaction data, internal tools or outbound channels.

This is an independent portfolio threat model. It does not represent the internal threat model of any real financial institution.

## Protected Assets

- synthetic customer records;
- synthetic account and transaction records;
- restricted transaction fields;
- fictional employee and department information;
- analytical reports;
- AI-agent permissions;
- internal tool definitions;
- security decisions;
- audit records;
- incident evidence;
- approval state;
- session history.

## Threat Actors

| Actor | Description |
|---|---|
| Misconfigured internal agent | Trusted agent with excessive or incorrect permissions |
| Compromised session | Valid session used for abnormal activity |
| Untrusted external agent | External actor attempting to reach internal data or tools |
| Malicious document source | Content containing instructions that conflict with policy |
| Over-privileged user | User requesting data outside the approved business purpose |
| Fragmented collector | Actor making small requests to bypass volume controls |
| Unapproved tool caller | Agent attempting to invoke a tool outside its permission set |

## Threat Scenarios

| Threat | Potential Impact | Primary Controls |
|---|---|---|
| Excessive data retrieval | Unnecessary exposure of records | Volume limits and risk scoring |
| Cross-department access | Unauthorized data access | Role and department checks |
| External export | Disclosure to an untrusted destination | DLP and egress control |
| Unauthorized tool call | Action outside agent scope | Tool allowlist and approval |
| Prompt or policy bypass | Control evasion | Input and context control |
| Restricted-field access | Exposure of classified data | Classification and masking |
| Repeated violations | Escalation from isolated misuse | Session risk and incident creation |
| Fragmented collection | Bypass of per-request limits | Behavioural monitoring |
| Untrusted context | Unsafe instructions influence a workflow | Context validation |
| Missing audit evidence | Inability to reconstruct an event | Monitoring and response controls |

## Security Objectives

The project aims to:

- prevent access outside the approved business purpose;
- reduce excessive data retrieval;
- prevent restricted data from reaching external destinations;
- limit tools available to each agent;
- detect repeated and abnormal behaviour;
- create explainable decisions;
- support human approval for elevated-risk requests;
- preserve evidence for review.

## Assumptions

- all business data is synthetic;
- agent permissions are explicitly defined;
- policies are versioned;
- security decisions are explainable;
- high-risk operations can be sent for human review;
- the public demonstration is not a production security boundary;
- the deployment does not have access to real bank systems.

## Risk Treatment

The MVP uses several complementary responses:

- prevention of unsafe activity;
- restriction of excessive activity;
- masking of sensitive fields;
- escalation to human approval;
- creation of synthetic incidents;
- recording of decisions and reason codes;
- review of repeated violations.

## Residual Risk

Residual risks remain because this project does not include:

- production identity federation;
- real-time fraud data;
- enterprise DLP integration;
- live SOC orchestration;
- regulatory validation;
- production-scale load testing;
- formally calibrated risk thresholds.
