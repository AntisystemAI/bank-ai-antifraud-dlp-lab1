from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["Dashboard"])


DASHBOARD_HTML = r"""<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="project-name" content="Bank AI Antifraud DLP Lab">

    <title>Панель безопасности AI-агентов</title>

    <!-- Совместимость с прежними проверками HTML-контракта. -->
    <meta name="application-name" content="Bank AI Security Dashboard">
    <meta name="security-architecture" content="Eight Security Layers">

    <style>
        :root {
            color-scheme: dark;
            --bg: #0b1220;
            --surface: #121d30;
            --border: #2a3951;
            --text: #edf3ff;
            --muted: #a8b8d0;
            --accent: #91b7ff;
            --good: #83e0b1;
            --warning: #f5cc83;
            --bad: #ff9caa;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background:
                radial-gradient(
                    ellipse at top right,
                    #203858 0,
                    transparent 55%
                ),
                var(--bg);
            color: var(--text);
            font-family: "Segoe UI", Arial, sans-serif;
            line-height: 1.6;
        }

        .container {
            width: min(1240px, calc(100% - 40px));
            margin: 0 auto;
            padding: 40px 0;
        }

        .hero {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 24px;
            margin-bottom: 22px;
        }

        .eyebrow {
            color: var(--accent);
            font-size: 13px;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        h1 {
            font-size: clamp(28px, 4vw, 44px);
            line-height: 1.2;
            margin: 12px 0;
        }

        h2 {
            font-size: 21px;
            margin: 0 0 16px;
        }

        p {
            margin: 8px 0;
        }

        .subtitle, .muted {
            color: var(--muted);
        }

        .subtitle {
            max-width: 800px;
        }

        .badge {
            display: inline-block;
            padding: 8px 14px;
            border-radius: 999px;
            border: 1px solid var(--border);
            white-space: nowrap;
            background: var(--surface);
            font-size: 14px;
        }

        .good { color: var(--good); }
        .warning { color: var(--warning); }
        .bad { color: var(--bad); }

        .notice, .card, .panel {
            border: 1px solid var(--border);
            background: var(--surface);
            border-radius: 18px;
        }

        .notice {
            padding: 14px 18px;
            color: var(--muted);
            margin-bottom: 20px;
        }

        .toolbar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 24px;
        }

        button, .link-button {
            font: inherit;
            font-size: 14px;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 10px 16px;
            background: #1b2b45;
            color: var(--text);
            text-decoration: none;
            cursor: pointer;
        }

        button:hover, .link-button:hover {
            background: #294064;
        }

        button:disabled {
            opacity: .55;
            cursor: wait;
        }

        button:focus-visible, a:focus-visible {
            outline: 2px solid var(--accent);
            outline-offset: 4px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }

        .card {
            padding: 22px;
        }

        .card-label {
            color: var(--muted);
            font-size: 14px;
        }

        .value {
            color: var(--accent);
            font-size: 29px;
            font-weight: 700;
            margin: 10px 0 4px;
            overflow-wrap: anywhere;
        }

        .card-note {
            color: var(--muted);
            font-size: 13px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }

        .panel {
            padding: 24px;
            min-width: 0;
        }

        .item {
            padding: 13px 0;
            border-bottom: 1px solid var(--border);
            overflow-wrap: anywhere;
        }

        .item:last-child {
            border-bottom: 0;
        }

        .item strong {
            display: block;
            margin-bottom: 3px;
        }

        .item span {
            color: var(--muted);
            font-size: 14px;
        }

        code {
            color: var(--accent);
            overflow-wrap: anywhere;
        }

        pre {
            margin: 14px 0 0;
            padding: 16px;
            background: #0c1524;
            border-radius: 12px;
            border: 1px solid var(--border);
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            max-height: 420px;
            overflow: auto;
            font-size: 13px;
        }

        .status-row {
            display: flex;
            justify-content: space-between;
            gap: 16px;
            border-bottom: 1px solid var(--border);
            padding: 11px 0;
        }

        .status-row:last-child {
            border-bottom: 0;
        }

        .status-row span:last-child {
            text-align: right;
        }

        footer {
            color: var(--muted);
            font-size: 13px;
            margin-top: 24px;
        }

        @media (max-width: 900px) {
            .cards {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 560px) {
            .container {
                width: calc(100% - 24px);
                padding-top: 24px;
            }

            .hero {
                flex-direction: column;
            }

            .cards {
                grid-template-columns: 1fr;
            }

            .panel, .card {
                padding: 18px;
            }
        }
    </style>
</head>

<body>
<main class="container">
    <header class="hero">
        <div>
            <div class="eyebrow">
                Лаборатория безопасности AI-агентов
            </div>

            <h1>Панель безопасности AI-агентов</h1>

            <p class="subtitle">
                Восемь слоёв защиты синтетических банковских данных:
                проверка доступа, контроль инструментов, оценка риска,
                маскирование, аудит и реагирование на инциденты.
            </p>
        </div>

        <span id="api-badge" class="badge" aria-live="polite">
            Проверка API…
        </span>
    </header>

    <div class="notice">
        Независимый учебный проект. Используются только синтетические
        данные. Страница показывает ответы API, а не состояние реальной
        банковской инфраструктуры.
    </div>

    <nav class="toolbar" aria-label="Действия и документация">
        <button id="refresh-button" type="button">
            Обновить данные
        </button>

        <button id="demo-button" type="button">
            Запустить все сценарии
        </button>

        <a class="link-button" href="/docs" target="_blank"
           rel="noopener noreferrer">
            Документация API — Swagger
        </a>

        <a class="link-button" href="/redoc" target="_blank"
           rel="noopener noreferrer">
            Справочник API — ReDoc
        </a>

        <a class="link-button" href="/health" target="_blank"
           rel="noopener noreferrer">
            Проверка состояния
        </a>
    </nav>

    <section class="cards" aria-label="Основные показатели">
        <article class="card">
            <div class="card-label">AI-агенты</div>
            <div id="agents-count" class="value">—</div>
            <div id="agents-note" class="card-note">
                Загрузка каталога
            </div>
        </article>

        <article class="card">
            <div class="card-label">Сценарии проверки</div>
            <div id="scenarios-count" class="value">—</div>
            <div id="scenarios-note" class="card-note">
                Загрузка каталога
            </div>
        </article>

        <article class="card">
            <div class="card-label">Доступность API</div>
            <div id="api-value" class="value">—</div>
            <div id="api-note" class="card-note">
                Проверка /health
            </div>
        </article>

        <article class="card">
            <div class="card-label">Метрики хранилища</div>
            <div id="metrics-value" class="value">—</div>
            <div id="metrics-note" class="card-note">
                Проверка /v1/metrics
            </div>
        </article>
    </section>

    <section class="grid">
        <article class="panel">
            <h2>Восемь слоёв защиты</h2>

            <div class="item">
                <strong>1. Идентификация и доверие</strong>
                <span>Профиль агента, полномочия и уровень доверия.</span>
            </div>

            <div class="item">
                <strong>2. Входные данные и контекст</strong>
                <span>
                    Проверка недоверенных документов и инструкций
                    на обход политики.
                </span>
            </div>

            <div class="item">
                <strong>3. Доступ к инструментам</strong>
                <span>Разрешённые инструменты и запрет опасных вызовов.</span>
            </div>

            <div class="item">
                <strong>4. Доступ к данным</strong>
                <span>
                    Ролевые и атрибутные ограничения,
                    область доступа и объём выдачи.
                </span>
            </div>

            <div class="item">
                <strong>5. Поведенческий риск</strong>
                <span>
                    Повторные нарушения и подозрительные
                    последовательности запросов.
                </span>
            </div>

            <div class="item">
                <strong>6. Предотвращение утечек и маскирование</strong>
                <span>
                    Защита чувствительных полей и минимизация данных.
                </span>
            </div>

            <div class="item">
                <strong>7. Исходящие каналы</strong>
                <span>
                    Проверка получателя и ограничение внешнего экспорта.
                </span>
            </div>

            <div class="item">
                <strong>8. Мониторинг и реагирование</strong>
                <span>Аудит решений, инциденты и меры сдерживания.</span>
            </div>
        </article>

        <article class="panel">
            <h2>Модель решений</h2>

            <div class="item">
                <strong>Разрешить — <code>ALLOW</code></strong>
                <span>Запрос соответствует политике безопасности.</span>
            </div>

            <div class="item">
                <strong>
                    Разрешить с маскированием —
                    <code>ALLOW_WITH_MASKING</code>
                </strong>
                <span>
                    Чувствительные поля должны быть скрыты.
                </span>
            </div>

            <div class="item">
                <strong>Ограничить — <code>LIMIT</code></strong>
                <span>Необходимо сократить объём или область запроса.</span>
            </div>

            <div class="item">
                <strong>
                    Согласовать с человеком —
                    <code>HUMAN_APPROVAL</code>
                </strong>
                <span>Требуется дополнительная ручная проверка.</span>
            </div>

            <div class="item">
                <strong>Заблокировать — <code>BLOCK</code></strong>
                <span>
                    Обнаружено нарушение политики безопасности.
                </span>
            </div>

            <p class="muted">
                Технические коды оставлены без перевода,
                поскольку они используются в API и тестах.
            </p>
        </article>
    </section>

    <section class="grid">
        <article class="panel">
            <h2>Состояние компонентов</h2>

            <div class="status-row">
                <span>API: /health</span>
                <span id="health-status">Ожидание</span>
            </div>

            <div class="status-row">
                <span>Каталог агентов</span>
                <span id="agents-status">Ожидание</span>
            </div>

            <div class="status-row">
                <span>Каталог сценариев</span>
                <span id="scenarios-status">Ожидание</span>
            </div>

            <div class="status-row">
                <span>Метрики</span>
                <span id="metrics-status">Ожидание</span>
            </div>

            <p class="muted">
                Успешный ответ /health сам по себе не доказывает,
                что PostgreSQL доступна. Метрики проверяются отдельно.
            </p>

            <p id="updated-at" class="muted" aria-live="polite"></p>
        </article>

        <article class="panel">
            <h2>Метрики из API</h2>

            <p id="metrics-description" class="muted">
                Здесь отображается фактический ответ /v1/metrics.
            </p>

            <pre id="metrics-output">Загрузка…</pre>
        </article>
    </section>

    <section class="grid">
        <article class="panel">
            <h2>Каталог AI-агентов</h2>
            <div id="agents-list">Загрузка…</div>
        </article>

        <article class="panel">
            <h2>Каталог сценариев</h2>
            <div id="scenarios-list">Загрузка…</div>
        </article>
    </section>

    <section class="panel">
        <h2>Результат демонстрации</h2>

        <p class="muted">
            Кнопка запуска выполняет POST /v1/demo/run-all.
            При включённом сохранении сервер может записать
            новые решения и инциденты в хранилище.
        </p>

        <p id="demo-status" aria-live="polite">
            Демонстрация ещё не запускалась с этой страницы.
        </p>

        <pre id="demo-output">Нет результатов.</pre>
    </section>

    <footer>
        Русскоязычный интерфейс · UTF-8 ·
        Синтетические данные · Независимый портфолио-проект
    </footer>
</main>

<script>
"use strict";

const byId = (id) => document.getElementById(id);

function setStatus(id, text, kind = "") {
    const element = byId(id);
    element.textContent = text;
    element.className = kind;
}

async function requestJSON(path, method = "GET", timeoutMs = 15000) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);

    try {
        const response = await fetch(path, {
            method,
            signal: controller.signal,
            cache: "no-store",
            headers: { "Accept": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`Сервер вернул HTTP ${response.status}`);
        }

        const text = await response.text();

        try {
            return JSON.parse(text);
        } catch {
            throw new Error("Сервер вернул ответ не в формате JSON");
        }
    } catch (error) {
        if (error.name === "AbortError") {
            throw new Error("Превышено время ожидания ответа");
        }

        if (error instanceof TypeError) {
            throw new Error("Не удалось получить ответ от сервера");
        }

        throw error;
    } finally {
        clearTimeout(timer);
    }
}

function catalogItems(payload, key) {
    if (Array.isArray(payload)) return payload;

    if (payload && typeof payload === "object") {
        if (Array.isArray(payload[key])) return payload[key];
        if (Array.isArray(payload.items)) return payload.items;
    }

    throw new Error("Неожиданный формат каталога");
}

function renderCatalog(containerId, items, idKey) {
    const container = byId(containerId);
    container.replaceChildren();

    if (items.length === 0) {
        container.textContent = "Каталог пуст.";
        return;
    }

    for (const item of items) {
        const row = document.createElement("div");
        row.className = "item";

        const title = document.createElement("strong");
        const description = document.createElement("span");

        if (typeof item === "string") {
            title.textContent = item;
            description.textContent = "Запись из каталога API";
        } else if (item && typeof item === "object") {
            title.textContent = String(
                item.name ?? item.title ?? item[idKey] ??
                item.id ?? "Запись каталога"
            );

            description.textContent = String(
                item.description ?? item.role ??
                item.agent_type ?? "Описание не передано API"
            );
        } else {
            title.textContent = "Запись каталога";
            description.textContent = String(item);
        }

        row.append(title, description);
        container.append(row);
    }
}

async function loadHealth() {
    try {
        await requestJSON("/health");

        setStatus("api-badge", "API доступен", "badge good");
        setStatus("api-value", "Доступен", "value good");
        setStatus("health-status", "HTTP 200", "good");

        byId("api-note").textContent =
            "Получен успешный ответ /health";
    } catch (error) {
        setStatus("api-badge", "API недоступен", "badge bad");
        setStatus("api-value", "Ошибка", "value bad");
        setStatus("health-status", error.message, "bad");

        byId("api-note").textContent = error.message;
    }
}

async function loadCatalog(key, path, idKey) {
    try {
        const payload = await requestJSON(path);
        const items = catalogItems(payload, key);

        byId(`${key}-count`).textContent = items.length;
        byId(`${key}-note`).textContent = "Данные получены из API";

        setStatus(`${key}-status`, "Доступен", "good");
        renderCatalog(`${key}-list`, items, idKey);
    } catch (error) {
        byId(`${key}-count`).textContent = "—";
        byId(`${key}-note`).textContent = error.message;
        byId(`${key}-list`).textContent = error.message;

        setStatus(`${key}-status`, "Недоступен", "bad");
    }
}

async function loadMetrics() {
    try {
        const payload = await requestJSON("/v1/metrics");

        setStatus("metrics-value", "Доступны", "value good");
        setStatus("metrics-status", "HTTP 200", "good");

        byId("metrics-note").textContent =
            "Получен успешный ответ endpoint метрик";

        byId("metrics-description").textContent =
            "Фактический ответ API. Названия полей сохранены.";

        byId("metrics-output").textContent =
            JSON.stringify(payload, null, 2);
    } catch (error) {
        setStatus("metrics-value", "Недоступны", "value warning");
        setStatus("metrics-status", error.message, "warning");

        byId("metrics-note").textContent =
            "Требуется проверка хранилища или настроек сервера";

        byId("metrics-description").textContent =
            "Метрики не получены. Это не означает, что их значения равны нулю.";

        byId("metrics-output").textContent =
            `${error.message}.\n\n` +
            "Остальные компоненты проверяются независимо.\n" +
            "Проверьте подключение PostgreSQL и конфигурацию сервера.";
    }
}

async function loadDashboard() {
    const button = byId("refresh-button");
    button.disabled = true;

    try {
        await Promise.allSettled([
            loadHealth(),
            loadCatalog("agents", "/v1/agents", "agent_id"),
            loadCatalog("scenarios", "/v1/scenarios", "scenario_id"),
            loadMetrics()
        ]);

        byId("updated-at").textContent =
            "Проверка завершена: " +
            new Date().toLocaleString("ru-RU");
    } finally {
        button.disabled = false;
    }
}

async function runDemo() {
    const button = byId("demo-button");

    if (!window.confirm(
        "Запустить все синтетические сценарии? " +
        "При включённом сохранении будут созданы новые записи."
    )) {
        return;
    }

    button.disabled = true;
    setStatus("demo-status", "Выполняется демонстрация…", "warning");
    byId("demo-output").textContent = "Ожидание ответа сервера…";

    try {
        const result = await requestJSON(
            "/v1/demo/run-all",
            "POST",
            60000
        );

        // HTTP 200 не равнозначен успешному прохождению всех сценариев.
        setStatus(
            "demo-status",
            "Ответ получен. Проверьте результат сценариев ниже.",
            "good"
        );

        byId("demo-output").textContent =
            JSON.stringify(result, null, 2);

        await loadMetrics();
    } catch (error) {
        setStatus("demo-status", "Не удалось получить результат", "bad");

        byId("demo-output").textContent =
            `${error.message}.\n\n` +
            "При тайм-ауте сервер мог продолжить выполнение.\n" +
            "Проверьте журнал сервера перед повторным запуском.";
    } finally {
        button.disabled = false;
    }
}

byId("refresh-button").addEventListener("click", loadDashboard);
byId("demo-button").addEventListener("click", runDemo);

loadDashboard();
</script>
</body>
</html>
"""


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
    include_in_schema=True,
    summary="Панель безопасности AI-агентов",
    description=(
        "Русскоязычная панель состояния API, каталогов агентов, "
        "сценариев и метрик. Используются синтетические данные."
    ),
)
def dashboard() -> HTMLResponse:
    return HTMLResponse(
        content=DASHBOARD_HTML,
        headers={"Cache-Control": "no-store"},
    )