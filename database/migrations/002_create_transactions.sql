CREATE TABLE IF NOT EXISTS public.security_decisions (
    decision_id VARCHAR(80) PRIMARY KEY,
    event_id VARCHAR(80) NOT NULL UNIQUE,
    actor_id VARCHAR(80) NOT NULL,
    agent_id VARCHAR(80),
    session_id VARCHAR(80) NOT NULL,
    correlation_id VARCHAR(80) NOT NULL,

    risk_score SMALLINT NOT NULL
        CHECK (risk_score BETWEEN 0 AND 100),

    final_decision VARCHAR(40) NOT NULL
        CHECK (
            final_decision IN (
                'ALLOW',
                'ALLOW_WITH_MASKING',
                'LIMIT',
                'HUMAN_APPROVAL',
                'BLOCK'
            )
        ),

    reason_codes JSONB NOT NULL,
    layer_results JSONB NOT NULL,

    policy_version VARCHAR(30) NOT NULL,
    evaluated_at TIMESTAMPTZ NOT NULL,
    is_synthetic BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_security_decisions_actor
    ON public.security_decisions (actor_id);

CREATE INDEX IF NOT EXISTS idx_security_decisions_agent
    ON public.security_decisions (agent_id);

CREATE INDEX IF NOT EXISTS idx_security_decisions_session
    ON public.security_decisions (session_id);

CREATE INDEX IF NOT EXISTS idx_security_decisions_correlation
    ON public.security_decisions (correlation_id);

CREATE INDEX IF NOT EXISTS idx_security_decisions_result
    ON public.security_decisions (final_decision);

CREATE INDEX IF NOT EXISTS idx_security_decisions_evaluated_at
    ON public.security_decisions (evaluated_at);