# Agent Permission Matrix

## Purpose

This matrix defines the intended permission boundaries for the five fictional AI-agent profiles used by the demonstration.

The permissions are synthetic and do not represent the access model of any real bank.

## Permission Levels

| Level | Meaning |
|---|---|
| Public | Non-sensitive information and public knowledge |
| Confidential | Approved internal analytical information |
| Restricted | Security, audit or incident information |
| Prohibited | Access is not permitted |

## Agent Matrix

| Agent | Type | Business Purpose | Maximum Data Level | Approved Tools | External Egress | Human Approval |
|---|---|---|---|---|---|---|
| Internal Analyst Agent | Internal | Analyse synthetic transactions | Confidential | Transaction search, aggregation, risk analysis | No | Required for elevated scope |
| Internal Reporting Agent | Internal | Prepare internal reports | Confidential | Report generation, aggregation, masking | No | Required for restricted output |
| External Support Agent | External | Provide public support responses | Public | Public knowledge search, FAQ retrieval | Restricted | Required for non-public content |
| External RAG Agent | External | Retrieve public knowledge | Public | Public document retrieval | Restricted | Required for internal context |
| Security Control Agent | Internal control | Review security events | Restricted | Audit search, incident review, policy inspection | No | Required for control changes |

## General Rules

- Agents may access only data required for their approved purpose.
- An internal identity does not automatically permit restricted access.
- External agents must not access confidential or restricted banking data.
- Unapproved tools are denied.
- External destinations are evaluated before any release.
- Sensitive fields must be masked when policy allows a transformed response.
- High-risk requests are routed to human approval.
- Repeated violations increase session risk.
- Critical events create incidents.
- Decisions should include reason codes and policy version.

## Separation of Duties

The Security Control Agent may review security events but must not directly change production policy or approve its own elevated access.

The Reporting Agent may produce reports but must not independently export restricted data to an external destination.

The External Support Agent and External RAG Agent must remain limited to public information and approved public knowledge sources.

## Permission Review Triggers

The matrix should be reviewed when:

- a new agent is introduced;
- an agent receives a new tool;
- a new data classification is added;
- an external destination is approved;
- a scenario reveals a permission gap;
- an incident indicates excessive privilege;
- the business purpose of an agent changes;
- the policy version changes.

## Governance Owner

The AI-agent owner is responsible for confirming that each agent:

- has a documented business purpose;
- has an approved owner;
- uses only approved tools;
- accesses only the required data;
- has a defined escalation path;
- is reviewed after incidents or material changes.
