BEGIN;

-- ============================================================
-- Accounts
-- Ускоряет получение всех счетов конкретного клиента.
-- PostgreSQL не создаёт индекс на стороне внешнего ключа
-- автоматически.
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_accounts_customer_id
    ON public.accounts (customer_id);


-- ============================================================
-- Transactions
-- ============================================================

-- История транзакций конкретного счёта:
-- WHERE account_id = ?
-- ORDER BY transaction_time DESC
CREATE INDEX IF NOT EXISTS idx_transactions_account_time
    ON public.transactions (
        account_id,
        transaction_time DESC
    );

-- Поиск транзакций за временной период без ограничения по счёту.
CREATE INDEX IF NOT EXISTS idx_transactions_transaction_time
    ON public.transactions (transaction_time DESC);

-- Поиск операций с высоким риском.
CREATE INDEX IF NOT EXISTS idx_transactions_risk_score
    ON public.transactions (risk_score DESC);

-- Частичный индекс только для подозрительных операций.
-- Он компактнее обычного индекса по boolean-полю.
CREATE INDEX IF NOT EXISTS idx_transactions_fraud_true_time
    ON public.transactions (transaction_time DESC)
    WHERE fraud_label IS TRUE;


-- ============================================================
-- Agent events
-- ============================================================

-- История событий определённого агента.
CREATE INDEX IF NOT EXISTS idx_agent_events_agent_time
    ON public.agent_events (
        agent_id,
        event_time DESC
    );

-- История событий сотрудника.
CREATE INDEX IF NOT EXISTS idx_agent_events_employee_time
    ON public.agent_events (
        employee_id,
        event_time DESC
    )
    WHERE employee_id IS NOT NULL;

-- Поиск всех событий одной сессии.
CREATE INDEX IF NOT EXISTS idx_agent_events_session_id
    ON public.agent_events (session_id);

-- Поиск событий за временной период.
CREATE INDEX IF NOT EXISTS idx_agent_events_event_time
    ON public.agent_events (event_time DESC);

-- Поиск событий по решению политики и времени.
CREATE INDEX IF NOT EXISTS idx_agent_events_policy_decision_time
    ON public.agent_events (
        policy_decision,
        event_time DESC
    );


-- ============================================================
-- Tool calls
-- ============================================================

-- Поиск вызовов инструментов за временной период.
CREATE INDEX IF NOT EXISTS idx_tool_calls_timestamp
    ON public.tool_calls ("timestamp" DESC);

-- История вызовов определённого агента.
CREATE INDEX IF NOT EXISTS idx_tool_calls_agent_time
    ON public.tool_calls (
        agent_id,
        "timestamp" DESC
    );


-- ============================================================
-- Incidents
-- ============================================================

-- Инциденты определённой критичности, сначала новые.
CREATE INDEX IF NOT EXISTS idx_incidents_severity_time
    ON public.incidents (
        severity,
        detected_at DESC
    );

-- Инциденты определённого статуса, сначала новые.
CREATE INDEX IF NOT EXISTS idx_incidents_status_time
    ON public.incidents (
        status,
        detected_at DESC
    );

-- Все инциденты по времени обнаружения.
CREATE INDEX IF NOT EXISTS idx_incidents_detected_at
    ON public.incidents (detected_at DESC);

-- Инциденты, связанные с определённым агентом.
CREATE INDEX IF NOT EXISTS idx_incidents_source_agent_time
    ON public.incidents (
        source_agent,
        detected_at DESC
    );

COMMIT;
