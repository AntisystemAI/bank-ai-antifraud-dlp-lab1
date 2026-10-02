
# Metrics

## Purpose

Metrics connect the security architecture with measurable outcomes.

The metrics in this project are intended for MVP validation, control review and portfolio demonstration. They are not regulatory evidence by themselves.

## Core Metrics

| Metric | Purpose |
|---|---|
| Scenario pass rate | Measures whether expected security behaviours are reproduced |
| Unauthorized request block rate | Measures whether prohibited activity is stopped |
| Human approval rate | Shows how often elevated-risk activity requires review |
| Sensitive-data masking rate | Measures protection of restricted fields |
| Repeated-violation detection rate | Measures behavioural monitoring effectiveness |
| External-export prevention rate | Measures egress-control effectiveness |
| Incident creation accuracy | Measures whether critical events generate incidents |
| Audit completeness | Measures whether the decision chain can be reconstructed |
| False-positive review rate | Identifies controls that may require tuning |
| Mean time to contain | Measures response speed after critical detection |
| Policy coverage | Shows which threat scenarios have executable tests |

## MVP Evidence

The public demonstration is expected to expose:

- application health;
- application version;
- policy version;
- loaded agent count;
- loaded scenario count;
- decision totals;
- decision distribution;
- incident totals;
- persistence status;
- synthetic-environment status.

## Scenario Metrics

The scenario suite should report:

- total scenario count;
- passed scenario count;
- failed scenario count;
- expected decision;
- actual decision;
- risk score;
- incident creation status;
- execution duration when available.

## Governance Metrics

Leadership review should consider:

- whether controls reduce unacceptable risk;
- whether false positives affect business usability;
- whether agent permissions remain appropriate;
- whether incidents reveal control gaps;
- whether approval volume is sustainable;
- whether audit evidence is complete;
- whether policy thresholds require recalibration.

## Metric Governance

Metrics should be reviewed when:

- a policy threshold changes;
- an agent receives a new permission;
- a new tool or destination is added;
- a scenario is added or removed;
- incidents reveal a control gap;
- false positives affect business usability;
- the runtime architecture changes.

## Limitations

Metrics from a synthetic demonstration cannot be interpreted as:

- production fraud-loss reduction;
- regulatory compliance;
- real customer-impact measurement;
- validated model performance;
- enterprise security effectiveness.
