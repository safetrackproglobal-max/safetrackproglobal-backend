-- Manufacturing and warehouse (2026-11-27): machine lockout procedures, lockouts, guarding, racking damage, forklift traffic by zone.
CREATE TABLE IF NOT EXISTS mf_procedures (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	machine VARCHAR(160) NOT NULL, 
	equipment_id INTEGER, 
	location VARCHAR(160), 
	energy_points TEXT NOT NULL, 
	notes TEXT, 
	version INTEGER NOT NULL, 
	approved_by INTEGER, 
	approved_at TIMESTAMP WITHOUT TIME ZONE, 
	periodic_at TIMESTAMP WITHOUT TIME ZONE, 
	periodic_by INTEGER, 
	periodic_note VARCHAR(1000), 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(equipment_id) REFERENCES equipment_items (id) ON DELETE SET NULL, 
	FOREIGN KEY(approved_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(periodic_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mf_procedures_company_id ON mf_procedures (company_id);
CREATE TABLE IF NOT EXISTS mf_lockouts (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	procedure_id INTEGER NOT NULL, 
	reason VARCHAR(500) NOT NULL, 
	points TEXT NOT NULL, 
	status VARCHAR(12) NOT NULL, 
	started_by INTEGER, 
	started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	verified_by INTEGER, 
	verified_at TIMESTAMP WITHOUT TIME ZONE, 
	verify_note VARCHAR(500), 
	released_by INTEGER, 
	released_at TIMESTAMP WITHOUT TIME ZONE, 
	release_note VARCHAR(500), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(procedure_id) REFERENCES mf_procedures (id) ON DELETE CASCADE, 
	FOREIGN KEY(started_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(verified_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(released_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mf_lockouts_procedure_id ON mf_lockouts (procedure_id);
CREATE INDEX IF NOT EXISTS ix_mf_lockouts_company_id ON mf_lockouts (company_id);
CREATE TABLE IF NOT EXISTS mf_guarding (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	machine VARCHAR(160) NOT NULL, 
	location VARCHAR(160), 
	points TEXT NOT NULL, 
	result VARCHAR(10) NOT NULL, 
	assessed_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(assessed_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mf_guarding_company_id ON mf_guarding (company_id);
CREATE TABLE IF NOT EXISTS wh_rack_reports (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	location VARCHAR(120) NOT NULL, 
	component VARCHAR(20) NOT NULL, 
	direction VARCHAR(8), 
	measured_mm FLOAT, 
	level VARCHAR(6) NOT NULL, 
	description VARCHAR(1000), 
	status VARCHAR(10) NOT NULL, 
	due_on DATE, 
	reported_by INTEGER, 
	offloaded_at TIMESTAMP WITHOUT TIME ZONE, 
	repaired_at TIMESTAMP WITHOUT TIME ZONE, 
	repaired_by INTEGER, 
	repair_note VARCHAR(1000), 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(reported_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(repaired_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_wh_rack_reports_company_id ON wh_rack_reports (company_id);
CREATE TABLE IF NOT EXISTS wh_traffic (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	zone VARCHAR(120) NOT NULL, 
	kind VARCHAR(20) NOT NULL, 
	note VARCHAR(1000), 
	occurred_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	reported_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(reported_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_wh_traffic_company_id ON wh_traffic (company_id);
CREATE TABLE IF NOT EXISTS wh_zone_controls (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	zone VARCHAR(120) NOT NULL, 
	control VARCHAR(300) NOT NULL, 
	kind VARCHAR(20) NOT NULL, 
	implemented_on DATE NOT NULL, 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_wh_zone_controls_company_id ON wh_zone_controls (company_id);
