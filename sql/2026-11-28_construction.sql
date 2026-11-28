-- Construction excavations (2026-11-28)
CREATE TABLE IF NOT EXISTS cn_excavations (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	ref VARCHAR(40) NOT NULL, 
	location VARCHAR(200) NOT NULL, 
	purpose VARCHAR(200), 
	depth_m FLOAT NOT NULL, 
	width_m FLOAT, 
	soil VARCHAR(12) NOT NULL, 
	protection VARCHAR(10) NOT NULL, 
	pe_design BOOLEAN NOT NULL, 
	pe_ref VARCHAR(160), 
	utilities_located BOOLEAN NOT NULL, 
	utilities_ref VARCHAR(160), 
	egress VARCHAR(10) NOT NULL, 
	egress_within_25ft BOOLEAN NOT NULL, 
	atmosphere_risk BOOLEAN NOT NULL, 
	status VARCHAR(8) NOT NULL, 
	hazard_event_at TIMESTAMP WITHOUT TIME ZONE, 
	hazard_event_note VARCHAR(300), 
	closed_at TIMESTAMP WITHOUT TIME ZONE, 
	closed_by INTEGER, 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(closed_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_cn_excavations_company_id ON cn_excavations (company_id);
CREATE TABLE IF NOT EXISTS cn_excavation_checks (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	excavation_id INTEGER NOT NULL, 
	checked_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	checked_by INTEGER, 
	answers TEXT NOT NULL, 
	o2 FLOAT, 
	lel FLOAT, 
	result VARCHAR(6) NOT NULL, 
	note VARCHAR(1000), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(excavation_id) REFERENCES cn_excavations (id) ON DELETE CASCADE, 
	FOREIGN KEY(checked_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_cn_excavation_checks_company_id ON cn_excavation_checks (company_id);
CREATE INDEX IF NOT EXISTS ix_cn_excavation_checks_excavation_id ON cn_excavation_checks (excavation_id);
