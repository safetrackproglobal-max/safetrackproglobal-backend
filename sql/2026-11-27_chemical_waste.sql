-- Chemical safety part 2 (2026-11-27): chemical waste log.
CREATE TABLE IF NOT EXISTS chem_waste (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(40),
    contents TEXT,
    groups TEXT,
    quantity DOUBLE PRECISION,
    unit VARCHAR(12),
    location VARCHAR(160),
    started_on DATE NOT NULL,
    limit_days INTEGER NOT NULL DEFAULT 90,
    status VARCHAR(12) NOT NULL DEFAULT 'open',
    collected_on DATE,
    contractor VARCHAR(160),
    manifest_no VARCHAR(80),
    disposal_method VARCHAR(120),
    notes TEXT,
    notified_on DATE,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_chem_waste_company_id ON chem_waste (company_id);
