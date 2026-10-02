from __future__ import annotations
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from collections import Counter
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query

from src.api.dashboard import router as dashboard_router
from src.configuration.app_settings import settings
from src.domain.security_models import (
    AgentPublicProfile,
    RuntimeMetrics,
    ScenarioResult,
    SecurityDecision,
    SecurityRequest,
)
from src.policies.policy_loader import load_security_policy
from src.scenarios.catalog import (
    SCENARIOS,
    get_scenario_request,
)
from src.security.security_engine import SecurityEngine
from src.services.security_service import SecurityService
from src.storage.decision_repository import DecisionRepository


ROOT = Path(__file__).resolve().parents[2]

policy_path = ROOT / settings.security_policy_path
policy = load_security_policy(policy_path)

engine = SecurityEngine(policy)

repository = DecisionRepository(
    settings.postgres_dsn
)

security_service = SecurityService(
    engine=engine,
    repository=repository,
    persist_decisions=settings.persist_decisions,
)


OPENAPI_TAGS = [
    {
        "name": "System",
        "description": (
            "Состояние приложения, версия политики, "
            "режим хранения и доступность PostgreSQL."
        ),
    },
    {
        "name": "Dashboard",
        "description": (
            "Локальный интерфейс демонстрации результатов "
            "работы восьми слоёв защиты."
        ),
    },
    {
        "name": "Agents",
        "description": (
            "Реестр внутренних и внешних демонстрационных "
            "AI-агентов и их разрешений."
        ),
    },
    {
        "name": "Decision Engine",
        "description": (
            "Проверка произвольного синтетического запроса "
            "восьмислойным Policy Engine."
        ),
    },
    {
        "name": "Scenarios",
        "description": (
            "Каталог и запуск одиннадцати воспроизводимых "
            "сценариев безопасности."
        ),
    },
    {
        "name": "Audit and Incidents",
        "description": (
            "Просмотр решений безопасности и автоматически "
            "созданных синтетических инцидентов."
        ),
    },
    {
        "name": "Metrics",
        "description": (
            "Агрегированные показатели решений, блокировок, "
            "маскирования и ручных согласований."
        ),
    },
]


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Учебный API восьмиуровневой защиты синтетических "
        "банковских данных и контроля внутренних и внешних "
        "AI-агентов.\n\n"
        "Каждый запрос проходит проверку идентичности, "
        "входного контекста, инструментов, доступа к данным, "
        "поведенческого риска, DLP, исходящего канала и "
        "механизмов реагирования.\n\n"
        "Все события и данные являются синтетическими."
    ),
    openapi_tags=OPENAPI_TAGS,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Bank AI Antifraud DLP Lab",
    },
    license_info={
        "name": "Educational portfolio project",
    },
)
_dashboard_route = next(
    route
    for route in dashboard_router.routes
    if getattr(route,"path",None) == "/dashboard"
)
app.add_api_route(
    "/dashboard",
    _dashboard_route.endpoint,
    methods=["GET"],
    response_class=HTMLResponse,
    include_in_schema=True,
    tags=["Dashboard"],
    summary="Интерактивная панель мониторинга",
    description=(
        "Веб-интерфейс для запуска демонстрационных "
        "сценариев и просмотра метрик безопасности."
    ),
)






@app.get(
    "/",
    tags=["System"],
    summary="Информация о приложении",
    description=(
        "Возвращает название, версию и ссылки на основные "
        "интерфейсы демонстрационного приложения."
    ),
)
def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "dashboard": "/dashboard",
        "swagger": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/health",
        "agents": "/v1/agents",
        "scenarios": "/v1/scenarios",
        "evaluate": "/v1/security/evaluate",
        "demo": "/v1/demo/run-all",
        "audit": "/v1/audit",
        "incidents": "/v1/incidents",
        "metrics": "/v1/metrics",
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Проверить состояние приложения",
    description=(
        "Проверяет загрузку политики, количество агентов "
        "и сценариев. Если сохранение включено, дополнительно "
        "проверяет доступность PostgreSQL."
    ),
)
def health() -> dict[str, Any]:
    database_status = "disabled"

    if settings.persist_decisions:
        try:
            database_status = (
                "connected"
                if repository.healthcheck()
                else "unavailable"
            )
        except Exception:
            database_status = "unavailable"

    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.app_version,
        "policy_version": policy["policy_version"],
        "agents_loaded": len(policy["agents"]),
        "scenarios_loaded": len(SCENARIOS),
        "persistence_enabled": settings.persist_decisions,
        "database_status": database_status,
        "synthetic_environment": True,
    }


@app.get(
    "/v1/agents",
    response_model=list[AgentPublicProfile],
    tags=["Agents"],
    summary="Получить профили AI-агентов",
    description=(
        "Возвращает публичную конфигурацию пяти "
        "демонстрационных AI-агентов."
    ),
)
def list_agents() -> list[AgentPublicProfile]:
    profiles: list[AgentPublicProfile] = []

    for agent_id, agent in policy["agents"].items():
        profiles.append(
            AgentPublicProfile(
                agent_id=agent_id,
                name=agent["name"],
                agent_type=agent["agent_type"],
                owner_department=agent[
                    "owner_department"
                ],
                trust_level=agent["trust_level"],
                permission_profile=agent[
                    "permission_profile"
                ],
                maximum_classification=agent[
                    "maximum_classification"
                ],
                status=agent["status"],
                allowed_tools=agent["allowed_tools"],
                allowed_destinations=agent[
                    "allowed_destinations"
                ],
            )
        )

    return profiles


@app.post(
    "/v1/security/evaluate",
    response_model=SecurityDecision,
    tags=["Decision Engine"],
    summary="Проверить запрос восьмислойным движком",
    description=(
        "Принимает синтетический запрос сотрудника или "
        "AI-агента, выполняет восемь слоёв проверки и "
        "возвращает risk score, reason codes и итоговое "
        "решение."
    ),
    responses={
        400: {
            "description": (
                "Некорректный или несинтетический запрос."
            ),
        },
        503: {
            "description": (
                "Ошибка проверки или сохранения решения."
            ),
        },
    },
)
def evaluate_security_request(
    request: SecurityRequest,
) -> SecurityDecision:
    try:
        return security_service.evaluate(request)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Security evaluation or persistence failed: "
                f"{type(error).__name__}"
            ),
        ) from error


@app.get(
    "/v1/scenarios",
    tags=["Scenarios"],
    summary="Получить каталог сценариев",
    description=(
        "Возвращает идентификатор, категорию, описание "
        "и ожидаемое решение каждого сценария."
    ),
)
def list_scenarios() -> list[dict[str, str]]:
    return [
        {
            "scenario_id": scenario_id,
            "category": scenario["category"],
            "description": scenario["description"],
            "expected_decision": (
                scenario["expected"].value
            ),
        }
        for scenario_id, scenario in SCENARIOS.items()
    ]


def execute_scenario(
    scenario_id: str,
) -> ScenarioResult:
    """
    Выполняет один сценарий и возвращает унифицированный
    результат для одиночного и массового запуска.
    """
    if scenario_id not in SCENARIOS:
        raise HTTPException(
            status_code=404,
            detail=f"Scenario not found: {scenario_id}",
        )

    scenario = SCENARIOS[scenario_id]
    request = get_scenario_request(scenario_id)

    try:
        decision = security_service.evaluate(request)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Scenario evaluation failed: "
                f"{type(error).__name__}"
            ),
        ) from error

    expected = scenario["expected"]

    return ScenarioResult(
        scenario_id=scenario_id,
        description=scenario["description"],
        expected_decision=expected,
        actual_decision=decision.decision,
        passed=decision.decision == expected,
        decision=decision,
    )


@app.post(
    "/v1/scenarios/{scenario_id}/run",
    response_model=ScenarioResult,
    tags=["Scenarios"],
    summary="Запустить один сценарий",
    description=(
        "Выполняет выбранный сценарий и сравнивает "
        "фактическое решение с ожидаемым."
    ),
    responses={
        404: {
            "description": "Сценарий не найден.",
        },
        503: {
            "description": (
                "Ошибка выполнения или сохранения сценария."
            ),
        },
    },
)
def run_scenario(
    scenario_id: str,
) -> ScenarioResult:
    return execute_scenario(scenario_id)


@app.post(
    "/v1/demo/run-all",
    tags=["Scenarios"],
    summary="Запустить все демонстрационные сценарии",
    description=(
        "Последовательно выполняет все одиннадцать "
        "сценариев и возвращает общий результат."
    ),
)
def run_all_scenarios() -> dict[str, Any]:
    results: list[ScenarioResult] = []

    for scenario_id in SCENARIOS:
        results.append(
            execute_scenario(scenario_id)
        )

    passed_count = sum(
        1 for result in results if result.passed
    )

    total = len(results)
    failed_count = total - passed_count

    return {
        "status": (
            "PASSED"
            if failed_count == 0
            else "FAILED"
        ),
        "total": total,
        "passed": passed_count,
        "failed": failed_count,
        "results": results,
    }


@app.get(
    "/v1/audit",
    tags=["Audit and Incidents"],
    summary="Получить журнал решений",
    description=(
        "Возвращает последние решения из PostgreSQL "
        "или временного хранилища."
    ),
)
def get_audit(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
        description=(
            "Максимальное количество последних решений."
        ),
    ),
) -> list[dict[str, Any]]:
    try:
        return security_service.list_decisions(limit)

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Audit storage is unavailable: "
                f"{type(error).__name__}"
            ),
        ) from error


@app.get(
    "/v1/incidents",
    tags=["Audit and Incidents"],
    summary="Получить журнал инцидентов",
    description=(
        "Возвращает последние синтетические инциденты, "
        "созданные для решений BLOCK."
    ),
)
def get_incidents(
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
        description=(
            "Максимальное количество последних инцидентов."
        ),
    ),
) -> list[dict[str, Any]]:
    try:
        return security_service.list_incidents(limit)

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Incident storage is unavailable: "
                f"{type(error).__name__}"
            ),
        ) from error


@app.get(
    "/v1/metrics",
    response_model=RuntimeMetrics,
    tags=["Metrics"],
    summary="Получить агрегированные метрики",
    description=(
        "Подсчитывает решения, блокировки, инциденты, "
        "ручные согласования, маскирование и ограничения."
    ),
)
def get_metrics() -> RuntimeMetrics:
    try:
        decisions = security_service.list_decisions(10000)
        incidents = security_service.list_incidents(10000)

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=(
                "Metrics storage is unavailable: "
                f"{type(error).__name__}"
            ),
        ) from error

    decision_values: list[str] = []

    for record in decisions:
        value = (
            record.get("final_decision")
            or record.get("decision")
        )

        if value is None:
            continue

        normalized_value = getattr(
            value,
            "value",
            value,
        )

        decision_values.append(
            str(normalized_value)
        )

    counts = Counter(decision_values)

    return RuntimeMetrics(
        total_decisions=len(decision_values),
        decision_counts=dict(counts),
        total_incidents=len(incidents),
        blocked_requests=counts.get(
            "BLOCK",
            0,
        ),
        approval_requests=counts.get(
            "HUMAN_APPROVAL",
            0,
        ),
        masked_responses=counts.get(
            "ALLOW_WITH_MASKING",
            0,
        ),
        limited_responses=counts.get(
            "LIMIT",
            0,
        ),
    )