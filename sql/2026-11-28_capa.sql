-- CAPA details (2026-11-28): root cause, preventive action, effectiveness check
CREATE TABLE IF NOT EXISTS capa_details (
	capa_id INTEGER NOT NULL, 
	company_id INTEGER NOT NULL, 
	source_key VARCHAR(160), 
	problem TEXT, 
	containment TEXT, 
	why_chain TEXT, 
	root_cause TEXT, 
	root_cause_category VARCHAR(20), 
	preventive_action TEXT, 
	check_criteria TEXT, 
	check_after_days INTEGER NOT NULL, 
	done_note TEXT, 
	done_by INTEGER, 
	done_at TIMESTAMP WITHOUT TIME ZONE, 
	check_due DATE, 
	check_result VARCHAR(16), 
	check_note TEXT, 
	checked_by INTEGER, 
	checked_at TIMESTAMP WITHOUT TIME ZONE, 
	cycles INTEGER NOT NULL, 
	history TEXT, 
	notified_on DATE, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (capa_id), 
	FOREIGN KEY(capa_id) REFERENCES corrective_actions (id) ON DELETE CASCADE, 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(done_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(checked_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_capa_details_source_key ON capa_details (source_key);
CREATE INDEX IF NOT EXISTS ix_capa_details_company_id ON capa_details (company_id);
