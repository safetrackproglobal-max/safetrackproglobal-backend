-- Daily Toolbox Talks (2026-11-23) — run once on the Railway PostgreSQL database.
CREATE TABLE IF NOT EXISTS toolbox_talks (
    id               SERIAL PRIMARY KEY,
    company_id       INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    created_by       INTEGER REFERENCES users(id) ON DELETE SET NULL,
    talk_date        DATE NOT NULL,
    mode             VARCHAR(10) NOT NULL DEFAULT 'auto',
    topic            VARCHAR(255),
    title            VARCHAR(255) NOT NULL,
    industry         VARCHAR(100),
    language         VARCHAR(20) DEFAULT 'en',
    duration_minutes INTEGER DEFAULT 10,
    content          TEXT NOT NULL,
    context_summary  TEXT,
    source           VARCHAR(20) DEFAULT 'ai',
    status           VARCHAR(20) NOT NULL DEFAULT 'generated',
    presenter        VARCHAR(120),
    location         VARCHAR(255),
    attendees        TEXT,
    attendee_count   INTEGER DEFAULT 0,
    notes            TEXT,
    delivered_at     TIMESTAMP,
    delivered_by     INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_toolbox_talks_company_id ON toolbox_talks (company_id);
CREATE INDEX IF NOT EXISTS ix_toolbox_talks_created_by ON toolbox_talks (created_by);
CREATE INDEX IF NOT EXISTS ix_toolbox_talks_talk_date  ON toolbox_talks (talk_date);
CREATE INDEX IF NOT EXISTS ix_toolbox_talks_company_date ON toolbox_talks (company_id, talk_date);
