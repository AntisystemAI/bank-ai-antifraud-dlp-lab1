from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = ROOT / "datasets" / "generated"
REPORTS_DIR = ROOT / "reports"

SCHEMAS = {
    "customers": [
        "customer_id",
        "customer_segment",
        "age_group",
        "region",
        "risk_level",
        "kyc_status",
        "registration_date",
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
    "documents": [
        "document_id",
        "document_type",
        "classification",
        "source_trust",
        "owner_department",
        "contains_untrusted_instruction",
        "contains_synthetic_marker",
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

PRIMARY_KEYS = {
    "customers": "customer_id",
    "accounts": "account_id",
    "transactions": "transaction_id",
    "employees": "employee_id",
    "agents": "agent_id",
    "agent_events": "event_id",
    "tool_calls": "call_id",
    "documents": "document_id",
    "incidents": "incident_id",
}

OPTIONAL_FIELDS = {
    ("agent_events", "employee_id"),
    ("agent_events", "tool_name"),
    ("tool_calls", "approved_scope"),
}

ALLOWED_VALUES = {
    ("customers", "customer_segment"): {
        "mass",
        "premium",
        "business",
        "private",
    },
    ("customers", "age_group"): {
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65_plus",
    },
    ("customers", "risk_level"): {
        "low",
        "medium",
        "high",
    },
    ("customers", "kyc_status"): {
        "verified",
        "pending",
        "restricted",
        "expired",
    },
    ("accounts", "account_type"): {
        "debit",
        "credit",
        "savings",
        "business",
    },
    ("accounts", "currency"): {
        "RUB",
        "USD",
        "EUR",
    },
    ("accounts", "status"): {
        "active",
        "restricted",
        "blocked",
        "closed",
    },
    ("transactions", "currency"): {
        "RUB",
        "USD",
        "EUR",
    },
    ("transactions", "channel"): {
        "mobile_app",
        "web",
        "atm",
        "branch",
        "api",
    },
    ("transactions", "merchant_category"): {
        "retail",
        "travel",
        "transport",
        "utilities",
        "telecom",
        "entertainment",
        "financial_services",
        "government",
        "other",
    },
    ("transactions", "recipient_type"): {
        "individual",
        "company",
        "government",
        "self_transfer",
    },
    ("transactions", "review_status"): {
        "not_required",
        "pending",
        "in_review",
        "confirmed_legitimate",
        "confirmed_fraud",
    },
    ("employees", "access_level"): {
        "basic",
        "standard",
        "elevated",
        "privileged",
    },
    ("employees", "status"): {
        "active",
        "suspended",
        "disabled",
    },
    ("agents", "trust_level"): {
        "low",
        "medium",
        "high",
    },
    ("agents", "data_access_level"): {
        "public",
        "internal",
        "confidential",
        "restricted",
    },
    ("agents", "status"): {
        "active",
        "suspended",
        "disabled",
    },
    ("documents", "classification"): {
        "public",
        "internal",
        "confidential",
        "restricted",
    },
    ("documents", "source_trust"): {
        "trusted_internal",
        "trusted_partner",
        "untrusted_external",
    },
    ("agent_events", "data_classification"): {
        "public",
        "internal",
        "confidential",
        "restricted",
    },
    ("agent_events", "policy_decision"): {
        "allow",
        "allow_with_masking",
        "limit",
        "require_approval",
        "review",
        "block",
        "quarantine",
    },
    ("tool_calls", "decision"): {
        "allow",
        "allow_with_masking",
        "limit",
        "require_approval",
        "review",
        "block",
        "quarantine",
    },
    ("incidents", "severity"): {
        "low",
        "medium",
        "high",
        "critical",
    },
    ("incidents", "status"): {
        "open",
        "investigating",
        "contained",
        "resolved",
        "false_positive",
    },
}

BOOLEAN_FIELDS = {
    ("transactions", "fraud_label"),
    ("documents", "contains_untrusted_instruction"),
    ("documents", "contains_synthetic_marker"),
}


def load_config(mode: str) -> dict[str, Any]:
    config_path = ROOT / "config" / f"dataset_{mode}.yml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"Файл конфигурации не найден: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def read_csv(
    table_name: str,
) -> tuple[list[str], list[dict[str, str]]]:
    path = GENERATED_DIR / f"{table_name}.csv"

    if not path.exists():
        raise FileNotFoundError(f"CSV-файл не найден: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames or []
        rows = list(reader)

    return headers, rows


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def parse_boolean(value: str) -> bool:
    normalized = value.strip().lower()

    if normalized in {"true", "1", "yes"}:
        return True

    if normalized in {"false", "0", "no"}:
        return False

    raise ValueError(f"Некорректное логическое значение: {value}")


def add_error(
    errors: list[str],
    message: str,
    limit: int = 200,
) -> None:
    if len(errors) < limit:
        errors.append(message)


def validate_dataset(
    mode: str,
) -> tuple[list[str], list[str], dict[str, int]]:
    config = load_config(mode)
    expected_counts = config["counts"]
    configured_end_date = date.fromisoformat(
        str(config["date_range"]["end"])
    )

    errors: list[str] = []
    warnings: list[str] = []
    data: dict[str, list[dict[str, str]]] = {}
    actual_counts: dict[str, int] = {}

    for table_name, expected_columns in SCHEMAS.items():
        try:
            headers, rows = read_csv(table_name)
        except FileNotFoundError as error:
            add_error(errors, str(error))
            continue

        data[table_name] = rows
        actual_counts[table_name] = len(rows)

        if headers != expected_columns:
            add_error(
                errors,
                f"{table_name}: заголовки не совпадают. "
                f"Ожидалось {expected_columns}, получено {headers}.",
            )

        expected_count = int(expected_counts[table_name])

        if len(rows) != expected_count:
            add_error(
                errors,
                f"{table_name}: ожидалось {expected_count} строк, "
                f"получено {len(rows)}.",
            )

        primary_key = PRIMARY_KEYS[table_name]
        identifiers = [row.get(primary_key, "") for row in rows]

        if len(identifiers) != len(set(identifiers)):
            add_error(
                errors,
                f"{table_name}: найдены дубликаты {primary_key}.",
            )

        for row_number, row in enumerate(rows, start=2):
            for column in expected_columns:
                value = row.get(column)

                if (
                    (table_name, column) not in OPTIONAL_FIELDS
                    and (value is None or value.strip() == "")
                ):
                    add_error(
                        errors,
                        f"{table_name}, строка {row_number}: "
                        f"пустое обязательное поле {column}.",
                    )

        for (
            allowed_table,
            column,
        ), allowed_values in ALLOWED_VALUES.items():
            if allowed_table != table_name:
                continue

            invalid_values = {
                row.get(column, "")
                for row in rows
                if row.get(column, "") not in allowed_values
            }

            if invalid_values:
                add_error(
                    errors,
                    f"{table_name}.{column}: недопустимые значения "
                    f"{sorted(invalid_values)}.",
                )

        for boolean_table, boolean_column in BOOLEAN_FIELDS:
            if boolean_table != table_name:
                continue

            for row_number, row in enumerate(rows, start=2):
                try:
                    parse_boolean(row[boolean_column])
                except ValueError:
                    add_error(
                        errors,
                        f"{table_name}, строка {row_number}: "
                        f"некорректное значение {boolean_column}.",
                    )

    missing_tables = sorted(set(SCHEMAS) - set(data))

    if missing_tables:
        add_error(
            errors,
            f"Отсутствуют наборы данных: {missing_tables}.",
        )
        return errors, warnings, actual_counts

    customer_ids = {
        row["customer_id"]
        for row in data["customers"]
    }
    employee_ids = {
        row["employee_id"]
        for row in data["employees"]
    }
    agent_ids = {
        row["agent_id"]
        for row in data["agents"]
    }
    account_ids = {
        row["account_id"]
        for row in data["accounts"]
    }

    customer_registration_dates = {
        row["customer_id"]: date.fromisoformat(
            row["registration_date"]
        )
        for row in data["customers"]
    }

    account_opening_dates: dict[str, date] = {}

    for row in data["accounts"]:
        account_id = row["account_id"]
        customer_id = row["customer_id"]

        if customer_id not in customer_ids:
            add_error(
                errors,
                f"accounts: {account_id} ссылается на "
                f"неизвестного клиента {customer_id}.",
            )
            continue

        try:
            daily_limit = float(row["daily_limit"])

            if daily_limit < 0:
                add_error(
                    errors,
                    f"accounts: отрицательный daily_limit "
                    f"у {account_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"accounts: некорректный daily_limit "
                f"у {account_id}.",
            )

        try:
            opening_date = date.fromisoformat(
                row["opening_date"]
            )
            account_opening_dates[account_id] = opening_date

            registration_date = (
                customer_registration_dates[customer_id]
            )

            if opening_date < registration_date:
                add_error(
                    errors,
                    f"accounts: {account_id} открыт раньше "
                    f"регистрации клиента.",
                )

            if opening_date > configured_end_date:
                add_error(
                    errors,
                    f"accounts: будущая дата открытия "
                    f"у {account_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"accounts: некорректная дата у {account_id}.",
            )

    for row in data["transactions"]:
        transaction_id = row["transaction_id"]
        account_id = row["account_id"]

        if account_id not in account_ids:
            add_error(
                errors,
                f"transactions: {transaction_id} ссылается "
                f"на неизвестный счёт {account_id}.",
            )
            continue

        try:
            amount = float(row["amount"])

            if amount <= 0:
                add_error(
                    errors,
                    f"transactions: сумма должна быть больше нуля "
                    f"у {transaction_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"transactions: некорректная сумма "
                f"у {transaction_id}.",
            )

        try:
            risk_score = int(row["risk_score"])

            if not 0 <= risk_score <= 100:
                add_error(
                    errors,
                    f"transactions: risk_score вне диапазона "
                    f"у {transaction_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"transactions: некорректный risk_score "
                f"у {transaction_id}.",
            )

        try:
            transaction_time = parse_datetime(
                row["transaction_time"]
            )
            opening_date = account_opening_dates.get(account_id)

            if (
                opening_date is not None
                and transaction_time.date() < opening_date
            ):
                add_error(
                    errors,
                    f"transactions: {transaction_id} создана "
                    f"раньше открытия счёта.",
                )

            if transaction_time.date() > configured_end_date:
                add_error(
                    errors,
                    f"transactions: будущая дата "
                    f"у {transaction_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"transactions: некорректное время "
                f"у {transaction_id}.",
            )

    for table_name in ("employees", "agents"):
        for row in data[table_name]:
            identifier = row[PRIMARY_KEYS[table_name]]

            try:
                tools = json.loads(row["allowed_tools"])

                if not isinstance(tools, list):
                    add_error(
                        errors,
                        f"{table_name}: allowed_tools должен быть "
                        f"JSON-массивом у {identifier}.",
                    )
            except json.JSONDecodeError:
                add_error(
                    errors,
                    f"{table_name}: некорректный JSON allowed_tools "
                    f"у {identifier}.",
                )

    for row in data["agent_events"]:
        event_id = row["event_id"]

        if row["agent_id"] not in agent_ids:
            add_error(
                errors,
                f"agent_events: {event_id} ссылается "
                f"на неизвестного агента.",
            )

        if (
            row["employee_id"]
            and row["employee_id"] not in employee_ids
        ):
            add_error(
                errors,
                f"agent_events: {event_id} ссылается "
                f"на неизвестного сотрудника.",
            )

        try:
            record_count = int(row["record_count"])
            risk_score = int(row["risk_score"])

            if record_count < 0:
                add_error(
                    errors,
                    f"agent_events: отрицательный record_count "
                    f"у {event_id}.",
                )

            if not 0 <= risk_score <= 100:
                add_error(
                    errors,
                    f"agent_events: risk_score вне диапазона "
                    f"у {event_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"agent_events: некорректное числовое значение "
                f"у {event_id}.",
            )

        try:
            event_time = parse_datetime(row["event_time"])

            if event_time.date() > configured_end_date:
                add_error(
                    errors,
                    f"agent_events: будущая дата у {event_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"agent_events: некорректное время у {event_id}.",
            )

    for row in data["tool_calls"]:
        call_id = row["call_id"]

        if row["agent_id"] not in agent_ids:
            add_error(
                errors,
                f"tool_calls: {call_id} ссылается "
                f"на неизвестного агента.",
            )

        try:
            records_requested = int(
                row["records_requested"]
            )

            if records_requested < 0:
                add_error(
                    errors,
                    f"tool_calls: отрицательное количество "
                    f"у {call_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"tool_calls: некорректное количество "
                f"у {call_id}.",
            )

        try:
            call_time = parse_datetime(row["timestamp"])

            if call_time.date() > configured_end_date:
                add_error(
                    errors,
                    f"tool_calls: будущая дата у {call_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"tool_calls: некорректное время у {call_id}.",
            )

        if (
            row["decision"] in {"allow", "allow_with_masking"}
            and not row["approved_scope"]
        ):
            add_error(
                errors,
                f"tool_calls: разрешённый вызов {call_id} "
                f"не имеет approved_scope.",
            )

    for row in data["incidents"]:
        incident_id = row["incident_id"]

        if row["source_agent"] not in agent_ids:
            add_error(
                errors,
                f"incidents: {incident_id} ссылается "
                f"на неизвестного агента.",
            )

        try:
            affected_records = int(
                row["affected_records"]
            )

            if affected_records < 0:
                add_error(
                    errors,
                    f"incidents: отрицательное affected_records "
                    f"у {incident_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"incidents: некорректное affected_records "
                f"у {incident_id}.",
            )

        try:
            detected_at = parse_datetime(
                row["detected_at"]
            )

            if detected_at.date() > configured_end_date:
                add_error(
                    errors,
                    f"incidents: будущая дата у {incident_id}.",
                )
        except ValueError:
            add_error(
                errors,
                f"incidents: некорректное время у {incident_id}.",
            )

    privacy_patterns = {
        "email": re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
        "possible_card_number": re.compile(
            r"(?<!\d)\d{13,19}(?!\d)"
        ),
        "possible_secret": re.compile(
            r"(?i)\b(password|api[_-]?key|secret[_-]?key)"
            r"\s*[:=]\s*\S+"
        ),
    }

    for table_name, rows in data.items():
        for row_number, row in enumerate(rows, start=2):
            searchable_text = " ".join(
                str(value)
                for value in row.values()
            )

            for pattern_name, pattern in privacy_patterns.items():
                if pattern.search(searchable_text):
                    add_error(
                        errors,
                        f"{table_name}, строка {row_number}: "
                        f"обнаружен признак {pattern_name}.",
                    )

    suspicious_events = sum(
        1
        for row in data["agent_events"]
        if row["policy_decision"] in {
            "block",
            "quarantine",
        }
    )

    if suspicious_events == 0:
        warnings.append(
            "В agent_events нет событий block или quarantine."
        )

    confirmed_fraud = sum(
        1
        for row in data["transactions"]
        if row["review_status"] == "confirmed_fraud"
    )

    if confirmed_fraud == 0:
        warnings.append(
            "В transactions нет confirmed_fraud."
        )

    return errors, warnings, actual_counts


def write_report(
    mode: str,
    expected_counts: dict[str, int],
    actual_counts: dict[str, int],
    errors: list[str],
    warnings: list[str],
) -> str:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if errors:
        status = "FAILED"
    elif warnings:
        status = "PASSED WITH WARNINGS"
    else:
        status = "PASSED"

    lines = [
        "# Data Quality Report",
        "",
        f"- Проверено: {datetime.now(timezone.utc).isoformat()}",
        f"- Режим: `{mode}`",
        f"- Статус: **{status}**",
        f"- Критические ошибки: {len(errors)}",
        f"- Предупреждения: {len(warnings)}",
        "",
        "## Количество строк",
        "",
        "| Таблица | Ожидалось | Фактически |",
        "|---|---:|---:|",
    ]

    for table_name in SCHEMAS:
        lines.append(
            f"| `{table_name}` | "
            f"{expected_counts.get(table_name, 0)} | "
            f"{actual_counts.get(table_name, 0)} |"
        )

    lines.extend(
        [
            "",
            "## Результаты проверок",
            "",
            "- Проверена структура CSV.",
            "- Проверена уникальность идентификаторов.",
            "- Проверены обязательные поля.",
            "- Проверены внешние связи между файлами.",
            "- Проверены суммы и числовые диапазоны.",
            "- Проверены даты.",
            "- Проверены разрешённые категории.",
            "- Выполнен эвристический поиск персональных данных и секретов.",
            "",
        ]
    )

    if errors:
        lines.extend(
            [
                "## Ошибки",
                "",
            ]
        )

        for error in errors:
            lines.append(f"- {error}")

        lines.append("")

    if warnings:
        lines.extend(
            [
                "## Предупреждения",
                "",
            ]
        )

        for warning in warnings:
            lines.append(f"- {warning}")

        lines.append("")

    report_text = "\n".join(lines)

    generic_report = REPORTS_DIR / "data_quality_report.md"
    mode_report = REPORTS_DIR / f"data_quality_report_{mode}.md"

    generic_report.write_text(
        report_text,
        encoding="utf-8",
    )
    mode_report.write_text(
        report_text,
        encoding="utf-8",
    )

    return status


def update_manifest(
    mode: str,
    status: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    manifest_path = (
        GENERATED_DIR / "generation_manifest.json"
    )

    if not manifest_path.exists():
        return

    with manifest_path.open("r", encoding="utf-8") as file:
        manifest = json.load(file)

    manifest["validation_status"] = status
    manifest["validation_mode"] = mode
    manifest["validated_at"] = (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )
    manifest["validation_error_count"] = len(errors)
    manifest["validation_warning_count"] = len(warnings)

    with manifest_path.open("w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Проверка синтетических CSV."
    )
    parser.add_argument(
        "--mode",
        choices=["small", "full"],
        default="small",
    )
    args = parser.parse_args()

    config = load_config(args.mode)

    errors, warnings, actual_counts = validate_dataset(
        args.mode
    )

    status = write_report(
        mode=args.mode,
        expected_counts=config["counts"],
        actual_counts=actual_counts,
        errors=errors,
        warnings=warnings,
    )

    update_manifest(
        mode=args.mode,
        status=status,
        errors=errors,
        warnings=warnings,
    )

    print(f"Режим: {args.mode}")
    print(f"Статус: {status}")
    print(f"Ошибок: {len(errors)}")
    print(f"Предупреждений: {len(warnings)}")
    print(
        "Отчёт: "
        f"{REPORTS_DIR / 'data_quality_report.md'}"
    )

    if errors:
        print()
        print("Первые ошибки:")

        for error in errors[:20]:
            print(f"- {error}")

        raise SystemExit(1)


if __name__ == "__main__":
    main()