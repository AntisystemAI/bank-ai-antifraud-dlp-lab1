from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter(tags=["Dashboard"])


DASHBOARD_HTML = """
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bank AI Antifraud DLP Lab</title>

    <style>
        :root {
            color-scheme: dark;
            --background: #09111f;
            --panel: #111c2d;
            --panel-light: #182840;
            --border: #2a3c57;
            --text: #edf4ff;
            --muted: #9caec5;
            --blue: #62b0ff;
            --green: #42d392;
            --yellow: #f2bf5b;
            --red: #ff6d7a;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            color: var(--text);
            background:
                radial-gradient(
                    circle at 90% 0%,
                    #1b4772 0,
                    transparent 32rem
                ),
                var(--background);
            font-family:
                Inter,
                "Segoe UI",
                Arial,
                sans-serif;
        }

        .container {
            width: min(1220px, calc(100% - 32px));
            margin: 0 auto;
            padding: 32px 0 56px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 24px;
            margin-bottom: 28px;
        }

        h1 {
            margin: 0 0 10px;
            font-size: clamp(28px, 5vw, 48px);
            line-height: 1.1;
        }

        h2 {
            margin: 0 0 14px;
            font-size: 21px;
        }

        h3 {
            margin: 0 0 8px;
            font-size: 16px;
        }

        p {
            color: var(--muted);
            line-height: 1.6;
        }

        .subtitle {
            max-width: 800px;
            margin: 0;
            font-size: 16px;
        }

        .badge {
            padding: 9px 14px;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: var(--panel);
            color: var(--yellow);
            white-space: nowrap;
            font-size: 14px;
        }

        .badge.ok {
            color: var(--green);
        }

        .badge.error {
            color: var(--red);
        }

        .grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(210px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }

        .panel {
            padding: 22px;
            border: 1px solid var(--border);
            border-radius: 16px;
            background: rgba(17, 28, 45, .94);
            box-shadow: 0 15px 36px rgba(0, 0, 0, .2);
        }

        .metric {
            margin: 8px 0 4px;
            color: var(--blue);
            font-size: 36px;
            font-weight: 750;
        }

        .label {
            color: var(--muted);
            font-size: 13px;
        }

        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 18px;
        }

        button,
        a.button {
            display: inline-block;
            padding: 11px 15px;
            border: 0;
            border-radius: 10px;
            background: var(--blue);
            color: #07111e;
            font-weight: 750;
            text-decoration: none;
            cursor: pointer;
        }

        button.secondary,
        a.button.secondary {
            border: 1px solid var(--border);
            background: var(--panel-light);
            color: var(--text);
        }

        .columns {
            display: grid;
            grid-template-columns: repeat(
                auto-fit,
                minmax(300px, 1fr)
            );
            gap: 20px;
            margin-bottom: 20px;
        }

        .layers {
            display: grid;
            gap: 9px;
            padding: 0;
            margin: 0;
            list-style: none;
        }

        .layers li {
            padding: 11px 12px;
            border: 1px solid var(--border);
            border-radius: 9px;
            background: rgba(24, 40, 64, .75);
            color: var(--muted);
        }

        .layers strong {
            color: var(--text);
        }

        .decision-grid {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(140px, 1fr));
            gap: 10px;
        }

        .decision {
            padding: 14px;
            border-left: 4px solid var(--blue);
            border-radius: 8px;
            background: #0c1727;
        }

        .decision strong {
            display: block;
            margin-bottom: 5px;
            font-size: 13px;
        }

        .decision span {
            color: var(--muted);
            font-size: 12px;
        }

        pre {
            min-height: 170px;
            overflow: auto;
            padding: 15px;
            border-radius: 10px;
            background: #060d17;
            color: #cbd8e8;
            font-size: 13px;
            line-height: 1.5;
        }

        footer {
            margin-top: 26px;
            color: var(--muted);
            font-size: 13px;
        }

        @media (max-width: 700px) {
            header {
                display: block;
            }

            .badge {
                display: inline-block;
                margin-top: 16px;
            }
        }
    </style>
</head>

<body>
<header class="hero">
    <div class="eyebrow">BANK AI ANTIFRAUD DLP LAB</div>
    <h1>Bank AI Security Dashboard</h1>
    <p>
        Synthetic control plane for safe AI agents,
        transaction-data protection and incident response.
    </p>
    <div class="security-badge">Eight Security Layers</div>
</header>
<main class="container">
    <header>
        <div>
            <h1>Bank AI Antifraud DLP Lab</h1>
            <p class="subtitle">
                Р”РµРјРѕРЅСЃС‚СЂР°С†РёРѕРЅРЅС‹Р№ РєРѕРЅС‚СѓСЂ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё AI-Р°РіРµРЅС‚РѕРІ:
                policy engine, antifraud-СЂРёСЃРє, DLP, РєРѕРЅС‚СЂРѕР»СЊ РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ,
                Р°СѓРґРёС‚ Рё СЂРµР°РіРёСЂРѕРІР°РЅРёРµ РЅР° РёРЅС†РёРґРµРЅС‚С‹.
            </p>
        </div>

        <div id="health-badge" class="badge">
            РџСЂРѕРІРµСЂРєР° API...
        </div>
    </header>

    <section class="grid">
        <div class="panel">
            <div class="label">AI-Р°РіРµРЅС‚С‹</div>
            <div id="agents-count" class="metric">вЂ”</div>
            <div class="label">РїСЂРѕС„РёР»РµР№ Р±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё</div>
        </div>

        <div class="panel">
            <div class="label">РЎС†РµРЅР°СЂРёРё</div>
            <div id="scenarios-count" class="metric">вЂ”</div>
            <div class="label">РґРµРјРѕРЅСЃС‚СЂР°С†РёРѕРЅРЅС‹С… РїСЂРѕРІРµСЂРѕРє</div>
        </div>

        <div class="panel">
            <div class="label">Р РµС€РµРЅРёСЏ</div>
            <div id="decisions-count" class="metric">вЂ”</div>
            <div class="label">Р·Р°РїРёСЃРµР№ runtime</div>
        </div>

        <div class="panel">
            <div class="label">РРЅС†РёРґРµРЅС‚С‹</div>
            <div id="incidents-count" class="metric">вЂ”</div>
            <div class="label">СЃРѕР·РґР°РЅРЅС‹С… СЃРёСЃС‚РµРјРѕР№</div>
        </div>
    </section>

    <section class="columns">
        <div class="panel">
            <h2>Eight Security Layers</h2>

            <ol class="layers">
                <li>
                    <strong>1. Identity and Trust</strong><br>
                    РџСЂРѕРІРµСЂРєР° Р°РіРµРЅС‚Р°, РІР»Р°РґРµР»СЊС†Р° Рё СЃРѕСЃС‚РѕСЏРЅРёСЏ.
                </li>
                <li>
                    <strong>2. Input Control</strong><br>
                    РџСЂРѕРІРµСЂРєР° РєРѕРЅС‚РµРєСЃС‚Р° Рё РЅРµРґРѕРІРµСЂРµРЅРЅС‹С… РёРЅСЃС‚СЂСѓРєС†РёР№.
                </li>
                <li>
                    <strong>3. Tool Access</strong><br>
                    Allowlist РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ Рё Р·Р°РїСЂРµС‚ РѕРїР°СЃРЅС‹С… С„СѓРЅРєС†РёР№.
                </li>
                <li>
                    <strong>4. Data Access</strong><br>
                    RBAC, ABAC, РєР»Р°СЃСЃРёС„РёРєР°С†РёСЏ Рё Р»РёРјРёС‚С‹.
                </li>
                <li>
                    <strong>5. Behavioral Risk</strong><br>
                    РўСЂР°РЅР·Р°РєС†РёРѕРЅРЅС‹Р№ СЂРёСЃРє Рё РїРѕРІС‚РѕСЂРЅС‹Рµ РЅР°СЂСѓС€РµРЅРёСЏ.
                </li>
                <li>
                    <strong>6. DLP and Masking</strong><br>
                    РћР±РЅР°СЂСѓР¶РµРЅРёРµ Рё РјР°СЃРєРёСЂРѕРІР°РЅРёРµ С‡СѓРІСЃС‚РІРёС‚РµР»СЊРЅС‹С… РїРѕР»РµР№.
                </li>
                <li>
                    <strong>7. Egress Control</strong><br>
                    РљРѕРЅС‚СЂРѕР»СЊ РїРѕР»СѓС‡Р°С‚РµР»СЏ Рё РёСЃС…РѕРґСЏС‰РµРіРѕ РєР°РЅР°Р»Р°.
                </li>
                <li>
                    <strong>8. Monitoring and Response</strong><br>
                    РђСѓРґРёС‚, containment Рё СЃРѕР·РґР°РЅРёРµ РёРЅС†РёРґРµРЅС‚РѕРІ.
                </li>
            </ol>
        </div>

        <div class="panel">
            <h2>Decision Model</h2>

            <div class="decision-grid">
                <div class="decision">
                    <strong>ALLOW</strong>
                    <span>Р—Р°РїСЂРѕСЃ СЂР°Р·СЂРµС€С‘РЅ.</span>
                </div>

                <div class="decision">
                    <strong>ALLOW_WITH_MASKING</strong>
                    <span>Р Р°Р·СЂРµС€С‘РЅ РїРѕСЃР»Рµ DLP.</span>
                </div>

                <div class="decision">
                    <strong>LIMIT</strong>
                    <span>РћР±СЉС‘Рј РѕРіСЂР°РЅРёС‡РµРЅ.</span>
                </div>

                <div class="decision">
                    <strong>HUMAN_APPROVAL</strong>
                    <span>РќСѓР¶РЅРѕ СЃРѕРіР»Р°СЃРѕРІР°РЅРёРµ.</span>
                </div>

                <div class="decision">
                    <strong>BLOCK</strong>
                    <span>РЎРѕР·РґР°С‘С‚СЃСЏ РёРЅС†РёРґРµРЅС‚.</span>
                </div>
            </div>

            <div class="actions">
                <button onclick="loadDashboard()">
                    РћР±РЅРѕРІРёС‚СЊ РїРѕРєР°Р·Р°С‚РµР»Рё
                </button>

                <button onclick="runDemo()">
                    Р—Р°РїСѓСЃС‚РёС‚СЊ 11 СЃС†РµРЅР°СЂРёРµРІ
                </button>

                <a class="button secondary" href="/docs">
                    Swagger
                </a>

                <a class="button secondary" href="/redoc">
                    ReDoc
                </a>
            </div>
        </div>
    </section>

    <section class="panel">
        <h2>Runtime Output</h2>
        <p>
            РќРёР¶Рµ РѕС‚РѕР±СЂР°Р¶Р°СЋС‚СЃСЏ СЂРµР·СѓР»СЊС‚Р°С‚С‹ health-check, РјРµС‚СЂРёРєРё Рё РїРѕСЃР»РµРґРЅРµРіРѕ
            Р·Р°РїСѓСЃРєР° РґРµРјРѕРЅСЃС‚СЂР°С†РёРѕРЅРЅС‹С… СЃС†РµРЅР°СЂРёРµРІ.
        </p>
        <pre id="output">Р“РѕС‚РѕРІРѕ Рє СЂР°Р±РѕС‚Рµ.</pre>
    </section>

    <footer>
        Synthetic data only. This project does not connect to real banking
        infrastructure.
    </footer>
</main>

<script>
async function requestJson(url, options = {}) {
    const response = await fetch(url, options);
    const text = await response.text();

    if (!response.ok) {
        throw new Error(response.status + ": " + text);
    }

    return text ? JSON.parse(text) : {};
}

function setText(id, value) {
    document.getElementById(id).textContent =
        value === undefined || value === null ? "вЂ”" : value;
}

function setHealth(ok, text) {
    const badge = document.getElementById("health-badge");
    badge.textContent = text;
    badge.className = ok ? "badge ok" : "badge error";
}

async function loadDashboard() {
    const output = document.getElementById("output");

    try {
        const health = await requestJson("/health");
        const agents = await requestJson("/v1/agents");
        const scenarios = await requestJson("/v1/scenarios");
        const metrics = await requestJson("/v1/metrics");

        setHealth(true, "API: OK");

        setText(
            "agents-count",
            Array.isArray(agents)
                ? agents.length
                : agents.total
        );

        setText(
            "scenarios-count",
            Array.isArray(scenarios)
                ? scenarios.length
                : scenarios.total
        );

        setText(
            "decisions-count",
            metrics.total_decisions ??
            metrics.decisions_count ??
            0
        );

        setText(
            "incidents-count",
            metrics.total_incidents ??
            metrics.incidents_count ??
            0
        );

        output.textContent = JSON.stringify(
            {
                health: health,
                metrics: metrics
            },
            null,
            2
        );
    } catch (error) {
        setHealth(false, "API: ERROR");
        output.textContent = String(error);
    }
}

async function runDemo() {
    const output = document.getElementById("output");
    output.textContent = "Р’С‹РїРѕР»РЅСЏРµС‚СЃСЏ РґРµРјРѕРЅСЃС‚СЂР°С†РёСЏ...";

    try {
        const result = await requestJson(
            "/v1/demo/run-all",
            { method: "POST" }
        );

        output.textContent = JSON.stringify(result, null, 2);
        await loadDashboard();
    } catch (error) {
        output.textContent = String(error);
    }
}

loadDashboard();
</script>
</body>
</html>
"""


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
    include_in_schema=False,
)
def dashboard() -> str:
    return DASHBOARD_HTML
