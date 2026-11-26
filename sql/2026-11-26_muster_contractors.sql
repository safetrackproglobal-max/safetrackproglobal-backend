-- Evacuation roll call and contractor management.
CREATE TABLE IF NOT EXISTS muster_events (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    kind VARCHAR(10) NOT NULL DEFAULT 'drill',
    reason VARCHAR(300),
    site VARCHAR(200),
    assembly_point VARCHAR(200),
    status VARCHAR(10) NOT NULL DEFAULT 'open',
    started_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    closed_at TIMESTAMP,
    close_note TEXT,
    summary TEXT
);
CREATE INDEX IF NOT EXISTS ix_muster_events_company_id ON muster_events (company_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_muster_one_open ON muster_events (company_id) WHERE status = 'open';
CREATE TABLE IF NOT EXISTS muster_marks (
    id SERIAL PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES muster_events(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    person_name VARCHAR(160),
    status VARCHAR(10) NOT NULL,
    note VARCHAR(300),
    marked_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    marked_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_muster_marks_event_id ON muster_marks (event_id);
CREATE UNIQUE INDEX IF NOT EXISTS uq_muster_mark_user ON muster_marks (event_id, user_id) WHERE user_id IS NOT NULL;
CREATE TABLE IF NOT EXISTS contractor_firms (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    trade VARCHAR(120),
    contact_name VARCHAR(120),
    contact_email VARCHAR(200),
    contact_phone VARCHAR(40),
    status VARCHAR(12) NOT NULL DEFAULT 'pending',
    prequal TEXT,
    notes TEXT,
    approved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    approved_at TIMESTAMP,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_contractor_firms_company_id ON contractor_firms (company_id);
CREATE TABLE IF NOT EXISTS contractor_workers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    firm_id INTEGER NOT NULL REFERENCES contractor_firms(id) ON DELETE CASCADE,
    name VARCHAR(160) NOT NULL,
    role VARCHAR(120),
    phone VARCHAR(40),
    inducted_on DATE,
    induction_valid_until DATE,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_contractor_workers_company_id ON contractor_workers (company_id);
CREATE INDEX IF NOT EXISTS ix_contractor_workers_firm_id ON contractor_workers (firm_id);
CREATE TABLE IF NOT EXISTS contractor_docs (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    firm_id INTEGER NOT NULL REFERENCES contractor_firms(id) ON DELETE CASCADE,
    worker_id INTEGER REFERENCES contractor_workers(id) ON DELETE CASCADE,
    doc_type VARCHAR(30) NOT NULL,
    title VARCHAR(200),
    number VARCHAR(100),
    expires_on DATE,
    file_name VARCHAR(200),
    file_mime VARCHAR(60),
    notified_stage INTEGER NOT NULL DEFAULT 0,
    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_contractor_docs_company_id ON contractor_docs (company_id);
CREATE INDEX IF NOT EXISTS ix_contractor_docs_firm_id ON contractor_docs (firm_id);
CREATE INDEX IF NOT EXISTS ix_contractor_docs_worker_id ON contractor_docs (worker_id);
CREATE INDEX IF NOT EXISTS ix_contractor_docs_expiry ON contractor_docs (expires_on, notified_stage);
