-- Mining (2026-11-27): critical controls, fit for shift, ground TARP, blast clearance.
CREATE TABLE IF NOT EXISTS mn_risks (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(160) NOT NULL, 
	description VARCHAR(1000), 
	controls TEXT NOT NULL, 
	active BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_mn_risks_company_id ON mn_risks (company_id);
CREATE TABLE IF NOT EXISTS mn_verifications (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	risk_id INTEGER NOT NULL, 
	area VARCHAR(160) NOT NULL, 
	answers TEXT NOT NULL, 
	failed INTEGER NOT NULL, 
	result VARCHAR(10) NOT NULL, 
	immediate_action VARCHAR(1000), 
	action_status VARCHAR(8), 
	closed_by INTEGER, 
	closed_at TIMESTAMP WITHOUT TIME ZONE, 
	closed_note VARCHAR(1000), 
	verified_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(risk_id) REFERENCES mn_risks (id) ON DELETE CASCADE, 
	FOREIGN KEY(closed_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(verified_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_verifications_risk_id ON mn_verifications (risk_id);
CREATE INDEX IF NOT EXISTS ix_mn_verifications_company_id ON mn_verifications (company_id);
CREATE TABLE IF NOT EXISTS mn_fatigue (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	user_id INTEGER, 
	shift_start TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	shift_end TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	sleep_24 FLOAT NOT NULL, 
	sleep_48 FLOAT NOT NULL, 
	woke_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	safety_critical BOOLEAN NOT NULL, 
	result VARCHAR(8) NOT NULL, 
	reasons TEXT, 
	controls TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_fatigue_user_id ON mn_fatigue (user_id);
CREATE INDEX IF NOT EXISTS ix_mn_fatigue_company_id ON mn_fatigue (company_id);
CREATE TABLE IF NOT EXISTS mn_tarps (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(160) NOT NULL, 
	location VARCHAR(160), 
	parameter VARCHAR(120) NOT NULL, 
	unit VARCHAR(20), 
	amber_at FLOAT NOT NULL, 
	red_at FLOAT NOT NULL, 
	green_actions TEXT, 
	amber_actions TEXT, 
	red_actions TEXT, 
	level VARCHAR(6) NOT NULL, 
	active BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_mn_tarps_company_id ON mn_tarps (company_id);
CREATE TABLE IF NOT EXISTS mn_tarp_readings (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	tarp_id INTEGER NOT NULL, 
	value FLOAT, 
	signs TEXT, 
	level VARCHAR(6) NOT NULL, 
	note VARCHAR(1000), 
	recorded_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(tarp_id) REFERENCES mn_tarps (id) ON DELETE CASCADE, 
	FOREIGN KEY(recorded_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_tarp_readings_tarp_id ON mn_tarp_readings (tarp_id);
CREATE INDEX IF NOT EXISTS ix_mn_tarp_readings_company_id ON mn_tarp_readings (company_id);
CREATE TABLE IF NOT EXISTS mn_blasts (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	ref VARCHAR(40) NOT NULL, 
	location VARCHAR(160) NOT NULL, 
	planned_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	exclusion_m INTEGER NOT NULL, 
	reentry_min INTEGER NOT NULL, 
	posts TEXT NOT NULL, 
	shotfirer VARCHAR(120), 
	status VARCHAR(12) NOT NULL, 
	fired_at TIMESTAMP WITHOUT TIME ZONE, 
	fired_by INTEGER, 
	misfire BOOLEAN NOT NULL, 
	reentry_by INTEGER, 
	reentry_at TIMESTAMP WITHOUT TIME ZONE, 
	note VARCHAR(1000), 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(fired_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(reentry_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_blasts_company_id ON mn_blasts (company_id);
