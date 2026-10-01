BEGIN;

CREATE TABLE IF NOT EXISTS public.employees (
    employee_id VARCHAR(50) PRIMARY KEY,

    department VARCHAR(100) NOT NULL,

    role VARCHAR(100) NOT NULL,

    access_level VARCHAR(20) NOT NULL
        CHECK (
            access_level IN (
                'basic',
                'standard',
                'elevated',
                'privileged'
            )
        ),

    work_region VARCHAR(50) NOT NULL,

    status VARCHAR(20) NOT NULL
        CHECK (
            status IN (
                'active',
                'suspended',
                'disabled'
            )
        ),

    allowed_tools JSONB NOT NULL DEFAULT '[]'::jsonb,

    CONSTRAINT chk_employees_allowed_tools_array
        CHECK (jsonb_typeof(allowed_tools) = 'array')
);

CREATE TABLE IF NOT EXISTS public.agents (
    agent_id VARCHAR(50) PRIMARY KEY,

    agent_type VARCHAR(100) NOT NULL,

    owner_department VARCHAR(100) NOT NULL,

    trust_level VARCHAR(20) NOT NULL
        CHECK (
            trust_level IN (
                'low',
                'medium',
                'high'
            )
        ),

    permission_profile VARCHAR(100) NOT NULL,

    allowed_tools JSONB NOT NULL DEFAULT '[]'::jsonb,

    data_access_level VARCHAR(20) NOT NULL
        CHECK (
            data_access_level IN (
                'public',
                'internal',
                'confidential',
                'restricted'
            )
        ),

    status VARCHAR(20) NOT NULL
        CHECK (
            status IN (
                'active',
                'suspended',
                'disabled'
            )
        ),

    CONSTRAINT chk_agents_allowed_tools_array
        CHECK (jsonb_typeof(allowed_tools) = 'array')
);

COMMIT;