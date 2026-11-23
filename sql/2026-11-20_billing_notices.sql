-- Billing notices table (models.BillingNotice) — PostgreSQL
-- Safe to run more than once. Run on the Railway database BEFORE or right after deploying.
-- Until it exists the billing job just logs "table billing_notices missing" and does nothing else.

CREATE TABLE IF NOT EXISTS billing_notices (
    id           SERIAL PRIMARY KEY,
    subject_key  VARCHAR(40)  NOT NULL,                                   -- 'user:<id>' or 'company:<id>'
    user_id      INTEGER      REFERENCES users(id)     ON DELETE CASCADE,
    company_id   INTEGER      REFERENCES companies(id) ON DELETE CASCADE,
    notice_type  VARCHAR(32)  NOT NULL,                                   -- activated | due_7 | due_3 | due_1 | due_today | expired
    period_key   VARCHAR(32)  NOT NULL,                                   -- billing period end date YYYY-MM-DD
    recipients   TEXT,
    status       VARCHAR(16)  NOT NULL DEFAULT 'pending',                 -- pending | sent | failed
    attempts     INTEGER      NOT NULL DEFAULT 0,
    last_error   TEXT,
    claimed_at   TIMESTAMP,
    sent_at      TIMESTAMP,
    created_at   TIMESTAMP    NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_billing_notice UNIQUE (subject_key, notice_type, period_key)
);

CREATE INDEX IF NOT EXISTS ix_billing_notices_user_id    ON billing_notices (user_id);
CREATE INDEX IF NOT EXISTS ix_billing_notices_company_id ON billing_notices (company_id);

-- Check:
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'billing_notices';
