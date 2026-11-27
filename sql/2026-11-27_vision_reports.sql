-- Safety vision (2026-11-27): hazard reports from photos / videos with the 43-class model.
CREATE TABLE IF NOT EXISTS vision_reports (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(200),
    location VARCHAR(200),
    site_type VARCHAR(20),
    kind VARCHAR(8) NOT NULL,
    source_name VARCHAR(200),
    findings TEXT,
    summary TEXT,
    files TEXT,
    model_version VARCHAR(80),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_vision_reports_company_id ON vision_reports (company_id);
CREATE INDEX IF NOT EXISTS ix_vision_reports_user_id ON vision_reports (user_id);
