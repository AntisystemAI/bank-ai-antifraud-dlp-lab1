from __future__ import annotations

import sys
from pathlib import Path


# При прямом запуске:
# python scripts/run_demo.py
# Python добавляет в sys.path папку scripts, но не корень проекта.
# Поэтому добавляем корень репозитория до импорта пакета src.
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from src.configuration.app_settings import settings
from src.policies.policy_loader import load_security_policy
from src.scenarios.catalog import (
    SCENARIOS,
    get_scenario_request,
)
from src.security.security_engine import SecurityEngine
from src.services.security_service import SecurityService
from src.storage.decision_repository import DecisionRepository


policy = load_security_policy(
    ROOT / settings.security_policy_path
)

engine = SecurityEngine(policy)

repository = DecisionRepository(
    settings.postgres_dsn
)

service = SecurityService(
    engine=engine,
    repository=repository,
    persist_decisions=settings.persist_decisions,
)


def main() -> None:
    print("=" * 86)
    print("BANK AI ANTIFRAUD DLP LAB — MVP DEMO")
    print("=" * 86)
    print(
        "Сохранение решений: "
        f"{'PostgreSQL' if settings.persist_decisions else 'отключено'}"
    )

    passed = 0

    for scenario_id, scenario in SCENARIOS.items():
        request = get_scenario_request(scenario_id)
        decision = service.evaluate(request)

        expected = scenario["expected"]
        success = decision.decision == expected

        if success:
            passed += 1

        marker = "PASS" if success else "FAIL"

        print()
        print(f"[{marker}] {scenario_id}")
        print(f"Описание: {scenario['description']}")
        print(f"Ожидалось: {expected.value}")
        print(f"Получено:  {decision.decision.value}")
        print(f"Risk score: {decision.risk_score}")
        print(f"Risk level: {decision.risk_level.value}")
        print(
            "Reason codes: "
            + ", ".join(decision.reason_codes)
        )

        if decision.incident_id:
            print(f"Incident: {decision.incident_id}")

    print()
    print("=" * 86)
    print(
        f"Результат: {passed}/{len(SCENARIOS)} "
        "сценариев пройдено"
    )
    print("=" * 86)

    if passed != len(SCENARIOS):
        raise SystemExit(1)


if __name__ == "__main__":
    main()