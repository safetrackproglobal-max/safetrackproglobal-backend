-- Document control plus: read & acknowledge, controlled copies, point-of-use QR codes, change requests.
CREATE TABLE IF NOT EXISTS doc_read_requests (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    document_id INTEGER NOT NULL,
    document_version INTEGER NOT NULL DEFAULT 1,
    message TEXT,
    due_date TIMESTAMP,
    quiz TEXT,
    pass_mark INTEGER NOT NULL DEFAULT 80,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    created_by INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_doc_read_requests_company_id ON doc_read_requests (company_id);
CREATE INDEX IF NOT EXISTS ix_doc_read_requests_document_id ON doc_read_requests (document_id);
CREATE TABLE IF NOT EXISTS doc_read_assignments (
    id SERIAL PRIMARY KEY,
    request_id INTEGER NOT NULL REFERENCES doc_read_requests(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    attempts INTEGER NOT NULL DEFAULT 0,
    quiz_score INTEGER,
    acknowledged_at TIMESTAMP,
    ip_address VARCHAR(64),
    reminded_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_doc_read_assignments_request_id ON doc_read_assignments (request_id);
CREATE INDEX IF NOT EXISTS ix_doc_read_assignments_user_id ON doc_read_assignments (user_id);
CREATE TABLE IF NOT EXISTS doc_controlled_copies (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    document_id INTEGER NOT NULL,
    document_version INTEGER NOT NULL DEFAULT 1,
    copy_number INTEGER NOT NULL,
    holder VARCHAR(255) NOT NULL,
    holder_user_id INTEGER,
    location VARCHAR(255),
    purpose VARCHAR(255),
    status VARCHAR(20) NOT NULL DEFAULT 'issued',
    issued_by INTEGER,
    issued_at TIMESTAMP NOT NULL DEFAULT NOW(),
    withdrawn_by INTEGER,
    withdrawn_at TIMESTAMP,
    note TEXT
);
CREATE INDEX IF NOT EXISTS ix_doc_controlled_copies_company_id ON doc_controlled_copies (company_id);
CREATE INDEX IF NOT EXISTS ix_doc_controlled_copies_document_id ON doc_controlled_copies (document_id);
CREATE TABLE IF NOT EXISTS doc_qr_links (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    document_id INTEGER NOT NULL,
    token VARCHAR(40) NOT NULL UNIQUE,
    label VARCHAR(255),
    scans INTEGER NOT NULL DEFAULT 0,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_doc_qr_links_company_id ON doc_qr_links (company_id);
CREATE INDEX IF NOT EXISTS ix_doc_qr_links_document_id ON doc_qr_links (document_id);
CREATE TABLE IF NOT EXISTS doc_change_requests (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    document_id INTEGER NOT NULL,
    number VARCHAR(40) NOT NULL,
    title VARCHAR(255) NOT NULL,
    reason TEXT NOT NULL,
    proposed_change TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'normal',
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    requested_by INTEGER,
    requested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    decided_by INTEGER,
    decided_at TIMESTAMP,
    decision_note TEXT,
    implemented_version INTEGER,
    implemented_at TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_doc_change_requests_company_id ON doc_change_requests (company_id);
CREATE INDEX IF NOT EXISTS ix_doc_change_requests_document_id ON doc_change_requests (document_id);
