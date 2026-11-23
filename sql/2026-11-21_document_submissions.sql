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
