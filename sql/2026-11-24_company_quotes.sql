-- Agreed price per company (set by the SafeTrack Pro team) and price requests from company admins.
CREATE TABLE IF NOT EXISTS company_quotes (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    plan VARCHAR(32) NOT NULL DEFAULT 'enterprise',
    billing_cycle VARCHAR(20) NOT NULL DEFAULT '1_year',
    amount NUMERIC(12,2),
    currency VARCHAR(8),
    status VARCHAR(20) NOT NULL DEFAULT 'requested',
    request_note TEXT,
    note TEXT,
    requested_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    last_paid_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_company_quotes_company_status ON company_quotes (company_id, status);
CREATE UNIQUE INDEX IF NOT EXISTS uq_company_quotes_one_active ON company_quotes (company_id) WHERE status = 'active';
