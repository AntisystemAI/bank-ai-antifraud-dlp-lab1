BEGIN;

CREATE TABLE IF NOT EXISTS public.documents (
    document_id VARCHAR(50) PRIMARY KEY,

    document_type VARCHAR(100) NOT NULL,

    classification VARCHAR(20) NOT NULL
        CHECK (
            classification IN (
                'public',
                'internal',
                'confidential',
                'restricted'
            )
        ),

    source_trust VARCHAR(30) NOT NULL
        CHECK (
            source_trust IN (
                'trusted_internal',
                'trusted_partner',
                'untrusted_external'
            )
        ),

    owner_department VARCHAR(100) NOT NULL,

    contains_untrusted_instruction BOOLEAN NOT NULL DEFAULT FALSE,

    contains_synthetic_marker BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS public.agent_events (
    event_id VARCHAR(50) PRIMARY KEY,

    session_id VARCHAR(50) NOT NULL,

    agent_id VARCHAR(50) NOT NULL,

    employee_id VARCHAR(50),

    event_time TIMESTAMPTZ NOT NULL,

    action VARCHAR(100) NOT NULL,

    tool_name VARCHAR(100),

    data_classification VARCHAR(20) NOT NULL
        CHECK (
            data_classification IN (
                'public',
                'internal',
                'confidential',
                'restricted'
            )
        ),

    record_count INTEGER NOT NULL DEFAULT 0
        CHECK (record_count >= 0),

    destination VARCHAR(150) NOT NULL,

    policy_decision VARCHAR(30) NOT NULL
        CHECK (
            policy_decision IN (
                'allow',
                'allow_with_masking',
                'limit',
                'require_approval',
                'review',
                'block',
                'quarantine'
            )
        ),

    risk_score SMALLINT NOT NULL
        CHECK (risk_score BETWEEN 0 AND 100),

    CONSTRAINT fk_agent_events_agent
        FOREIGN KEY (agent_id)
        REFERENCES public.agents(agent_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_agent_events_employee
        FOREIGN KEY (employee_id)
        REFERENCES public.employees(employee_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS public.tool_calls (
    call_id VARCHAR(50) PRIMARY KEY,

    agent_id VARCHAR(50) NOT NULL,

    tool_name VARCHAR(100) NOT NULL,

    requested_scope VARCHAR(200) NOT NULL,

    approved_scope VARCHAR(200),

    records_requested INTEGER NOT NULL DEFAULT 0
        CHECK (records_requested >= 0),

    decision VARCHAR(30) NOT NULL
        CHECK (
            decision IN (
                'allow',
                'allow_with_masking',
                'limit',
                'require_approval',
                'review',
                'block',
                'quarantine'
            )
        ),

    reason VARCHAR(500) NOT NULL,

    "timestamp" TIMESTAMPTZ NOT NULL,

    CONSTRAINT fk_tool_calls_agent
        FOREIGN KEY (agent_id)
        REFERENCES public.agents(agent_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

COMMIT;