-- =====================================================================================
-- FULL DEPLOY SQL — 2026-11-23. Run ONCE on the Railway PostgreSQL database (Query tab).
-- Covers every database change made since the live version of 2026-11-16.
-- Every statement is safe to run again (IF NOT EXISTS / IF EXISTS).
-- =====================================================================================


-- -------------------------------------------------------------------------------------
-- Audit log table (2026-11-20)
-- -------------------------------------------------------------------------------------
-- AuditLog model (models.py) — general audit trail used by app.py.
-- Safe to run more than once.
CREATE TABLE IF NOT EXISTS audit_logs (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NULL REFERENCES users(id) ON DELETE SET NULL,
    target_user_id  INTEGER NULL,
    hospital_id     INTEGER NULL,
    action          VARCHAR(100) NOT NULL,
    resource_type   VARCHAR(64)  NULL,
    resource_id     VARCHAR(255) NULL,
    details         TEXT NULL,
    ip_address      VARCHAR(64)  NULL,
    user_agent      TEXT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc')
);

CREATE INDEX IF NOT EXISTS ix_audit_logs_user_id        ON audit_logs (user_id);
CREATE INDEX IF NOT EXISTS ix_audit_logs_target_user_id ON audit_logs (target_user_id);
CREATE INDEX IF NOT EXISTS ix_audit_logs_hospital_id    ON audit_logs (hospital_id);
CREATE INDEX IF NOT EXISTS ix_audit_logs_action         ON audit_logs (action);
CREATE INDEX IF NOT EXISTS ix_audit_logs_created_at     ON audit_logs (created_at);


-- -------------------------------------------------------------------------------------
-- Billing notices (2026-11-20)
-- -------------------------------------------------------------------------------------
-- Billing notices table (models.BillingNotice) — PostgreSQL
-- Safe to run more than once. Run on the Railway database BEFORE or right after deploying.
-- Until it exists the billing job just logs "table billing_notices missing" and does nothing else.

CREATE TABLE IF NOT EXISTS billing_notices (
    id           SERIAL PRIMARY KEY,
    subject_key  VARCHAR(40)  NOT NULL,                                   -- 'user:<id>' or 'company:<id>'
    user_id      INTEGER      REFERENCES users(id)     ON DELETE CASCADE,
    company_id   INTEGER      REFERENCES companies(id) ON DELETE CASCADE,
    notice_type  VARCHAR(32)  NOT NULL,                                   -- activated | due_7 | due_3 | due_1 | due_today | expired
    period_key   VARCHAR(32)  NOT NULL,                                   -- billing period end date YYYY-MM-DD
    recipients   TEXT,
    status       VARCHAR(16)  NOT NULL DEFAULT 'pending',                 -- pending | sent | failed
    attempts     INTEGER      NOT NULL DEFAULT 0,
    last_error   TEXT,
    claimed_at   TIMESTAMP,
    sent_at      TIMESTAMP,
    created_at   TIMESTAMP    NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_billing_notice UNIQUE (subject_key, notice_type, period_key)
);

CREATE INDEX IF NOT EXISTS ix_billing_notices_user_id    ON billing_notices (user_id);
CREATE INDEX IF NOT EXISTS ix_billing_notices_company_id ON billing_notices (company_id);

-- Check:
-- SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'billing_notices';


-- -------------------------------------------------------------------------------------
-- Document control: clients, submissions, signing, permits (2026-11-21)
-- -------------------------------------------------------------------------------------
-- Document submission & signing cycle (models.py: ClientOrganization, ClientMember,
-- DocumentSubmission, SubmissionSigner, SigningAsset). Safe to run more than once.

CREATE TABLE IF NOT EXISTS client_organizations (
    id            SERIAL PRIMARY KEY,
    company_id    INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name          VARCHAR(255) NOT NULL,
    project_name  VARCHAR(255),
    contact_email VARCHAR(255),
    notes         TEXT,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_by    INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at    TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    CONSTRAINT uq_client_org_company_name UNIQUE (company_id, name)
);
CREATE INDEX IF NOT EXISTS ix_client_organizations_company_id ON client_organizations (company_id);

CREATE TABLE IF NOT EXISTS client_members (
    id                SERIAL PRIMARY KEY,
    client_org_id     INTEGER NOT NULL REFERENCES client_organizations(id) ON DELETE CASCADE,
    company_id        INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    user_id           INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_title         VARCHAR(128),
    status            VARCHAR(20) NOT NULL DEFAULT 'invited',
    invite_token_hash VARCHAR(128),
    invite_expires_at TIMESTAMP,
    invited_by        INTEGER REFERENCES users(id) ON DELETE SET NULL,
    invited_at        TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    accepted_at       TIMESTAMP,
    CONSTRAINT uq_client_member_org_user UNIQUE (client_org_id, user_id)
);
CREATE INDEX IF NOT EXISTS ix_client_members_client_org_id ON client_members (client_org_id);
CREATE INDEX IF NOT EXISTS ix_client_members_company_id ON client_members (company_id);
CREATE INDEX IF NOT EXISTS ix_client_members_user_id ON client_members (user_id);
CREATE INDEX IF NOT EXISTS ix_client_members_invite_token_hash ON client_members (invite_token_hash);

CREATE TABLE IF NOT EXISTS document_submissions (
    id               SERIAL PRIMARY KEY,
    reference        VARCHAR(40) NOT NULL UNIQUE,
    document_id      INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    company_id       INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    client_org_id    INTEGER REFERENCES client_organizations(id) ON DELETE SET NULL,
    title            VARCHAR(255) NOT NULL,
    message          TEXT,
    status           VARCHAR(30) NOT NULL DEFAULT 'in_review',
    current_order    INTEGER NOT NULL DEFAULT 1,
    due_date         TIMESTAMP,
    submitted_by     INTEGER REFERENCES users(id) ON DELETE SET NULL,
    submitted_at     TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    completed_at     TIMESTAMP,
    base_version     INTEGER,
    final_file_url   VARCHAR(500),
    final_file_hash  VARCHAR(128),
    in_approved_list BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at       TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc')
);
CREATE INDEX IF NOT EXISTS ix_document_submissions_document_id ON document_submissions (document_id);
CREATE INDEX IF NOT EXISTS ix_document_submissions_company_id ON document_submissions (company_id);
CREATE INDEX IF NOT EXISTS ix_document_submissions_status ON document_submissions (status);

CREATE TABLE IF NOT EXISTS submission_signers (
    id               SERIAL PRIMARY KEY,
    submission_id    INTEGER NOT NULL REFERENCES document_submissions(id) ON DELETE CASCADE,
    sign_order       INTEGER NOT NULL DEFAULT 1,
    user_id          INTEGER REFERENCES users(id) ON DELETE SET NULL,
    name             VARCHAR(255) NOT NULL,
    email            VARCHAR(255) NOT NULL,
    organization     VARCHAR(255),
    signer_type      VARCHAR(20) NOT NULL DEFAULT 'internal',
    action           VARCHAR(20) NOT NULL DEFAULT 'sign',
    status           VARCHAR(20) NOT NULL DEFAULT 'waiting',
    comment          TEXT,
    notified_at      TIMESTAMP,
    reminder_count   INTEGER NOT NULL DEFAULT 0,
    viewed_at        TIMESTAMP,
    acted_at         TIMESTAMP,
    ip_address       VARCHAR(64),
    user_agent       VARCHAR(512),
    signed_file_hash VARCHAR(128)
);
CREATE INDEX IF NOT EXISTS ix_submission_signers_submission_id ON submission_signers (submission_id);
CREATE INDEX IF NOT EXISTS ix_submission_signers_user_id ON submission_signers (user_id);

CREATE TABLE IF NOT EXISTS signing_assets (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    kind       VARCHAR(20) NOT NULL,
    label      VARCHAR(120),
    file_path  VARCHAR(500) NOT NULL,
    width      INTEGER,
    height     INTEGER,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc')
);
CREATE INDEX IF NOT EXISTS ix_signing_assets_user_id ON signing_assets (user_id);

-- Permit to work register (models.py: WorkPermit)
CREATE TABLE IF NOT EXISTS work_permits (
    id               SERIAL PRIMARY KEY,
    company_id       INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    permit_number    VARCHAR(40) NOT NULL,
    permit_type      VARCHAR(40) NOT NULL,
    title            VARCHAR(255) NOT NULL,
    location         VARCHAR(255),
    work_description TEXT,
    start_at         TIMESTAMP,
    end_at           TIMESTAMP,
    status           VARCHAR(20) NOT NULL DEFAULT 'draft',
    risk_level       VARCHAR(20),
    data             TEXT,
    document_id      INTEGER REFERENCES documents(id) ON DELETE SET NULL,
    created_by       INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at       TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    updated_at       TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
    activated_at     TIMESTAMP,
    closed_at        TIMESTAMP,
    closed_by        INTEGER REFERENCES users(id) ON DELETE SET NULL,
    close_notes      TEXT,
    CONSTRAINT uq_work_permit_company_number UNIQUE (company_id, permit_number)
);
CREATE INDEX IF NOT EXISTS ix_work_permits_company_id ON work_permits (company_id);
CREATE INDEX IF NOT EXISTS ix_work_permits_status ON work_permits (status);
CREATE INDEX IF NOT EXISTS ix_work_permits_document_id ON work_permits (document_id);


-- -------------------------------------------------------------------------------------
-- Toolbox talks + Workplace Voice + rewards + environmental company scope (2026-11-22/23)
-- -------------------------------------------------------------------------------------
-- ============================================================================
-- DEPLOY 2026-11-23 — run once on Railway PostgreSQL. Every statement is safe to re-run.
-- Order: toolbox talks, workplace voice (+ rewards), environmental company scope.
-- ============================================================================

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
ALTER TABLE IF EXISTS wv_channels ADD COLUMN IF NOT EXISTS rewards_enabled  BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE IF EXISTS wv_channels ADD COLUMN IF NOT EXISTS show_leaderboard BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE IF EXISTS wv_channels ADD COLUMN IF NOT EXISTS rewards_note     TEXT;

ALTER TABLE IF EXISTS wv_reports ADD COLUMN IF NOT EXISTS net_hash          VARCHAR(64);
ALTER TABLE IF EXISTS wv_reports ADD COLUMN IF NOT EXISTS reward_account_id INTEGER;
ALTER TABLE IF EXISTS wv_reports ADD COLUMN IF NOT EXISTS duplicate_of      INTEGER;
ALTER TABLE IF EXISTS wv_reports ADD COLUMN IF NOT EXISTS duplicate_count   INTEGER DEFAULT 0;
ALTER TABLE IF EXISTS wv_reports ADD COLUMN IF NOT EXISTS fingerprint       VARCHAR(64);
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

-- 2026-11-22  Environmental / thermal data isolation
-- These tables had no company column, so every company could read (and delete) every other
-- company's records. New rows are stamped with the creator's company automatically.
-- Safe to run more than once (PostgreSQL).

ALTER TABLE IF EXISTS thermal_sensors                ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS thermal_readings               ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS thermal_alerts                 ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS thermal_anomalies              ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS thermal_recommendations        ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS thermal_comfort_logs           ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS urban_heat_island_records      ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS thermal_analyses               ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS building_thermal_profiles      ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS compliance_reports             ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE IF EXISTS compliance_reports             ADD COLUMN IF NOT EXISTS created_by INTEGER REFERENCES users(id);
ALTER TABLE IF EXISTS compliance_automation_settings ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);

DO $$ BEGIN IF to_regclass('thermal_sensors') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_thermal_sensors_company_id           ON thermal_sensors(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('thermal_readings') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_thermal_readings_company_id          ON thermal_readings(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('thermal_alerts') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_thermal_alerts_company_id            ON thermal_alerts(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('thermal_anomalies') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_thermal_anomalies_company_id         ON thermal_anomalies(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('thermal_recommendations') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_thermal_recommendations_company_id   ON thermal_recommendations(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('thermal_comfort_logs') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_thermal_comfort_logs_company_id      ON thermal_comfort_logs(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('urban_heat_island_records') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_urban_heat_island_records_company_id ON urban_heat_island_records(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('thermal_analyses') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_thermal_analyses_company_id          ON thermal_analyses(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('building_thermal_profiles') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_building_thermal_profiles_company_id ON building_thermal_profiles(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('compliance_reports') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_compliance_reports_company_id        ON compliance_reports(company_id)'; END IF; END $$;
DO $$ BEGIN IF to_regclass('compliance_automation_settings') IS NOT NULL THEN EXECUTE 'CREATE INDEX IF NOT EXISTS ix_compliance_automation_settings_company_id ON compliance_automation_settings(company_id)'; END IF; END $$;

-- Existing rows keep company_id = NULL: only platform super admins see them.
-- If you know all existing thermal/compliance rows belong to ONE company, you can assign them, e.g.:
--   UPDATE thermal_sensors SET company_id = <id> WHERE company_id IS NULL;   (repeat per table)

