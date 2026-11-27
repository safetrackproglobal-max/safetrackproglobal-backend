-- Chemical safety (2026-11-27): PubChem cache, company chemical register, test log.
CREATE TABLE IF NOT EXISTS chem_substances (
    id SERIAL PRIMARY KEY,
    cid INTEGER UNIQUE,
    name VARCHAR(200) NOT NULL,
    cas VARCHAR(40),
    formula VARCHAR(120),
    data TEXT,
    fetched_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_chem_substances_cid ON chem_substances (cid);
CREATE INDEX IF NOT EXISTS ix_chem_substances_cas ON chem_substances (cas);
CREATE TABLE IF NOT EXISTS chem_items (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    substance_id INTEGER REFERENCES chem_substances(id) ON DELETE SET NULL,
    name VARCHAR(200) NOT NULL,
    cas VARCHAR(40),
    location VARCHAR(160),
    quantity DOUBLE PRECISION,
    unit VARCHAR(12),
    containers INTEGER,
    supplier VARCHAR(160),
    groups TEXT,
    groups_confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    peroxide_class VARCHAR(2),
    received_on DATE,
    opened_on DATE,
    expires_on DATE,
    status VARCHAR(12) NOT NULL DEFAULT 'in_use',
    notes TEXT,
    sds_file VARCHAR(60),
    sds_mime VARCHAR(40),
    sds_uploaded_at TIMESTAMP,
    legacy_id INTEGER,
    notified_on DATE,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_chem_items_company_id ON chem_items (company_id);
CREATE TABLE IF NOT EXISTS chem_tests (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    item_id INTEGER NOT NULL REFERENCES chem_items(id) ON DELETE CASCADE,
    kind VARCHAR(20) NOT NULL DEFAULT 'peroxide',
    tested_on DATE NOT NULL,
    result_ppm DOUBLE PRECISION,
    result VARCHAR(300),
    tested_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_chem_tests_company_id ON chem_tests (company_id);
CREATE INDEX IF NOT EXISTS ix_chem_tests_item_id ON chem_tests (item_id);
