BEGIN;

CREATE TABLE IF NOT EXISTS public.security_decisions (
    decision_id VARCHAR(80) PRIMARY KEY,
    event_id VARCHAR(80) NOT NULL UNIQUE,
    actor_id VARCHAR(80) NOT NULL,
    agent_id VARCHAR(80) NOT NULL,
    session_id VARCHAR(80) NOT NULL,

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

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.security_incidents (
    incident_id VARCHAR(80) PRIMARY KEY,
    decision_id VARCHAR(80) NOT NULL,
    event_id VARCHAR(80) NOT NULL,
    agent_id VARCHAR(80) NOT NULL,

    severity VARCHAR(20) NOT NULL
        CHECK (
            severity IN (
                'low',
                'medium',
                'high',
                'critical'
            )
        ),

    reason_codes JSONB NOT NULL,
    containment_action VARCHAR(150) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'open'
        CHECK (
            status IN (
                'open',
                'investigating',
                'contained',
                'resolved',
                'false_positive'
            )
        ),

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_security_incident_decision
        FOREIGN KEY (decision_id)
        REFERENCES public.security_decisions(decision_id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_security_decisions_actor
    ON public.security_decisions(actor_id);

CREATE INDEX IF NOT EXISTS idx_security_decisions_agent
    ON public.security_decisions(agent_id);

CREATE INDEX IF NOT EXISTS idx_security_decisions_session
    ON public.security_decisions(session_id);

CREATE INDEX IF NOT EXISTS idx_security_decisions_result
    ON public.security_decisions(final_decision);

CREATE INDEX IF NOT EXISTS idx_security_decisions_time
    ON public.security_decisions(evaluated_at);

CREATE INDEX IF NOT EXISTS idx_security_incidents_agent
    ON public.security_incidents(agent_id);

CREATE INDEX IF NOT EXISTS idx_security_incidents_severity
    ON public.security_incidents(severity);

CREATE INDEX IF NOT EXISTS idx_security_incidents_status
    ON public.security_incidents(status);

COMMIT;