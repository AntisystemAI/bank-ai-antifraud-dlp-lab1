# Incident Response

## Purpose

The incident-response model defines how the platform should react when a security decision indicates critical or repeated risk.

The MVP creates synthetic incidents for applicable critical scenarios.

## Incident Severity

| Severity | Example | Expected Response |
|---|---|---|
| Low | Single low-impact policy warning | Record and monitor |
| Medium | Repeated violation or excessive request | Limit session and require review |
| High | Restricted-data request or unauthorized tool | Block, audit and investigate |
| Critical | External export combined with multiple violations | Block, create incident and contain session |

## Response Lifecycle

1. Detect the security event.
2. Evaluate the request through the policy engine.
3. Produce a decision, risk score and reason codes.
4. Block or restrict the unsafe operation.
5. Create an incident when the threshold is reached.
6. Preserve decision and session evidence.
7. Review the agent, user, destination and requested data.
8. Apply containment or permission changes.
9. Record the final disposition.
10. Use lessons learned to improve policies and scenarios.

## Incident Record

A synthetic incident should contain:

- incident identifier;
- timestamp;
- severity;
- agent identifier;
- request identifier;
- decision identifier;
- risk score;
- triggered reason codes;
- affected data classification;
- destination;
- containment status;
- investigation status;
- final disposition.

## Containment Actions

Possible actions include:

- block the current request;
- restrict the current session;
- require human approval;
- disable a tool for the agent;
- reduce the data-access scope;
- prevent external egress;
- flag the agent for investigation;
- increase monitoring.

## Investigation Questions

An analyst should determine:

- which agent initiated the request;
- who owns the agent;
- what data was requested;
- which tools were invoked;
- where the data was intended to go;
- which controls were triggered;
- whether similar requests occurred earlier;
- whether the agent permission matrix was violated;
- whether the policy requires an update.

## Auditability

The incident must be linked to the security decision that created it.

This allows an investigator to reconstruct the chain from:
```text
request
agent context
security controls
risk score
final decision
incident
containment action
final disposition
