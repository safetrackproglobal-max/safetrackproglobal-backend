-- 2026-11-22  Environmental / thermal data isolation
-- These tables had no company column, so every company could read (and delete) every other
-- company's records. New rows are stamped with the creator's company automatically.
-- Safe to run more than once (PostgreSQL).

ALTER TABLE thermal_sensors                ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE thermal_readings               ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE thermal_alerts                 ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE thermal_anomalies              ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE thermal_recommendations        ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE thermal_comfort_logs           ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE urban_heat_island_records      ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE thermal_analyses               ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE building_thermal_profiles      ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE compliance_reports             ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);
ALTER TABLE compliance_reports             ADD COLUMN IF NOT EXISTS created_by INTEGER REFERENCES users(id);
ALTER TABLE compliance_automation_settings ADD COLUMN IF NOT EXISTS company_id INTEGER REFERENCES companies(id);

CREATE INDEX IF NOT EXISTS ix_thermal_sensors_company_id           ON thermal_sensors(company_id);
CREATE INDEX IF NOT EXISTS ix_thermal_readings_company_id          ON thermal_readings(company_id);
CREATE INDEX IF NOT EXISTS ix_thermal_alerts_company_id            ON thermal_alerts(company_id);
CREATE INDEX IF NOT EXISTS ix_thermal_anomalies_company_id         ON thermal_anomalies(company_id);
CREATE INDEX IF NOT EXISTS ix_thermal_recommendations_company_id   ON thermal_recommendations(company_id);
CREATE INDEX IF NOT EXISTS ix_thermal_comfort_logs_company_id      ON thermal_comfort_logs(company_id);
CREATE INDEX IF NOT EXISTS ix_urban_heat_island_records_company_id ON urban_heat_island_records(company_id);
CREATE INDEX IF NOT EXISTS ix_thermal_analyses_company_id          ON thermal_analyses(company_id);
CREATE INDEX IF NOT EXISTS ix_building_thermal_profiles_company_id ON building_thermal_profiles(company_id);
CREATE INDEX IF NOT EXISTS ix_compliance_reports_company_id        ON compliance_reports(company_id);
CREATE INDEX IF NOT EXISTS ix_compliance_automation_settings_company_id ON compliance_automation_settings(company_id);

-- Existing rows keep company_id = NULL: only platform super admins see them.
-- If you know all existing thermal/compliance rows belong to ONE company, you can assign them, e.g.:
--   UPDATE thermal_sensors SET company_id = <id> WHERE company_id IS NULL;   (repeat per table)
