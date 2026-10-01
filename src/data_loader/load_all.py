from __future__ import annotations

import argparse
import csv
import json
import time
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any

from psycopg import sql
from psycopg.types.json import Jsonb

from src.data_quality.validate_all import SCHEMAS
from src.database.connection import get_connection


ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = ROOT / "datasets" / "generated"
REPORTS_DIR = ROOT / "reports"

TABLE_ORDER = [
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

RESET_ORDER = [
    "incidents",
    "tool_calls",
    "agent_events",
    "transactions",
    "accounts",
    "documents",
    "agents",
    "employees",
    "customers",
]

JSON_FIELDS = {
    ("employees", "allowed_tools"),
    ("agents", "allowed_tools"),
}

BOOLEAN_FIELDS = {
    ("transactions", "fraud_label"),
    ("documents", "contains_untrusted_instruction"),
    ("documents", "contains_synthetic_marker"),
}

INTEGER_FIELDS = {
    ("transactions", "risk_score"),
    ("agent_events", "record_count"),
    ("agent_events", "risk_score"),
    ("tool_calls", "records_requested"),
    ("incidents", "affected_records"),
}

DECIMAL_FIELDS = {
    ("accounts", "daily_limit"),
    ("transactions", "amount"),
}

DATE_FIELDS = {
    ("customers", "registration_date"),
    ("accounts", "opening_date"),
}

DATETIME_FIELDS = {
    ("transactions", "transaction_time"),
    ("agent_events", "event_time"),
    ("tool_calls", "timestamp"),
    ("incidents", "detected_at"),
}

NULLABLE_FIELDS = {
    ("agent_events", "employee_id"),
    ("agent_events", "tool_name"),
    ("tool_calls", "approved_scope"),
}


def parse_boolean(value: str) -> bool:
    normalized = value.strip().lower()

    if normalized in {"true", "1", "yes"}:
        return True

    if normalized in {"false", "0", "no"}:
        return False

    raise ValueError(
        f"Некорректное логическое значение: {value}"
    )


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def convert_value(
    table_name: str,
    column_name: str,
    value: str,
) -> Any:
    if (
        (table_name, column_name) in NULLABLE_FIELDS
        and value == ""
    ):
        return None

    field = (table_name, column_name)

    if field in JSON_FIELDS:
        return Jsonb(json.loads(value))

    if field in BOOLEAN_FIELDS:
        return parse_boolean(value)

    if field in INTEGER_FIELDS:
        return int(value)

    if field in DECIMAL_FIELDS:
        return Decimal(value)

    if field in DATE_FIELDS:
        return date.fromisoformat(value)

    if field in DATETIME_FIELDS:
        return parse_datetime(value)

    return value


def read_csv_rows(
    table_name: str,
) -> list[tuple[Any, ...]]:
    csv_path = GENERATED_DIR / f"{table_name}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Не найден файл: {csv_path}"
        )

    expected_columns = SCHEMAS[table_name]

    with csv_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        actual_columns = reader.fieldnames or []

        if actual_columns != expected_columns:
            raise RuntimeError(
                f"{table_name}: заголовки CSV не совпадают. "
                f"Ожидалось {expected_columns}, "
                f"получено {actual_columns}."
            )

        converted_rows = []

        for row_number, row in enumerate(
            reader,
            start=2,
        ):
            try:
                converted_rows.append(
                    tuple(
                        convert_value(
                            table_name,
                            column_name,
                            row[column_name],
                        )
                        for column_name in expected_columns
                    )
                )
            except Exception as error:
                raise RuntimeError(
                    f"Ошибка преобразования {table_name}, "
                    f"строка {row_number}: {error}"
                ) from error

    return converted_rows


def load_manifest(mode: str) -> dict[str, Any]:
    manifest_path = (
        GENERATED_DIR / "generation_manifest.json"
    )

    if not manifest_path.exists():
        raise FileNotFoundError(
            "Не найден generation_manifest.json. "
            "Сначала запусти генератор."
        )

    with manifest_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        manifest = json.load(file)

    if manifest.get("mode") != mode:
        raise RuntimeError(
            f"Манифест имеет режим "
            f"{manifest.get('mode')}, ожидался {mode}."
        )

    if manifest.get("generation_status") != "SUCCESS":
        raise RuntimeError(
            "Генерация не имеет статуса SUCCESS."
        )

    if manifest.get("validation_status") not in {
        "PASSED",
        "PASSED WITH WARNINGS",
    }:
        raise RuntimeError(
            "Данные не прошли проверку качества. "
            "Сначала запусти validate_all."
        )

    return manifest


def verify_database_schema(cursor) -> None:
    for table_name, expected_columns in SCHEMAS.items():
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = %s
            ORDER BY ordinal_position;
            """,
            (table_name,),
        )

        actual_columns = [
            row[0]
            for row in cursor.fetchall()
        ]

        if not actual_columns:
            raise RuntimeError(
                f"В PostgreSQL отсутствует таблица "
                f"public.{table_name}."
            )

        if actual_columns != expected_columns:
            raise RuntimeError(
                f"Структура public.{table_name} "
                f"не совпадает с CSV. "
                f"Ожидалось {expected_columns}, "
                f"получено {actual_columns}."
            )


def get_table_counts(cursor) -> dict[str, int]:
    counts: dict[str, int] = {}

    for table_name in TABLE_ORDER:
        query = sql.SQL(
            "SELECT COUNT(*) FROM public.{}"
        ).format(
            sql.Identifier(table_name)
        )

        cursor.execute(query)
        counts[table_name] = int(
            cursor.fetchone()[0]
        )

    return counts


def reset_tables(cursor) -> None:
    table_names = [
        sql.SQL("public.{}").format(
            sql.Identifier(table_name)
        )
        for table_name in RESET_ORDER
    ]

    query = sql.SQL(
        "TRUNCATE TABLE {};"
    ).format(
        sql.SQL(", ").join(table_names)
    )

    cursor.execute(query)


def insert_rows(
    cursor,
    table_name: str,
    rows: list[tuple[Any, ...]],
    batch_size: int,
) -> int:
    columns = SCHEMAS[table_name]

    query = sql.SQL(
        "INSERT INTO public.{} ({}) VALUES ({})"
    ).format(
        sql.Identifier(table_name),
        sql.SQL(", ").join(
            sql.Identifier(column)
            for column in columns
        ),
        sql.SQL(", ").join(
            sql.Placeholder()
            for _ in columns
        ),
    )

    loaded_rows = 0

    for start in range(0, len(rows), batch_size):
        batch = rows[start:start + batch_size]
        cursor.executemany(query, batch)
        loaded_rows += len(batch)

        print(
            f"{table_name}: "
            f"{loaded_rows}/{len(rows)}"
        )

    return loaded_rows


def write_load_report(
    mode: str,
    expected_counts: dict[str, int],
    actual_counts: dict[str, int],
    duration_seconds: float,
    status: str,
    error_message: str | None = None,
) -> None:
    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = [
        "# PostgreSQL Load Report",
        "",
        f"- Дата: {datetime.now(timezone.utc).isoformat()}",
        "- База: `bank_ai_lab`",
        "- Схема: `public`",
        f"- Режим: `{mode}`",
        f"- Статус: **{status}**",
        f"- Время загрузки: {duration_seconds:.2f} секунд",
        "",
        "## Количество строк",
        "",
        "| Таблица | Ожидалось | В PostgreSQL |",
        "|---|---:|---:|",
    ]

    for table_name in TABLE_ORDER:
        lines.append(
            f"| `{table_name}` | "
            f"{expected_counts.get(table_name, 0)} | "
            f"{actual_counts.get(table_name, 0)} |"
        )

    if error_message:
        lines.extend(
            [
                "",
                "## Ошибка",
                "",
                f"`{error_message}`",
            ]
        )

    report_text = "\n".join(lines)

    generic_report = (
        REPORTS_DIR / "database_load_report.md"
    )
    mode_report = (
        REPORTS_DIR
        / f"database_load_report_{mode}.md"
    )

    generic_report.write_text(
        report_text,
        encoding="utf-8",
    )
    mode_report.write_text(
        report_text,
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Загрузка синтетических CSV в PostgreSQL."
    )
    parser.add_argument(
        "--mode",
        choices=["small", "full"],
        default="small",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help=(
            "Очистить девять демонстрационных таблиц "
            "перед загрузкой."
        ),
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=2000,
    )
    args = parser.parse_args()

    started_at = time.perf_counter()
    manifest = load_manifest(args.mode)

    expected_counts = {
        table_name: int(count)
        for table_name, count
        in manifest["expected_counts"].items()
    }

    final_counts = {
        table_name: 0
        for table_name in TABLE_ORDER
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        current_database(),
                        current_user;
                    """
                )

                database_name, database_user = (
                    cursor.fetchone()
                )

                if database_name != "bank_ai_lab":
                    raise RuntimeError(
                        f"Подключение выполнено к базе "
                        f"{database_name}, ожидалась bank_ai_lab."
                    )

                print(
                    f"Подключено к {database_name} "
                    f"как {database_user}."
                )

                verify_database_schema(cursor)
                print("Структура базы проверена.")

                existing_counts = get_table_counts(
                    cursor
                )
                nonempty_tables = {
                    table_name: count
                    for table_name, count
                    in existing_counts.items()
                    if count > 0
                }

                if nonempty_tables and not args.reset:
                    raise RuntimeError(
                        "В таблицах уже есть данные: "
                        f"{nonempty_tables}. "
                        "Для осознанной очистки используй --reset."
                    )

                if args.reset:
                    print(
                        "Выполняется очистка "
                        "демонстрационных таблиц..."
                    )
                    reset_tables(cursor)

                for table_name in TABLE_ORDER:
                    rows = read_csv_rows(table_name)

                    expected_count = expected_counts[
                        table_name
                    ]

                    if len(rows) != expected_count:
                        raise RuntimeError(
                            f"{table_name}: ожидалось "
                            f"{expected_count} строк, "
                            f"CSV содержит {len(rows)}."
                        )

                    if table_name in {
                        "transactions",
                        "agent_events",
                        "tool_calls",
                    }:
                        batch_size = args.batch_size
                    else:
                        batch_size = max(
                            len(rows),
                            1,
                        )

                    insert_rows(
                        cursor=cursor,
                        table_name=table_name,
                        rows=rows,
                        batch_size=batch_size,
                    )

                final_counts = get_table_counts(
                    cursor
                )

                mismatches = {
                    table_name: {
                        "expected": expected_counts[
                            table_name
                        ],
                        "actual": final_counts[
                            table_name
                        ],
                    }
                    for table_name in TABLE_ORDER
                    if final_counts[table_name]
                    != expected_counts[table_name]
                }

                if mismatches:
                    raise RuntimeError(
                        "Количество строк после загрузки "
                        f"не совпадает: {mismatches}"
                    )

        duration_seconds = (
            time.perf_counter() - started_at
        )

        write_load_report(
            mode=args.mode,
            expected_counts=expected_counts,
            actual_counts=final_counts,
            duration_seconds=duration_seconds,
            status="SUCCESS",
        )

        print()
        print("Загрузка завершена успешно.")
        print(
            f"Загружено строк: "
            f"{sum(final_counts.values())}"
        )
        print(
            f"Время: {duration_seconds:.2f} секунд"
        )

    except Exception as error:
        duration_seconds = (
            time.perf_counter() - started_at
        )

        write_load_report(
            mode=args.mode,
            expected_counts=expected_counts,
            actual_counts=final_counts,
            duration_seconds=duration_seconds,
            status="FAILED",
            error_message=str(error),
        )

        print()
        print("Загрузка отменена.")
        print(f"Тип ошибки: {type(error).__name__}")
        print(f"Сообщение: {error}")
        print(
            "Изменения текущей операции "
            "не должны быть зафиксированы."
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()