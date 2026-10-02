# Limitations

## Data Limitations

- All customers, accounts, employees, transactions and incidents are synthetic.
- The data does not represent real customer behaviour.
- The dataset is not statistically calibrated to a real bank.
- The project does not use real personal or payment information.
- The examples are intended for demonstration and testing.

## Security Limitations

- The MVP is not a complete enterprise security platform.
- Authentication and identity federation are represented conceptually.
- Production secrets management is not implemented.
- Network segmentation and private connectivity are outside the portfolio scope.
- The public deployment is not a regulated banking environment.
- Persistence may be disabled in the public demo.
- Dashboard access is intended for demonstration rather than production operations.
- No production security certification is claimed.

## Model Limitations

- The risk score is policy-based and demonstrational.
- The score is not a validated fraud model.
- Thresholds are not calibrated against production labels.
- False-positive and false-negative rates are not production estimates.
- Human approval is represented as a decision outcome rather than a complete workflow system.
- The project does not claim autonomous fraud investigation.

## Operational Limitations

- There is no real SOC integration.
- There is no production ticketing integration.
- There is no customer notification workflow.
- There is no regulatory reporting integration.
- Retention and deletion controls are demonstrated conceptually.
- Availability and disaster-recovery objectives are not claimed.
- Production support processes are outside the current scope.

## Deployment Limitations

The application is Docker-compatible and can run without a mandatory banking-system integration.

This makes the demonstration portable, but it does not establish production readiness.

The public Render deployment should be treated as a demonstration environment. It must not receive real personal data, real banking credentials or confidential company information.

## Security and Privacy Position

The project is an independent educational and portfolio implementation.

It is not connected to, endorsed by or operated for any real financial institution.

## Next Steps

Future work may include:

- stronger identity integration;
- policy administration UI;
- immutable audit storage;
- richer PostgreSQL reporting;
- approval workflow integration;
- external secret management;
- property-based testing;
- load and resilience testing;
- calibrated fraud and DLP evaluation;
- security review before any production use.

## Final Positioning

This project should be presented as an independent portfolio MVP demonstrating:

- architecture;
- governance;
- implementation discipline;
- testable security controls;
- risk-based decision-making;
- operational thinking.

It should not be presented as a deployed solution for any real financial institution.
