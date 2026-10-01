BEGIN;

CREATE TABLE IF NOT EXISTS public.customers (
    customer_id VARCHAR(50) PRIMARY KEY,

    customer_segment VARCHAR(20) NOT NULL
        CHECK (
            customer_segment IN (
                'mass',
                'premium',
                'business',
                'private'
            )
        ),

    age_group VARCHAR(20) NOT NULL
        CHECK (
            age_group IN (
                '18-24',
                '25-34',
                '35-44',
                '45-54',
                '55-64',
                '65_plus'
            )
        ),

    region VARCHAR(50) NOT NULL,

    risk_level VARCHAR(10) NOT NULL
        CHECK (
            risk_level IN (
                'low',
                'medium',
                'high'
            )
        ),

    kyc_status VARCHAR(20) NOT NULL
        CHECK (
            kyc_status IN (
                'verified',
                'pending',
                'restricted',
                'expired'
            )
        ),

    registration_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS public.accounts (
    account_id VARCHAR(50) PRIMARY KEY,

    customer_id VARCHAR(50) NOT NULL,

    account_type VARCHAR(20) NOT NULL
        CHECK (
            account_type IN (
                'debit',
                'credit',
                'savings',
                'business'
            )
        ),

    currency VARCHAR(3) NOT NULL
        CHECK (
            currency IN (
                'RUB',
                'USD',
                'EUR'
            )
        ),

    status VARCHAR(20) NOT NULL
        CHECK (
            status IN (
                'active',
                'restricted',
                'blocked',
                'closed'
            )
        ),

    daily_limit NUMERIC(15, 2) NOT NULL
        CHECK (daily_limit >= 0),

    opening_date DATE NOT NULL,

    CONSTRAINT fk_accounts_customer
        FOREIGN KEY (customer_id)
        REFERENCES public.customers(customer_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

COMMIT;