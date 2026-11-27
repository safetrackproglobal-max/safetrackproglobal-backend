-- Equipment register and QR safety tags (2026-11-27).
CREATE TABLE IF NOT EXISTS equipment_items (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    tag_no VARCHAR(20) NOT NULL,
    qr_token VARCHAR(32) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(30) NOT NULL DEFAULT 'other',
    make VARCHAR(120),
    model VARCHAR(120),
    serial_no VARCHAR(120),
    location VARCHAR(160),
    ownership VARCHAR(12) NOT NULL DEFAULT 'owned',
    supplier VARCHAR(160),
    arrived_on DATE,
    checklist_ref VARCHAR(40),
    inspect_every_days INTEGER,
    next_due DATE,
    cert_name VARCHAR(120),
    cert_due DATE,
    status VARCHAR(16) NOT NULL DEFAULT 'in_service',
    status_reason VARCHAR(500),
    last_inspection_id INTEGER,
    last_inspected_at TIMESTAMP,
    last_result VARCHAR(10),
    notes TEXT,
    notified_on DATE,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_equipment_items_company_tag UNIQUE (company_id, tag_no)
);
CREATE INDEX IF NOT EXISTS ix_equipment_items_company_id ON equipment_items (company_id);
CREATE INDEX IF NOT EXISTS ix_equipment_items_qr_token ON equipment_items (qr_token);
CREATE TABLE IF NOT EXISTS equipment_inspections (
    inspection_id INTEGER PRIMARY KEY REFERENCES inspections(id) ON DELETE CASCADE,
    equipment_id INTEGER NOT NULL REFERENCES equipment_items(id) ON DELETE CASCADE,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_equipment_inspections_equipment_id ON equipment_inspections (equipment_id);
CREATE INDEX IF NOT EXISTS ix_equipment_inspections_company_id ON equipment_inspections (company_id);
CREATE TABLE IF NOT EXISTS equipment_log (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    equipment_id INTEGER NOT NULL REFERENCES equipment_items(id) ON DELETE CASCADE,
    kind VARCHAR(16) NOT NULL,
    text VARCHAR(600) NOT NULL,
    inspection_id INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_equipment_log_company_id ON equipment_log (company_id);
CREATE INDEX IF NOT EXISTS ix_equipment_log_equipment_id ON equipment_log (equipment_id);
