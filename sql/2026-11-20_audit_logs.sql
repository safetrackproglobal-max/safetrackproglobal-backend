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
