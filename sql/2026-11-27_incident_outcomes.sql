-- Safety KPIs (2026-11-27): injury outcome of each incident, for TRIR / DART / LTIFR / severity rate.
CREATE TABLE IF NOT EXISTS incident_outcomes (
    incident_id INTEGER PRIMARY KEY REFERENCES incidents(id) ON DELETE CASCADE,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    outcome VARCHAR(16) NOT NULL,
    days_lost INTEGER NOT NULL DEFAULT 0,
    days_restricted INTEGER NOT NULL DEFAULT 0,
    updated_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_incident_outcomes_company_id ON incident_outcomes (company_id);
