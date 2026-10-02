from pathlib import Path

import pytest

from src.policies.policy_loader import (
    load_security_policy,
)
from src.scenarios.catalog import (
    SCENARIOS,
    get_scenario_request,
)
from src.security.security_engine import SecurityEngine


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def engine() -> SecurityEngine:
    policy = load_security_policy(
        ROOT / "config" / "security_policy.yml"
    )
    return SecurityEngine(policy)


@pytest.mark.parametrize(
    "scenario_id",
    list(SCENARIOS.keys()),
)
def test_scenario_decision(
    engine: SecurityEngine,
    scenario_id: str,
) -> None:
    scenario = SCENARIOS[scenario_id]
    request = get_scenario_request(scenario_id)

    decision = engine.evaluate(request)

    assert decision.decision == scenario["expected"]
    assert 0 <= decision.risk_score <= 100
    assert len(decision.layers) == 8
    assert decision.reason_codes
    assert decision.policy_version == "1.0.0"
    assert decision.is_synthetic is True


def test_all_eight_layers_are_executed(
    engine: SecurityEngine,
) -> None:
    request = get_scenario_request(
        "aggregated_report"
    )

    decision = engine.evaluate(request)

    assert [
        result.layer_number
        for result in decision.layers
    ] == [1, 2, 3, 4, 5, 6, 7, 8]


def test_block_creates_incident(
    engine: SecurityEngine,
) -> None:
    request = get_scenario_request(
        "combined_incident"
    )

    decision = engine.evaluate(request)

    assert decision.decision.value == "BLOCK"
    assert decision.incident_created is True
    assert decision.incident_id is not None


def test_allow_does_not_create_incident(
    engine: SecurityEngine,
) -> None:
    request = get_scenario_request(
        "aggregated_report"
    )

    decision = engine.evaluate(request)

    assert decision.decision.value == "ALLOW"
    assert decision.incident_created is False
    assert decision.incident_id is None


def test_raw_request_text_is_not_in_decision(
    engine: SecurityEngine,
) -> None:
    request = get_scenario_request(
        "combined_incident"
    )

    request.request_text = (
        "SYNTHETIC_SECRET_MUST_NOT_BE_LOGGED"
    )

    decision = engine.evaluate(request)
    serialized = decision.model_dump_json()

    assert (
        "SYNTHETIC_SECRET_MUST_NOT_BE_LOGGED"
        not in serialized
    )