BEGIN;

CREATE TABLE IF NOT EXISTS public.incidents (
    incident_id VARCHAR(50) PRIMARY KEY,

    incident_type VARCHAR(100) NOT NULL,

    severity VARCHAR(20) NOT NULL
        CHECK (
            severity IN (
                'low',
                'medium',
                'high',
                'critical'
            )
        ),

    source_agent VARCHAR(50) NOT NULL,

    detected_at TIMESTAMPTZ NOT NULL,

    affected_records INTEGER NOT NULL DEFAULT 0
        CHECK (affected_records >= 0),

    blocked_layer VARCHAR(100) NOT NULL,

    containment_action VARCHAR(100) NOT NULL,

    status VARCHAR(30) NOT NULL
        CHECK (
            status IN (
                'open',
                'investigating',
                'contained',
                'resolved',
                'false_positive'
            )
        ),

    CONSTRAINT fk_incidents_source_agent
        FOREIGN KEY (source_agent)
        REFERENCES public.agents(agent_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

COMMIT;