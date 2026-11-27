-- Inspections & checklists (2026-11-27).
CREATE TABLE IF NOT EXISTS inspection_templates (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(160) NOT NULL,
    category VARCHAR(60),
    description VARCHAR(500),
    items TEXT NOT NULL,
    source VARCHAR(40),
    archived BOOLEAN NOT NULL DEFAULT FALSE,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_inspection_templates_company_id ON inspection_templates (company_id);
CREATE TABLE IF NOT EXISTS inspection_schedules (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    template_id INTEGER REFERENCES inspection_templates(id) ON DELETE CASCADE,
    library_key VARCHAR(40),
    title VARCHAR(200) NOT NULL,
    site VARCHAR(200),
    assignee_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    frequency VARCHAR(12) NOT NULL DEFAULT 'weekly',
    next_due DATE NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    notified_on DATE,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_inspection_schedules_company_id ON inspection_schedules (company_id);
CREATE TABLE IF NOT EXISTS inspections (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    template_id INTEGER REFERENCES inspection_templates(id) ON DELETE SET NULL,
    library_key VARCHAR(40),
    schedule_id INTEGER REFERENCES inspection_schedules(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    site VARCHAR(200),
    inspector_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(12) NOT NULL DEFAULT 'in_progress',
    items TEXT NOT NULL,
    answers TEXT,
    score INTEGER,
    max_score INTEGER,
    failed_count INTEGER NOT NULL DEFAULT 0,
    critical_failed INTEGER NOT NULL DEFAULT 0,
    note TEXT,
    signed_name VARCHAR(160),
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_inspections_company_id ON inspections (company_id);
CREATE INDEX IF NOT EXISTS ix_inspections_inspector_id ON inspections (inspector_id);
CREATE TABLE IF NOT EXISTS inspection_photos (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    inspection_id INTEGER NOT NULL REFERENCES inspections(id) ON DELETE CASCADE,
    item_id VARCHAR(20),
    file_name VARCHAR(60) NOT NULL,
    file_mime VARCHAR(30) NOT NULL,
    uploaded_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_inspection_photos_company_id ON inspection_photos (company_id);
CREATE INDEX IF NOT EXISTS ix_inspection_photos_inspection_id ON inspection_photos (inspection_id);
CREATE TABLE IF NOT EXISTS inspection_actions (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    inspection_id INTEGER NOT NULL REFERENCES inspections(id) ON DELETE CASCADE,
    item_id VARCHAR(20),
    title VARCHAR(300) NOT NULL,
    detail TEXT,
    priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    assignee_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    due_date DATE,
    status VARCHAR(10) NOT NULL DEFAULT 'open',
    done_note TEXT,
    done_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    done_at TIMESTAMP,
    verified_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    verified_at TIMESTAMP,
    notified_on DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_inspection_actions_company_id ON inspection_actions (company_id);
CREATE INDEX IF NOT EXISTS ix_inspection_actions_inspection_id ON inspection_actions (inspection_id);
CREATE INDEX IF NOT EXISTS ix_inspection_actions_assignee_id ON inspection_actions (assignee_id);
