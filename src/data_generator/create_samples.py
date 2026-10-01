from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATED_DIR = ROOT / "datasets" / "generated"
SAMPLES_DIR = ROOT / "datasets" / "samples"

SAMPLE_SIZES = {
    "customers": 10,
    "accounts": 15,
    "transactions": 50,
    "employees": 10,
    "agents": 10,
    "agent_events": 30,
    "tool_calls": 20,
    "documents": 10,
    "incidents": 10,
}


def create_sample(
    table_name: str,
    sample_size: int,
) -> None:
    source_path = (
        GENERATED_DIR / f"{table_name}.csv"
    )
    target_path = (
        SAMPLES_DIR / f"{table_name}_sample.csv"
    )

    if not source_path.exists():
        raise FileNotFoundError(
            f"Не найден файл {source_path}"
        )

    with source_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as source_file:
        reader = csv.DictReader(source_file)
        rows = []

        for index, row in enumerate(reader):
            if index >= sample_size:
                break

            rows.append(row)

        if not reader.fieldnames:
            raise RuntimeError(
                f"В {source_path} нет заголовков."
            )

    with target_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as target_file:
        writer = csv.DictWriter(
            target_file,
            fieldnames=reader.fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"{target_path.name}: {len(rows)} строк"
    )


def main() -> None:
    SAMPLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for table_name, sample_size in (
        SAMPLE_SIZES.items()
    ):
        create_sample(
            table_name,
            sample_size,
        )

    print("Примеры созданы.")


if __name__ == "__main__":
    main()