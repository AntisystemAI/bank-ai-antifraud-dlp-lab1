# Business Problem

AI agents in banking workflows can process transaction data, generate reports, work with documents and invoke internal tools.

An employee mistake, incorrect agent configuration or untrusted external request may lead to unauthorized access, excessive data extraction or disclosure of sensitive information.

## Objective

The objective of this project is to design an eight-layer security architecture that evaluates:

- user and agent identity;
- request content and context;
- tool permissions;
- data access scope;
- transaction risk;
- sensitive-data presence;
- destination and data-transfer direction;
- post-event system behavior.

## Business Risks

Without policy-controlled access, an AI-enabled banking workflow may create the following risks:

- excessive retrieval of transaction records;
- access to data outside the agent's department;
- unauthorized invocation of internal tools;
- exposure of restricted fields;
- export of sensitive data to external destinations;
- fragmented data collection used to bypass volume limits;
- repeated policy violations without escalation;
- incomplete audit evidence;
- delayed incident response.

## Protected Assets

The project uses synthetic data to represent:

- customer records;
- account records;
- transaction records;
- antifraud reports;
- investigation results;
- employee profiles;
- AI-agent activity logs;
- internal tool-call parameters;
- synthetic documents;
- fictional control markers;
- security decisions and incidents.

## Out of Scope

The project does not include:

- real banking integrations;
- interaction with real accounts;
- execution of financial operations;
- real personal data;
- internal systems of any specific bank;
- production banking infrastructure;
- live customer activity;
- real credentials, tokens or private endpoints.

## Expected Business Value

The proposed architecture is intended to:

- reduce unauthorized data access;
- enforce least-privilege principles;
- make AI-agent decisions explainable;
- prevent unsafe data exports;
- support human approval for high-risk requests;
- provide auditable evidence for investigations;
- connect technical controls with measurable business risk.

## Success Criteria

The project is considered successful when:

- legitimate low-risk requests can be processed;
- prohibited requests are blocked;
- sensitive fields can be masked;
- high-risk requests can require human approval;
- repeated violations increase session risk;
- critical events create incidents;
- decisions and incidents can be audited;
- the complete decision chain can be reconstructed;
- all test data remains synthetic.
