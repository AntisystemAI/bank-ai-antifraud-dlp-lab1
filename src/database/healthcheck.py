from __future__ import annotations

from src.database.connection import get_connection


def main() -> None:
    print("Проверка подключения к PostgreSQL...")

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        current_database(),
                        current_user,
                        current_schema();
                    """
                )

                result = cursor.fetchone()

                if result is None:
                    raise RuntimeError(
                        "PostgreSQL не вернул результат проверки."
                    )

                database_name, user_name, schema_name = result

        print("Подключение к PostgreSQL успешно.")
        print(f"База: {database_name}")
        print(f"Пользователь: {user_name}")
        print(f"Схема: {schema_name}")

    except Exception as error:
        print("Не удалось подключиться к PostgreSQL.")
        print(f"Тип ошибки: {type(error).__name__}")
        print(f"Сообщение: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()