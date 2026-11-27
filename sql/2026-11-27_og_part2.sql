-- Oil and gas part 2 (2026-11-27): shift handover, gas detector checks, dropped objects.
CREATE TABLE IF NOT EXISTS og_handovers (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	area VARCHAR(200), 
	shift_label VARCHAR(80), 
	outgoing_id INTEGER, 
	incoming_id INTEGER, 
	status VARCHAR(10) NOT NULL, 
	items TEXT, 
	cleared TEXT, 
	notes TEXT, 
	concerns TEXT, 
	notified BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	accepted_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(outgoing_id) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(incoming_id) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_og_handovers_company_id ON og_handovers (company_id);
CREATE TABLE IF NOT EXISTS og_detector_checks (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	instrument_id INTEGER NOT NULL, 
	kind VARCHAR(12) NOT NULL, 
	checked_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	result VARCHAR(6) NOT NULL, 
	sensors TEXT, 
	tolerance_pct FLOAT, 
	reasons TEXT, 
	note VARCHAR(500), 
	checked_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(instrument_id) REFERENCES equipment_items (id) ON DELETE CASCADE, 
	FOREIGN KEY(checked_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_og_detector_checks_company_id ON og_detector_checks (company_id);
CREATE INDEX IF NOT EXISTS ix_og_detector_checks_instrument_id ON og_detector_checks (instrument_id);
CREATE TABLE IF NOT EXISTS og_drops_surveys (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	area VARCHAR(200) NOT NULL, 
	items_checked INTEGER, 
	findings INTEGER NOT NULL, 
	note VARCHAR(500), 
	surveyed_by INTEGER, 
	surveyed_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(surveyed_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_og_drops_surveys_company_id ON og_drops_surveys (company_id);
CREATE TABLE IF NOT EXISTS og_drops_findings (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	survey_id INTEGER, 
	area VARCHAR(200) NOT NULL, 
	item VARCHAR(200) NOT NULL, 
	position VARCHAR(200), 
	issue VARCHAR(20) NOT NULL, 
	mass_kg FLOAT NOT NULL, 
	height_m FLOAT NOT NULL, 
	energy_j FLOAT NOT NULL, 
	consequence VARCHAR(8), 
	people_below BOOLEAN NOT NULL, 
	status VARCHAR(8) NOT NULL, 
	action VARCHAR(500), 
	fix_note VARCHAR(500), 
	found_by INTEGER, 
	found_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	fixed_by INTEGER, 
	fixed_at TIMESTAMP WITHOUT TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(survey_id) REFERENCES og_drops_surveys (id) ON DELETE SET NULL, 
	FOREIGN KEY(found_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(fixed_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_og_drops_findings_survey_id ON og_drops_findings (survey_id);
CREATE INDEX IF NOT EXISTS ix_og_drops_findings_company_id ON og_drops_findings (company_id);
