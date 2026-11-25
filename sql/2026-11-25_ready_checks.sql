-- Ready Check: pre-task life-saving control checks, stop work and lone-worker timers.
CREATE TABLE IF NOT EXISTS ready_checks (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(64) NOT NULL,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    worker_name VARCHAR(120),
    kind VARCHAR(12) NOT NULL DEFAULT 'check',
    task_key VARCHAR(40),
    task_name VARCHAR(160) NOT NULL,
    location VARCHAR(200),
    crew_size INTEGER NOT NULL DEFAULT 1,
    answers TEXT,
    missing TEXT,
    controls_total INTEGER NOT NULL DEFAULT 0,
    controls_ok INTEGER NOT NULL DEFAULT 0,
    result VARCHAR(8) NOT NULL,
    status VARCHAR(12) NOT NULL,
    note TEXT,
    is_lone BOOLEAN NOT NULL DEFAULT FALSE,
    expected_end TIMESTAMP,
    alert_level INTEGER NOT NULL DEFAULT 0,
    alerted_at TIMESTAMP,
    finished_at TIMESTAMP,
    resolved_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    resolved_at TIMESTAMP,
    resolution_note TEXT,
    done_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_ready_checks_client ON ready_checks (user_id, client_id);
CREATE INDEX IF NOT EXISTS ix_ready_checks_company_done ON ready_checks (company_id, done_at);
CREATE INDEX IF NOT EXISTS ix_ready_checks_timer ON ready_checks (status, expected_end);
