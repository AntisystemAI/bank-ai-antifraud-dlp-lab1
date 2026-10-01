BEGIN;

CREATE TABLE IF NOT EXISTS public.transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,

    account_id VARCHAR(50) NOT NULL,

    transaction_time TIMESTAMPTZ NOT NULL,

    amount NUMERIC(15, 2) NOT NULL
        CHECK (amount > 0),

    currency VARCHAR(3) NOT NULL
        CHECK (
            currency IN (
                'RUB',
                'USD',
                'EUR'
            )
        ),

    channel VARCHAR(20) NOT NULL
        CHECK (
            channel IN (
                'mobile_app',
                'web',
                'atm',
                'branch',
                'api'
            )
        ),

    merchant_category VARCHAR(50) NOT NULL
        CHECK (
            merchant_category IN (
                'retail',
                'travel',
                'transport',
                'utilities',
                'telecom',
                'entertainment',
                'financial_services',
                'government',
                'other'
            )
        ),

    recipient_type VARCHAR(20) NOT NULL
        CHECK (
            recipient_type IN (
                'individual',
                'company',
                'government',
                'self_transfer'
            )
        ),

    device_id VARCHAR(50) NOT NULL,

    region VARCHAR(50) NOT NULL,

    risk_score SMALLINT NOT NULL
        CHECK (risk_score BETWEEN 0 AND 100),

    fraud_label BOOLEAN NOT NULL DEFAULT FALSE,

    review_status VARCHAR(30) NOT NULL
        CHECK (
            review_status IN (
                'not_required',
                'pending',
                'in_review',
                'confirmed_legitimate',
                'confirmed_fraud'
            )
        ),

    CONSTRAINT fk_transactions_account
        FOREIGN KEY (account_id)
        REFERENCES public.accounts(account_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

COMMIT;