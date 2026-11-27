-- Oil & gas (2026-11-27): isolations on permits, gas tests, management of change, bypassed safety devices, zones.
CREATE TABLE IF NOT EXISTS og_isolations (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    permit_id INTEGER NOT NULL REFERENCES work_permits(id) ON DELETE CASCADE,
    point_tag VARCHAR(80) NOT NULL,
    equipment VARCHAR(200),
    energy_type VARCHAR(20) NOT NULL,
    method VARCHAR(30) NOT NULL,
    lock_no VARCHAR(40),
    status VARCHAR(12) NOT NULL DEFAULT 'isolated',
    isolated_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    isolated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    verified_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    verified_at TIMESTAMP,
    verify_note VARCHAR(300),
    removed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    removed_at TIMESTAMP,
    note VARCHAR(500)
);
CREATE INDEX IF NOT EXISTS ix_og_isolations_company_id ON og_isolations (company_id);
CREATE INDEX IF NOT EXISTS ix_og_isolations_permit_id ON og_isolations (permit_id);
CREATE TABLE IF NOT EXISTS og_gas_tests (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    permit_id INTEGER REFERENCES work_permits(id) ON DELETE SET NULL,
    location VARCHAR(200),
    tested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    o2 DOUBLE PRECISION,
    lel DOUBLE PRECISION,
    h2s DOUBLE PRECISION,
    co DOUBLE PRECISION,
    other_name VARCHAR(60),
    other_value DOUBLE PRECISION,
    other_limit DOUBLE PRECISION,
    instrument_id INTEGER REFERENCES equipment_items(id) ON DELETE SET NULL,
    instrument_text VARCHAR(120),
    result VARCHAR(6) NOT NULL,
    reasons TEXT,
    limits TEXT,
    tested_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_og_gas_tests_company_id ON og_gas_tests (company_id);
CREATE INDEX IF NOT EXISTS ix_og_gas_tests_permit_id ON og_gas_tests (permit_id);
CREATE TABLE IF NOT EXISTS og_mocs (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    number VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    change_type VARCHAR(20) NOT NULL,
    temporary BOOLEAN NOT NULL DEFAULT FALSE,
    expires_on DATE,
    location VARCHAR(200),
    description TEXT,
    technical_basis TEXT,
    safety_impact TEXT,
    procedures_affected TEXT,
    risk_level VARCHAR(10),
    needs_pssr BOOLEAN NOT NULL DEFAULT TRUE,
    training_done BOOLEAN NOT NULL DEFAULT FALSE,
    psi_updated BOOLEAN NOT NULL DEFAULT FALSE,
    procedures_updated BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(12) NOT NULL DEFAULT 'draft',
    owner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    approved_at TIMESTAMP,
    decision_note VARCHAR(1000),
    implemented_at TIMESTAMP,
    pssr_inspection_id INTEGER,
    closed_at TIMESTAMP,
    notified_on DATE,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_og_mocs_company_number UNIQUE (company_id, number)
);
CREATE INDEX IF NOT EXISTS ix_og_mocs_company_id ON og_mocs (company_id);
CREATE TABLE IF NOT EXISTS og_bypasses (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    device_tag VARCHAR(80) NOT NULL,
    device_type VARCHAR(20) NOT NULL,
    location VARCHAR(200),
    reason VARCHAR(1000) NOT NULL,
    mitigation VARCHAR(1000) NOT NULL,
    authorised_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    start_at TIMESTAMP NOT NULL DEFAULT NOW(),
    planned_end TIMESTAMP NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    removed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    removed_at TIMESTAMP,
    removal_note VARCHAR(500),
    notified_on DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_og_bypasses_company_id ON og_bypasses (company_id);
CREATE TABLE IF NOT EXISTS og_zones (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(160) NOT NULL,
    zone_type VARCHAR(20) NOT NULL,
    description VARCHAR(1000),
    requirements TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_og_zones_company_id ON og_zones (company_id);
