-- Maritime enclosed space entry and drills (2026-11-28)
CREATE TABLE IF NOT EXISTS mar_spaces (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	vessel VARCHAR(120) NOT NULL, 
	name VARCHAR(160) NOT NULL, 
	kind VARCHAR(16) NOT NULL, 
	hazards TEXT, 
	active BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_mar_spaces_company_id ON mar_spaces (company_id);
CREATE TABLE IF NOT EXISTS mar_entries (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	space_id INTEGER NOT NULL, 
	purpose VARCHAR(300) NOT NULL, 
	entrants TEXT NOT NULL, 
	attendant VARCHAR(120) NOT NULL, 
	comms VARCHAR(120), 
	o2 FLOAT, 
	lfl FLOAT, 
	h2s FLOAT, 
	co FLOAT, 
	limits TEXT, 
	tested_by VARCHAR(120), 
	tested_at TIMESTAMP WITHOUT TIME ZONE, 
	ventilated BOOLEAN NOT NULL, 
	rescue_ready BOOLEAN NOT NULL, 
	status VARCHAR(8) NOT NULL, 
	entered_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	exited_at TIMESTAMP WITHOUT TIME ZONE, 
	close_note VARCHAR(500), 
	authorised_by INTEGER, 
	closed_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(space_id) REFERENCES mar_spaces (id) ON DELETE CASCADE, 
	FOREIGN KEY(authorised_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(closed_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mar_entries_company_id ON mar_entries (company_id);
CREATE INDEX IF NOT EXISTS ix_mar_entries_space_id ON mar_entries (space_id);
CREATE TABLE IF NOT EXISTS mar_drills (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	vessel VARCHAR(120) NOT NULL, 
	held_on DATE NOT NULL, 
	scenario VARCHAR(300) NOT NULL, 
	participants INTEGER NOT NULL, 
	equipment_checked BOOLEAN NOT NULL, 
	lessons TEXT, 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mar_drills_company_id ON mar_drills (company_id);
