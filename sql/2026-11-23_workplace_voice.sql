-- Workplace Voice (2026-11-23) — run once on the Railway PostgreSQL database.
CREATE TABLE IF NOT EXISTS wv_channels (
    id                 SERIAL PRIMARY KEY,
    company_id         INTEGER NOT NULL UNIQUE REFERENCES companies(id) ON DELETE CASCADE,
    slug               VARCHAR(80) NOT NULL UNIQUE,
    enabled            BOOLEAN NOT NULL DEFAULT TRUE,
    listed             BOOLEAN NOT NULL DEFAULT TRUE,
    welcome_message    TEXT,
    languages          TEXT,
    preferred_language VARCHAR(10) DEFAULT 'en',
    allow_anonymous    BOOLEAN NOT NULL DEFAULT TRUE,
    allow_protected    BOOLEAN NOT NULL DEFAULT TRUE,
    allow_open         BOOLEAN NOT NULL DEFAULT TRUE,
    show_projects      BOOLEAN NOT NULL DEFAULT FALSE,
    created_by         INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at         TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS wv_routes (
    id           SERIAL PRIMARY KEY,
    company_id   INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    project_id   INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    report_group VARCHAR(20) NOT NULL DEFAULT 'all',
    user_ids     TEXT NOT NULL DEFAULT '[]',
    created_by   INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_wv_routes_company_id ON wv_routes (company_id);
CREATE INDEX IF NOT EXISTS ix_wv_routes_project_id ON wv_routes (project_id);

CREATE TABLE IF NOT EXISTS wv_reports (
    id                SERIAL PRIMARY KEY,
    company_id        INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    project_id        INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    tracking_code     VARCHAR(20) NOT NULL UNIQUE,
    report_group      VARCHAR(20) NOT NULL DEFAULT 'safety',
    category          VARCHAR(40),
    input_method      VARCHAR(20),
    language_selected VARCHAR(10),
    language_detected VARCHAR(40),
    original_text     TEXT,
    english_text      TEXT,
    translated_text   TEXT,
    title             VARCHAR(255),
    summary           TEXT,
    details           TEXT,
    evidence          TEXT,
    photo_findings    TEXT,
    risk_level        VARCHAR(10),
    severity_score    INTEGER,
    priority_score    INTEGER,
    response_hours    INTEGER,
    response_due_at   TIMESTAMP,
    anonymity         VARCHAR(12) NOT NULL DEFAULT 'anonymous',
    reporter_name     VARCHAR(120),
    reporter_contact  VARCHAR(160),
    status            VARCHAR(20) NOT NULL DEFAULT 'received',
    assigned_user_ids TEXT DEFAULT '[]',
    timeline          TEXT DEFAULT '[]',
    action_taken      TEXT,
    tbt_id            INTEGER,
    capa_id           INTEGER,
    ai_status         VARCHAR(12) DEFAULT 'pending',
    ai_error          VARCHAR(255),
    ip_hash           VARCHAR(64),
    first_response_at TIMESTAMP,
    closed_at         TIMESTAMP,
    created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_wv_reports_company_id ON wv_reports (company_id);
CREATE INDEX IF NOT EXISTS ix_wv_reports_project_id ON wv_reports (project_id);
CREATE INDEX IF NOT EXISTS ix_wv_reports_status     ON wv_reports (status);
CREATE INDEX IF NOT EXISTS ix_wv_reports_ip_hash    ON wv_reports (ip_hash);
CREATE INDEX IF NOT EXISTS ix_wv_reports_created_at ON wv_reports (created_at);

CREATE TABLE IF NOT EXISTS wv_identities (
    id         SERIAL PRIMARY KEY,
    report_id  INTEGER NOT NULL UNIQUE REFERENCES wv_reports(id) ON DELETE CASCADE,
    name       VARCHAR(120),
    contact    VARCHAR(160),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ---------------------------------------------------------------------------
-- Rewards (Safety Impact Score), repeated-report detection, abuse controls
-- (safe to run even if the part above was already applied)
-- ---------------------------------------------------------------------------
ALTER TABLE wv_channels ADD COLUMN IF NOT EXISTS rewards_enabled  BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE wv_channels ADD COLUMN IF NOT EXISTS show_leaderboard BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE wv_channels ADD COLUMN IF NOT EXISTS rewards_note     TEXT;

ALTER TABLE wv_reports ADD COLUMN IF NOT EXISTS net_hash          VARCHAR(64);
ALTER TABLE wv_reports ADD COLUMN IF NOT EXISTS reward_account_id INTEGER;
ALTER TABLE wv_reports ADD COLUMN IF NOT EXISTS duplicate_of      INTEGER;
ALTER TABLE wv_reports ADD COLUMN IF NOT EXISTS duplicate_count   INTEGER DEFAULT 0;
ALTER TABLE wv_reports ADD COLUMN IF NOT EXISTS fingerprint       VARCHAR(64);
CREATE INDEX IF NOT EXISTS ix_wv_reports_net_hash          ON wv_reports (net_hash);
CREATE INDEX IF NOT EXISTS ix_wv_reports_reward_account_id ON wv_reports (reward_account_id);
CREATE INDEX IF NOT EXISTS ix_wv_reports_duplicate_of      ON wv_reports (duplicate_of);
CREATE INDEX IF NOT EXISTS ix_wv_reports_fingerprint       ON wv_reports (fingerprint);

CREATE TABLE IF NOT EXISTS wv_reward_accounts (
    id                  SERIAL PRIMARY KEY,
    company_id          INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    reward_code         VARCHAR(20) NOT NULL UNIQUE,
    pin_hash            VARCHAR(255) NOT NULL,
    alias               VARCHAR(40) NOT NULL,
    points              INTEGER NOT NULL DEFAULT 0,
    redeemed_points     INTEGER NOT NULL DEFAULT 0,
    reports_count       INTEGER NOT NULL DEFAULT 0,
    failed_pin_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until        TIMESTAMP,
    last_report_at      TIMESTAMP,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_wv_reward_accounts_company_id ON wv_reward_accounts (company_id);

CREATE TABLE IF NOT EXISTS wv_reward_events (
    id         SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES wv_reward_accounts(id) ON DELETE CASCADE,
    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    report_id  INTEGER REFERENCES wv_reports(id) ON DELETE SET NULL,
    kind       VARCHAR(30) NOT NULL,
    points     INTEGER NOT NULL,
    note       VARCHAR(255),
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_wv_reward_report_kind UNIQUE (report_id, kind)
);
CREATE INDEX IF NOT EXISTS ix_wv_reward_events_account_id ON wv_reward_events (account_id);
CREATE INDEX IF NOT EXISTS ix_wv_reward_events_company_id ON wv_reward_events (company_id);
CREATE INDEX IF NOT EXISTS ix_wv_reward_events_report_id  ON wv_reward_events (report_id);
CREATE INDEX IF NOT EXISTS ix_wv_reward_events_created_at ON wv_reward_events (created_at);
