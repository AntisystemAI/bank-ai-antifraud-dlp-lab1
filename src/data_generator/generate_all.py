from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml


# Корневая папка репозитория.
ROOT_DIR = Path(__file__).resolve().parents[2]

# Папка, в которой будут создаваться полные CSV-файлы.
OUTPUT_DIR = ROOT_DIR / "datasets" / "generated"

# Версия генератора записывается в манифест.
DEFAULT_GENERATOR_VERSION = "1.0.0"


# Названия и порядок столбцов в CSV-файлах.
TABLE_COLUMNS: dict[str, list[str]] = {
    "customers": [
        "customer_id",
        "customer_segment",
        "age_group",
        "region",
        "risk_level",
        "kyc_status",
        "registration_date",
    ],
    "employees": [
        "employee_id",
        "department",
        "role",
        "access_level",
        "work_region",
        "status",
        "allowed_tools",
    ],
    "agents": [
        "agent_id",
        "agent_type",
        "owner_department",
        "trust_level",
        "permission_profile",
        "allowed_tools",
        "data_access_level",
        "status",
    ],
    "documents": [
        "document_id",
        "document_type",
        "classification",
        "source_trust",
        "owner_department",
        "contains_untrusted_instruction",
        "contains_synthetic_marker",
    ],
    "accounts": [
        "account_id",
        "customer_id",
        "account_type",
        "currency",
        "status",
        "daily_limit",
        "opening_date",
    ],
    "transactions": [
        "transaction_id",
        "account_id",
        "transaction_time",
        "amount",
        "currency",
        "channel",
        "merchant_category",
        "recipient_type",
        "device_id",
        "region",
        "risk_score",
        "fraud_label",
        "review_status",
    ],
    "agent_events": [
        "event_id",
        "session_id",
        "agent_id",
        "employee_id",
        "event_time",
        "action",
        "tool_name",
        "data_classification",
        "record_count",
        "destination",
        "policy_decision",
        "risk_score",
    ],
    "tool_calls": [
        "call_id",
        "agent_id",
        "tool_name",
        "requested_scope",
        "approved_scope",
        "records_requested",
        "decision",
        "reason",
        "timestamp",
    ],
    "incidents": [
        "incident_id",
        "incident_type",
        "severity",
        "source_agent",
        "detected_at",
        "affected_records",
        "blocked_layer",
        "containment_action",
        "status",
    ],
}


# Порядок создания и сохранения таблиц.
GENERATION_ORDER = [
    "customers",
    "employees",
    "agents",
    "documents",
    "accounts",
    "transactions",
    "agent_events",
    "tool_calls",
    "incidents",
]


def load_configuration(mode: str) -> dict[str, Any]:
    """
    Загружает конфигурацию маленького или полного режима.
    """

    config_path = ROOT_DIR / "config" / f"dataset_{mode}.yml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Не найден файл конфигурации: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        configuration = yaml.safe_load(file)

    if not isinstance(configuration, dict):
        raise ValueError(
            f"Конфигурация {config_path} должна содержать словарь параметров."
        )

    required_sections = {
        "mode",
        "seed",
        "date_range",
        "counts",
    }

    missing_sections = required_sections - set(configuration)

    if missing_sections:
        raise ValueError(
            "В конфигурации отсутствуют разделы: "
            f"{sorted(missing_sections)}"
        )

    required_counts = set(TABLE_COLUMNS)
    actual_counts = set(configuration["counts"])
    missing_counts = required_counts - actual_counts

    if missing_counts:
        raise ValueError(
            "В разделе counts отсутствуют таблицы: "
            f"{sorted(missing_counts)}"
        )

    return configuration


def parse_date(value: str | date) -> date:
    """
    Преобразует текстовую дату из YAML в объект date.
    """

    if isinstance(value, date):
        return value

    return date.fromisoformat(str(value))


def random_date(
    random_source: random.Random,
    start_date: date,
    end_date: date,
) -> date:
    """
    Возвращает случайную дату внутри разрешённого периода.
    """

    if start_date > end_date:
        raise ValueError(
            f"Начальная дата {start_date} позже конечной даты {end_date}."
        )

    total_days = (end_date - start_date).days

    return start_date + timedelta(
        days=random_source.randint(0, total_days)
    )


def random_datetime(
    random_source: random.Random,
    start_date: date,
    end_date: date,
) -> datetime:
    """
    Возвращает случайные дату и время в UTC.
    """

    if start_date > end_date:
        raise ValueError(
            f"Начальная дата {start_date} позже конечной даты {end_date}."
        )

    start_value = datetime.combine(
        start_date,
        time.min,
        tzinfo=timezone.utc,
    )

    end_value = datetime.combine(
        end_date,
        time.max,
        tzinfo=timezone.utc,
    )

    total_seconds = int(
        (end_value - start_value).total_seconds()
    )

    return start_value + timedelta(
        seconds=random_source.randint(0, total_seconds)
    )


def format_datetime(value: datetime) -> str:
    """
    Форматирует дату и время в ISO 8601 и UTC.
    """

    return (
        value.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def create_risk_score(
    random_source: random.Random,
) -> int:
    """
    Создаёт синтетический риск от 0 до 100.

    Большая часть событий получает низкий риск.
    """

    probability = random_source.random()

    if probability < 0.70:
        return random_source.randint(0, 29)

    if probability < 0.84:
        return random_source.randint(30, 44)

    if probability < 0.92:
        return random_source.randint(45, 59)

    if probability < 0.97:
        return random_source.randint(60, 69)

    if probability < 0.99:
        return random_source.randint(70, 84)

    return random_source.randint(85, 100)


def decision_from_risk(risk_score: int) -> str:
    """
    Преобразует оценку риска в решение политики.
    """

    if risk_score <= 29:
        return "allow"

    if risk_score <= 44:
        return "allow_with_masking"

    if risk_score <= 59:
        return "limit"

    if risk_score <= 69:
        return "require_approval"

    if risk_score <= 84:
        return "block"

    return "quarantine"


def create_file_hash(file_path: Path) -> str:
    """
    Рассчитывает SHA-256 созданного файла.
    """

    digest = hashlib.sha256()

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def write_csv(
    table_name: str,
    rows: list[dict[str, Any]],
) -> Path:
    """
    Сохраняет строки таблицы в CSV.
    """

    if table_name not in TABLE_COLUMNS:
        raise ValueError(
            f"Неизвестная таблица: {table_name}"
        )

    output_path = OUTPUT_DIR / f"{table_name}.csv"

    with output_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=TABLE_COLUMNS[table_name],
            extrasaction="raise",
        )

        writer.writeheader()
        writer.writerows(rows)

    return output_path


def generate_customers(
    random_source: random.Random,
    count: int,
    start_date: date,
    end_date: date,
) -> list[dict[str, Any]]:
    """
    Создаёт обезличенных синтетических клиентов.
    """

    segments = [
        "mass",
        "premium",
        "business",
        "private",
    ]

    age_groups = [
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65_plus",
    ]

    regions = [
        "central",
        "northwest",
        "south",
        "volga",
        "ural",
        "siberia",
        "far_east",
    ]

    rows: list[dict[str, Any]] = []

    for number in range(1, count + 1):
        customer_risk = random_source.choices(
            ["low", "medium", "high"],
            weights=[70, 25, 5],
            k=1,
        )[0]

        if customer_risk == "low":
            kyc_status = random_source.choices(
                ["verified", "pending"],
                weights=[95, 5],
                k=1,
            )[0]

        elif customer_risk == "medium":
            kyc_status = random_source.choices(
                [
                    "verified",
                    "pending",
                    "restricted",
                    "expired",
                ],
                weights=[65, 20, 5, 10],
                k=1,
            )[0]

        else:
            kyc_status = random_source.choices(
                [
                    "verified",
                    "pending",
                    "restricted",
                    "expired",
                ],
                weights=[25, 20, 40, 15],
                k=1,
            )[0]

        rows.append(
            {
                "customer_id": f"CUS-{number:06d}",
                "customer_segment": random_source.choices(
                    segments,
                    weights=[65, 15, 15, 5],
                    k=1,
                )[0],
                "age_group": random_source.choice(
                    age_groups
                ),
                "region": random_source.choice(
                    regions
                ),
                "risk_level": customer_risk,
                "kyc_status": kyc_status,
                "registration_date": random_date(
                    random_source,
                    start_date,
                    end_date,
                ).isoformat(),
            }
        )

    return rows


def generate_employees(
    random_source: random.Random,
    count: int,
) -> list[dict[str, Any]]:
    """
    Создаёт обезличенных сотрудников.
    """

    profiles = [
        {
            "department": "fraud_analytics",
            "role": "fraud_analyst",
            "access_level": "elevated",
            "allowed_tools": [
                "get_transaction_summary",
                "review_transaction",
                "open_case",
            ],
        },
        {
            "department": "customer_support",
            "role": "support_specialist",
            "access_level": "standard",
            "allowed_tools": [
                "get_customer_summary",
                "create_support_ticket",
            ],
        },
        {
            "department": "security_operations",
            "role": "security_analyst",
            "access_level": "privileged",
            "allowed_tools": [
                "get_security_event",
                "quarantine_session",
                "open_case",
            ],
        },
        {
            "department": "risk_management",
            "role": "risk_specialist",
            "access_level": "elevated",
            "allowed_tools": [
                "get_risk_summary",
                "generate_report",
            ],
        },
        {
            "department": "compliance",
            "role": "compliance_specialist",
            "access_level": "elevated",
            "allowed_tools": [
                "get_compliance_summary",
                "request_approval",
                "generate_report",
            ],
        },
        {
            "department": "product_management",
            "role": "product_analyst",
            "access_level": "standard",
            "allowed_tools": [
                "get_aggregate_metrics",
                "generate_report",
            ],
        },
        {
            "department": "data_analytics",
            "role": "data_analyst",
            "access_level": "standard",
            "allowed_tools": [
                "get_aggregate_metrics",
                "generate_report",
            ],
        },
    ]

    regions = [
        "central",
        "northwest",
        "south",
        "volga",
        "ural",
        "siberia",
        "far_east",
    ]

    rows: list[dict[str, Any]] = []

    for number in range(1, count + 1):
        profile = profiles[
            (number - 1) % len(profiles)
        ]

        employee_status = random_source.choices(
            ["active", "suspended", "disabled"],
            weights=[94, 4, 2],
            k=1,
        )[0]

        rows.append(
            {
                "employee_id": f"EMP-{number:05d}",
                "department": profile["department"],
                "role": profile["role"],
                "access_level": profile[
                    "access_level"
                ],
                "work_region": random_source.choice(
                    regions
                ),
                "status": employee_status,
                "allowed_tools": json.dumps(
                    profile["allowed_tools"],
                    ensure_ascii=False,
                ),
            }
        )

    return rows


def generate_agents(
    count: int,
) -> list[dict[str, Any]]:
    """
    Создаёт синтетических AI-агентов.
    """

    profiles = [
        {
            "agent_type": "internal_analytics_agent",
            "owner_department": "data_analytics",
            "trust_level": "high",
            "permission_profile": "analytics_read_only",
            "allowed_tools": [
                "get_aggregate_metrics",
                "generate_report",
            ],
            "data_access_level": "internal",
        },
        {
            "agent_type": "fraud_review_agent",
            "owner_department": "fraud_analytics",
            "trust_level": "high",
            "permission_profile": "fraud_review",
            "allowed_tools": [
                "get_transaction_summary",
                "review_transaction",
                "open_case",
            ],
            "data_access_level": "confidential",
        },
        {
            "agent_type": "support_agent",
            "owner_department": "customer_support",
            "trust_level": "medium",
            "permission_profile": "support_limited",
            "allowed_tools": [
                "get_customer_summary",
                "create_support_ticket",
            ],
            "data_access_level": "internal",
        },
        {
            "agent_type": "rag_agent",
            "owner_department": "compliance",
            "trust_level": "medium",
            "permission_profile": "trusted_documents_only",
            "allowed_tools": [
                "search_documents",
                "generate_report",
            ],
            "data_access_level": "internal",
        },
        {
            "agent_type": "security_agent",
            "owner_department": "security_operations",
            "trust_level": "high",
            "permission_profile": "security_response",
            "allowed_tools": [
                "get_security_event",
                "quarantine_session",
                "open_case",
            ],
            "data_access_level": "restricted",
        },
        {
            "agent_type": "external_api_agent",
            "owner_department": "external",
            "trust_level": "low",
            "permission_profile": "external_minimal",
            "allowed_tools": [
                "get_public_status",
            ],
            "data_access_level": "public",
        },
    ]

    rows: list[dict[str, Any]] = []

    for number in range(1, count + 1):
        profile = profiles[
            (number - 1) % len(profiles)
        ]

        rows.append(
            {
                "agent_id": f"AGT-{number:04d}",
                "agent_type": profile["agent_type"],
                "owner_department": profile[
                    "owner_department"
                ],
                "trust_level": profile["trust_level"],
                "permission_profile": profile[
                    "permission_profile"
                ],
                "allowed_tools": json.dumps(
                    profile["allowed_tools"],
                    ensure_ascii=False,
                ),
                "data_access_level": profile[
                    "data_access_level"
                ],
                "status": "active",
            }
        )

    return rows


def generate_documents(
    random_source: random.Random,
    count: int,
) -> list[dict[str, Any]]:
    """
    Создаёт доверенные и недоверенные документы.
    """

    document_types = [
        "policy",
        "procedure",
        "knowledge_article",
        "risk_report",
        "customer_template",
    ]

    departments = [
        "fraud_analytics",
        "customer_support",
        "security_operations",
        "risk_management",
        "compliance",
        "product_management",
        "data_analytics",
    ]

    rows: list[dict[str, Any]] = []

    for number in range(1, count + 1):
        is_untrusted = (
            random_source.random() < 0.15
        )

        contains_marker = (
            random_source.random() < 0.20
        )

        if is_untrusted:
            source_trust = "untrusted_external"

            classification = random_source.choice(
                ["public", "internal"]
            )

        else:
            source_trust = random_source.choices(
                [
                    "trusted_internal",
                    "trusted_partner",
                ],
                weights=[85, 15],
                k=1,
            )[0]

            classification = random_source.choices(
                [
                    "public",
                    "internal",
                    "confidential",
                    "restricted",
                ],
                weights=[15, 50, 28, 7],
                k=1,
            )[0]

        rows.append(
            {
                "document_id": f"DOC-{number:05d}",
                "document_type": random_source.choice(
                    document_types
                ),
                "classification": classification,
                "source_trust": source_trust,
                "owner_department": random_source.choice(
                    departments
                ),
                "contains_untrusted_instruction": (
                    is_untrusted
                ),
                "contains_synthetic_marker": (
                    contains_marker
                ),
            }
        )

    return rows


def generate_accounts(
    random_source: random.Random,
    count: int,
    customers: list[dict[str, Any]],
    end_date: date,
) -> list[dict[str, Any]]:
    """
    Создаёт счета, связанные с существующими клиентами.
    """

    if not customers:
        raise ValueError(
            "Нельзя создавать счета без клиентов."
        )

    if count < len(customers):
        raise ValueError(
            "Количество счетов должно быть не меньше "
            "количества клиентов, чтобы у каждого клиента "
            "был хотя бы один счёт."
        )

    account_types = [
        "debit",
        "credit",
        "savings",
        "business",
    ]

    currencies = [
        "RUB",
        "USD",
        "EUR",
    ]

    rows: list[dict[str, Any]] = []

    for index in range(count):
        customer = customers[
            index % len(customers)
        ]

        registration_date = date.fromisoformat(
            customer["registration_date"]
        )

        account_type = random_source.choices(
            account_types,
            weights=[50, 20, 20, 10],
            k=1,
        )[0]

        limit_ranges = {
            "debit": (10_000, 300_000),
            "credit": (20_000, 500_000),
            "savings": (5_000, 200_000),
            "business": (100_000, 2_000_000),
        }

        minimum_limit, maximum_limit = (
            limit_ranges[account_type]
        )

        daily_limit = random_source.randrange(
            minimum_limit,
            maximum_limit + 1,
            100,
        )

        account_status = random_source.choices(
            [
                "active",
                "restricted",
                "blocked",
                "closed",
            ],
            weights=[91, 4, 3, 2],
            k=1,
        )[0]

        rows.append(
            {
                "account_id": (
                    f"ACC-{index + 1:06d}"
                ),
                "customer_id": customer[
                    "customer_id"
                ],
                "account_type": account_type,
                "currency": random_source.choices(
                    currencies,
                    weights=[85, 10, 5],
                    k=1,
                )[0],
                "status": account_status,
                "daily_limit": (
                    f"{daily_limit:.2f}"
                ),
                "opening_date": random_date(
                    random_source,
                    registration_date,
                    end_date,
                ).isoformat(),
            }
        )

    return rows


def generate_transactions(
    random_source: random.Random,
    count: int,
    accounts: list[dict[str, Any]],
    customers: list[dict[str, Any]],
    end_date: date,
) -> list[dict[str, Any]]:
    """
    Создаёт транзакции по существующим счетам.
    """

    if not accounts:
        raise ValueError(
            "Нельзя создавать транзакции без счетов."
        )

    customer_regions = {
        customer["customer_id"]: customer["region"]
        for customer in customers
    }

    channels = [
        "mobile_app",
        "web",
        "atm",
        "branch",
        "api",
    ]

    merchant_categories = [
        "retail",
        "travel",
        "transport",
        "utilities",
        "telecom",
        "entertainment",
        "financial_services",
        "government",
        "other",
    ]

    recipient_types = [
        "individual",
        "company",
        "government",
        "self_transfer",
    ]

    rows: list[dict[str, Any]] = []

    for index in range(count):
        account = accounts[
            index % len(accounts)
        ]

        opening_date = date.fromisoformat(
            account["opening_date"]
        )

        risk_score = create_risk_score(
            random_source
        )

        if risk_score <= 29:
            amount = random_source.uniform(
                50,
                15_000,
            )
            fraud_label = False
            review_status = "not_required"

        elif risk_score <= 49:
            amount = random_source.uniform(
                5_000,
                60_000,
            )
            fraud_label = False
            review_status = "pending"

        elif risk_score <= 69:
            amount = random_source.uniform(
                20_000,
                200_000,
            )
            fraud_label = False
            review_status = "in_review"

        else:
            amount = random_source.uniform(
                50_000,
                600_000,
            )

            fraud_label = (
                random_source.random() < 0.65
            )

            if fraud_label:
                review_status = "confirmed_fraud"
            else:
                review_status = "in_review"

        normal_region = customer_regions[
            account["customer_id"]
        ]

        if (
            risk_score >= 70
            and random_source.random() < 0.70
        ):
            transaction_region = (
                random_source.choice(
                    [
                        "external_region_1",
                        "external_region_2",
                        "unusual_region",
                    ]
                )
            )
        else:
            transaction_region = normal_region

        rows.append(
            {
                "transaction_id": (
                    f"TXN-{index + 1:08d}"
                ),
                "account_id": account[
                    "account_id"
                ],
                "transaction_time": format_datetime(
                    random_datetime(
                        random_source,
                        opening_date,
                        end_date,
                    )
                ),
                "amount": f"{amount:.2f}",
                "currency": account["currency"],
                "channel": random_source.choice(
                    channels
                ),
                "merchant_category": (
                    random_source.choice(
                        merchant_categories
                    )
                ),
                "recipient_type": (
                    random_source.choice(
                        recipient_types
                    )
                ),
                "device_id": (
                    f"DEV-{random_source.randint(1, max(100, len(accounts))):06d}"
                ),
                "region": transaction_region,
                "risk_score": risk_score,
                "fraud_label": fraud_label,
                "review_status": review_status,
            }
        )

    return rows


def generate_agent_events(
    random_source: random.Random,
    count: int,
    agents: list[dict[str, Any]],
    employees: list[dict[str, Any]],
    start_date: date,
    end_date: date,
    minimum_high_risk_events: int,
) -> list[dict[str, Any]]:
    """
    Создаёт события агентов.

    Первые minimum_high_risk_events событий создаются
    как высокорисковые. Это позволяет затем создать
    требуемое количество связанных инцидентов.
    """

    if not agents:
        raise ValueError(
            "Нельзя создавать события без агентов."
        )

    if not employees:
        raise ValueError(
            "Нельзя создавать события без сотрудников."
        )

    if minimum_high_risk_events > count:
        raise ValueError(
            "Количество обязательных рискованных событий "
            "не может быть больше общего числа событий."
        )

    rows: list[dict[str, Any]] = []

    for index in range(count):
        agent = agents[
            index % len(agents)
        ]

        agent_tools = json.loads(
            agent["allowed_tools"]
        )

        is_required_high_risk = (
            index < minimum_high_risk_events
        )

        if is_required_high_risk:
            risk_score = random_source.randint(
                70,
                100,
            )
        else:
            risk_score = create_risk_score(
                random_source
            )

        policy_decision = decision_from_risk(
            risk_score
        )

        is_external_agent = (
            agent["agent_type"]
            == "external_api_agent"
        )

        if is_external_agent:
            employee_id = ""
        else:
            employee = employees[
                index % len(employees)
            ]
            employee_id = employee[
                "employee_id"
            ]

        if policy_decision in {
            "block",
            "quarantine",
        }:
            tool_name = random_source.choice(
                [
                    "bulk_export",
                    "admin_export",
                    "send_external_data",
                ]
            )

            action = (
                "attempt_sensitive_data_access"
            )

            data_classification = (
                random_source.choice(
                    [
                        "confidential",
                        "restricted",
                    ]
                )
            )

            record_count = random_source.randint(
                1_000,
                10_000,
            )

            destination = "external_sandbox"

        else:
            if agent_tools:
                tool_name = random_source.choice(
                    agent_tools
                )
            else:
                tool_name = ""

            action = random_source.choice(
                [
                    "read_summary",
                    "generate_report",
                    "review_event",
                    "search_document",
                ]
            )

            data_classification = (
                random_source.choice(
                    [
                        "public",
                        "internal",
                        "confidential",
                    ]
                )
            )

            record_count = random_source.randint(
                0,
                500,
            )

            destination = "internal_service"

        rows.append(
            {
                "event_id": (
                    f"EVT-{index + 1:08d}"
                ),
                "session_id": (
                    f"SES-{(index // 5) + 1:07d}"
                ),
                "agent_id": agent["agent_id"],
                "employee_id": employee_id,
                "event_time": format_datetime(
                    random_datetime(
                        random_source,
                        start_date,
                        end_date,
                    )
                ),
                "action": action,
                "tool_name": tool_name,
                "data_classification": (
                    data_classification
                ),
                "record_count": record_count,
                "destination": destination,
                "policy_decision": (
                    policy_decision
                ),
                "risk_score": risk_score,
            }
        )

    return rows


def generate_tool_calls(
    random_source: random.Random,
    count: int,
    agents: list[dict[str, Any]],
    start_date: date,
    end_date: date,
) -> list[dict[str, Any]]:
    """
    Создаёт вызовы инструментов агентами.
    """

    if not agents:
        raise ValueError(
            "Нельзя создавать вызовы инструментов "
            "без агентов."
        )

    rows: list[dict[str, Any]] = []

    for index in range(count):
        agent = agents[
            index % len(agents)
        ]

        allowed_tools = json.loads(
            agent["allowed_tools"]
        )

        risk_score = create_risk_score(
            random_source
        )

        decision = decision_from_risk(
            risk_score
        )

        if decision in {
            "block",
            "quarantine",
        }:
            tool_name = random_source.choice(
                [
                    "bulk_export",
                    "admin_export",
                    "send_external_data",
                ]
            )

            requested_scope = (
                "restricted_full_export"
            )

            approved_scope = ""

            records_requested = (
                random_source.randint(
                    1_000,
                    10_000,
                )
            )

            reason = (
                "Tool or scope is outside "
                "the agent permission profile"
            )

        elif decision == "require_approval":
            tool_name = (
                random_source.choice(
                    allowed_tools
                )
                if allowed_tools
                else "none"
            )

            requested_scope = (
                "confidential_limited"
            )

            approved_scope = ""

            records_requested = (
                random_source.randint(
                    100,
                    1_000,
                )
            )

            reason = (
                "Manual approval is required"
            )

        elif decision == "limit":
            tool_name = (
                random_source.choice(
                    allowed_tools
                )
                if allowed_tools
                else "none"
            )

            requested_scope = (
                "internal_extended"
            )

            approved_scope = (
                "internal_limited"
            )

            records_requested = (
                random_source.randint(
                    50,
                    500,
                )
            )

            reason = (
                "Requested scope was reduced "
                "by policy"
            )

        else:
            tool_name = (
                random_source.choice(
                    allowed_tools
                )
                if allowed_tools
                else "none"
            )

            requested_scope = (
                "authorized_scope"
            )

            approved_scope = (
                "authorized_scope"
            )

            records_requested = (
                random_source.randint(
                    0,
                    200,
                )
            )

            reason = (
                "Tool and scope are allowed"
            )

        rows.append(
            {
                "call_id": (
                    f"CALL-{index + 1:08d}"
                ),
                "agent_id": agent["agent_id"],
                "tool_name": tool_name,
                "requested_scope": (
                    requested_scope
                ),
                "approved_scope": (
                    approved_scope
                ),
                "records_requested": (
                    records_requested
                ),
                "decision": decision,
                "reason": reason,
                "timestamp": format_datetime(
                    random_datetime(
                        random_source,
                        start_date,
                        end_date,
                    )
                ),
            }
        )

    return rows


def generate_incidents(
    random_source: random.Random,
    count: int,
    agent_events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Создаёт инциденты на основе рискованных событий агентов.
    """

    risky_events = [
        event
        for event in agent_events
        if event["policy_decision"]
        in {"block", "quarantine"}
        or int(event["risk_score"]) >= 70
    ]

    risky_events.sort(
        key=lambda event: int(
            event["risk_score"]
        ),
        reverse=True,
    )

    if len(risky_events) < count:
        raise ValueError(
            "Недостаточно рискованных событий для "
            f"создания {count} инцидентов. "
            f"Доступно событий: {len(risky_events)}."
        )

    incident_types = [
        "unauthorized_tool_call",
        "external_data_transfer",
        "bulk_data_access",
        "repeated_policy_violation",
        "suspicious_agent_session",
    ]

    blocked_layers = [
        "identity_and_access",
        "agent_gateway",
        "tool_policy",
        "data_loss_prevention",
        "api_egress",
        "decision_engine",
    ]

    containment_actions = [
        "block_operation",
        "quarantine_session",
        "revoke_capability",
        "require_manual_review",
        "disable_agent",
    ]

    rows: list[dict[str, Any]] = []

    for index in range(count):
        source_event = risky_events[index]

        risk_score = int(
            source_event["risk_score"]
        )

        if risk_score >= 90:
            severity = "critical"
        elif risk_score >= 80:
            severity = "high"
        elif risk_score >= 70:
            severity = "medium"
        else:
            severity = "low"

        if source_event["policy_decision"] == "quarantine":
            containment_action = (
                "quarantine_session"
            )
        elif source_event["policy_decision"] == "block":
            containment_action = (
                "block_operation"
            )
        else:
            containment_action = (
                random_source.choice(
                    containment_actions
                )
            )

        incident_status = random_source.choices(
            [
                "open",
                "investigating",
                "contained",
                "resolved",
                "false_positive",
            ],
            weights=[15, 25, 30, 25, 5],
            k=1,
        )[0]

        rows.append(
            {
                "incident_id": (
                    f"INC-{index + 1:06d}"
                ),
                "incident_type": (
                    random_source.choice(
                        incident_types
                    )
                ),
                "severity": severity,
                "source_agent": source_event[
                    "agent_id"
                ],
                "detected_at": source_event[
                    "event_time"
                ],
                "affected_records": max(
                    1,
                    int(
                        source_event[
                            "record_count"
                        ]
                    ),
                ),
                "blocked_layer": (
                    random_source.choice(
                        blocked_layers
                    )
                ),
                "containment_action": (
                    containment_action
                ),
                "status": incident_status,
            }
        )

    return rows


def create_manifest(
    mode: str,
    configuration: dict[str, Any],
    generated_data: dict[
        str,
        list[dict[str, Any]],
    ],
    created_files: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """
    Создаёт содержимое манифеста генерации.
    """

    expected_counts = {
        table_name: int(count)
        for table_name, count
        in configuration["counts"].items()
    }

    actual_counts = {
        table_name: len(rows)
        for table_name, rows
        in generated_data.items()
    }

    expected_total = sum(
        expected_counts.values()
    )

    actual_total = sum(
        actual_counts.values()
    )

    counts_match = (
        expected_counts == actual_counts
    )

    return {
        "mode": mode,
        "generated_at": format_datetime(
            datetime.now(timezone.utc)
        ),
        "generator_version": configuration.get(
            "generator_version",
            DEFAULT_GENERATOR_VERSION,
        ),
        "seed": int(
            configuration["seed"]
        ),
        "date_range": {
            "start": str(
                configuration[
                    "date_range"
                ]["start"]
            ),
            "end": str(
                configuration[
                    "date_range"
                ]["end"]
            ),
        },
        "generation_order": GENERATION_ORDER,
        "expected_counts": expected_counts,
        "actual_counts": actual_counts,
        "expected_total": expected_total,
        "actual_total": actual_total,
        "files": created_files,
        "generation_status": (
            "SUCCESS"
            if counts_match
            else "FAILED"
        ),
        "validation_status": "NOT_RUN",
        "validation_errors": [],
    }


def main() -> None:
    """
    Главная функция генератора.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Создание синтетических данных "
            "для проекта."
        )
    )

    parser.add_argument(
        "--mode",
        choices=["small", "full"],
        default="small",
        help=(
            "Режим генерации: "
            "small или full."
        ),
    )

    arguments = parser.parse_args()

    configuration = load_configuration(
        arguments.mode
    )

    configured_mode = str(
        configuration["mode"]
    )

    if configured_mode != arguments.mode:
        raise ValueError(
            "Режим внутри конфигурации не совпадает "
            f"с аргументом запуска: "
            f"{configured_mode} != {arguments.mode}"
        )

    counts = {
        table_name: int(count)
        for table_name, count
        in configuration["counts"].items()
    }

    seed = int(
        configuration["seed"]
    )

    start_date = parse_date(
        configuration["date_range"]["start"]
    )

    end_date = parse_date(
        configuration["date_range"]["end"]
    )

    if start_date > end_date:
        raise ValueError(
            "Дата начала периода позже даты окончания."
        )

    random_source = random.Random(seed)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 60)
    print("ГЕНЕРАЦИЯ СИНТЕТИЧЕСКИХ ДАННЫХ")
    print("=" * 60)
    print(f"Режим: {arguments.mode}")
    print(f"Seed: {seed}")
    print(
        f"Период: {start_date} — {end_date}"
    )
    print(f"Результат: {OUTPUT_DIR}")
    print()

    print("1/9. Создание customers...")

    customers = generate_customers(
        random_source=random_source,
        count=counts["customers"],
        start_date=start_date,
        end_date=end_date,
    )

    print(
        f"     Создано: {len(customers)}"
    )

    print("2/9. Создание employees...")

    employees = generate_employees(
        random_source=random_source,
        count=counts["employees"],
    )

    print(
        f"     Создано: {len(employees)}"
    )

    print("3/9. Создание agents...")

    agents = generate_agents(
        count=counts["agents"],
    )

    print(
        f"     Создано: {len(agents)}"
    )

    print("4/9. Создание documents...")

    documents = generate_documents(
        random_source=random_source,
        count=counts["documents"],
    )

    print(
        f"     Создано: {len(documents)}"
    )

    print("5/9. Создание accounts...")

    accounts = generate_accounts(
        random_source=random_source,
        count=counts["accounts"],
        customers=customers,
        end_date=end_date,
    )

    print(
        f"     Создано: {len(accounts)}"
    )

    print("6/9. Создание transactions...")

    transactions = generate_transactions(
        random_source=random_source,
        count=counts["transactions"],
        accounts=accounts,
        customers=customers,
        end_date=end_date,
    )

    print(
        f"     Создано: {len(transactions)}"
    )

    print("7/9. Создание agent_events...")

    agent_events = generate_agent_events(
        random_source=random_source,
        count=counts["agent_events"],
        agents=agents,
        employees=employees,
        start_date=start_date,
        end_date=end_date,
        minimum_high_risk_events=counts[
            "incidents"
        ],
    )

    print(
        f"     Создано: {len(agent_events)}"
    )

    print("8/9. Создание tool_calls...")

    tool_calls = generate_tool_calls(
        random_source=random_source,
        count=counts["tool_calls"],
        agents=agents,
        start_date=start_date,
        end_date=end_date,
    )

    print(
        f"     Создано: {len(tool_calls)}"
    )

    print("9/9. Создание incidents...")

    incidents = generate_incidents(
        random_source=random_source,
        count=counts["incidents"],
        agent_events=agent_events,
    )

    print(
        f"     Создано: {len(incidents)}"
    )

    generated_data = {
        "customers": customers,
        "employees": employees,
        "agents": agents,
        "documents": documents,
        "accounts": accounts,
        "transactions": transactions,
        "agent_events": agent_events,
        "tool_calls": tool_calls,
        "incidents": incidents,
    }

    print()
    print("Сохранение CSV-файлов...")

    created_files: dict[
        str,
        dict[str, Any],
    ] = {}

    for table_name in GENERATION_ORDER:
        rows = generated_data[table_name]

        output_path = write_csv(
            table_name=table_name,
            rows=rows,
        )

        created_files[table_name] = {
            "file_name": output_path.name,
            "relative_path": str(
                output_path.relative_to(
                    ROOT_DIR
                )
            ).replace("\\", "/"),
            "row_count": len(rows),
            "sha256": create_file_hash(
                output_path
            ),
        }

        print(
            f"  {output_path.name}: "
            f"{len(rows)} строк"
        )

    manifest = create_manifest(
        mode=arguments.mode,
        configuration=configuration,
        generated_data=generated_data,
        created_files=created_files,
    )

    manifest_path = (
        OUTPUT_DIR
        / "generation_manifest.json"
    )

    with manifest_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            manifest,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print("=" * 60)
    print("ГЕНЕРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)
    print(
        f"Ожидалось строк: "
        f"{manifest['expected_total']}"
    )
    print(
        f"Создано строк: "
        f"{manifest['actual_total']}"
    )
    print(
        f"Статус: "
        f"{manifest['generation_status']}"
    )
    print(
        f"Манифест: {manifest_path}"
    )

    if (
        manifest["generation_status"]
        != "SUCCESS"
    ):
        raise RuntimeError(
            "Количество созданных строк "
            "не соответствует конфигурации."
        )


if __name__ == "__main__":
    main()