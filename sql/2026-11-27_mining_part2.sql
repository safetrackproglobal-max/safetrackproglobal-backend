-- Mining part 2 (2026-11-27): tag board, refuges, emergency roll call, exposure samples, health checks, slope / tailings monitoring.
CREATE TABLE IF NOT EXISTS mn_presence (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	user_id INTEGER, 
	person VARCHAR(120) NOT NULL, 
	employer VARCHAR(120), 
	area VARCHAR(160) NOT NULL, 
	scsr_tag VARCHAR(40) NOT NULL, 
	scsr_equipment_id INTEGER, 
	lamp_no VARCHAR(40), 
	status VARCHAR(4) NOT NULL, 
	entered_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	expected_out TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	exited_at TIMESTAMP WITHOUT TIME ZONE, 
	tagged_in_by INTEGER, 
	tagged_out_by INTEGER, 
	moves TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(scsr_equipment_id) REFERENCES equipment_items (id) ON DELETE SET NULL, 
	FOREIGN KEY(tagged_in_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(tagged_out_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_presence_company_id ON mn_presence (company_id);
CREATE TABLE IF NOT EXISTS mn_refuges (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	area VARCHAR(160) NOT NULL, 
	capacity INTEGER NOT NULL, 
	air_hours FLOAT, 
	check_every_days INTEGER NOT NULL, 
	last_checked_at TIMESTAMP WITHOUT TIME ZONE, 
	last_ok BOOLEAN, 
	last_issues TEXT, 
	active BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS ix_mn_refuges_company_id ON mn_refuges (company_id);
CREATE TABLE IF NOT EXISTS mn_refuge_checks (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	refuge_id INTEGER NOT NULL, 
	answers TEXT NOT NULL, 
	ok BOOLEAN NOT NULL, 
	note VARCHAR(1000), 
	checked_by INTEGER, 
	checked_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(refuge_id) REFERENCES mn_refuges (id) ON DELETE CASCADE, 
	FOREIGN KEY(checked_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_refuge_checks_refuge_id ON mn_refuge_checks (refuge_id);
CREATE INDEX IF NOT EXISTS ix_mn_refuge_checks_company_id ON mn_refuge_checks (company_id);
CREATE TABLE IF NOT EXISTS mn_emergencies (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	kind VARCHAR(20) NOT NULL, 
	area VARCHAR(160), 
	status VARCHAR(8) NOT NULL, 
	people TEXT NOT NULL, 
	started_by INTEGER, 
	started_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	closed_by INTEGER, 
	closed_at TIMESTAMP WITHOUT TIME ZONE, 
	note VARCHAR(1000), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(started_by) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(closed_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_emergencies_company_id ON mn_emergencies (company_id);
CREATE TABLE IF NOT EXISTS mn_samples (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	user_id INTEGER, 
	person VARCHAR(120) NOT NULL, 
	seg VARCHAR(120) NOT NULL, 
	area VARCHAR(160), 
	task VARCHAR(200), 
	agent VARCHAR(20) NOT NULL, 
	sampled_on DATE NOT NULL, 
	duration_min FLOAT NOT NULL, 
	shift_h FLOAT NOT NULL, 
	conc FLOAT NOT NULL, 
	twa8 FLOAT NOT NULL, 
	limit_used FLOAT NOT NULL, 
	action_used FLOAT, 
	result VARCHAR(8) NOT NULL, 
	respirator VARCHAR(60), 
	lab_ref VARCHAR(80), 
	note VARCHAR(500), 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_samples_company_id ON mn_samples (company_id);
CREATE TABLE IF NOT EXISTS mn_health_checks (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	user_id INTEGER, 
	person VARCHAR(120) NOT NULL, 
	done_on DATE NOT NULL, 
	outcome VARCHAR(10) NOT NULL, 
	next_due DATE NOT NULL, 
	note VARCHAR(500), 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_health_checks_company_id ON mn_health_checks (company_id);
CREATE TABLE IF NOT EXISTS mn_monitor_points (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	kind VARCHAR(14) NOT NULL, 
	structure VARCHAR(160) NOT NULL, 
	unit VARCHAR(10) NOT NULL, 
	amber_rate FLOAT, 
	red_rate FLOAT, 
	amber_level FLOAT, 
	red_level FLOAT, 
	level VARCHAR(6) NOT NULL, 
	active BOOLEAN NOT NULL, 
	created_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_monitor_points_company_id ON mn_monitor_points (company_id);
CREATE TABLE IF NOT EXISTS mn_monitor_readings (
	id SERIAL NOT NULL, 
	company_id INTEGER NOT NULL, 
	point_id INTEGER NOT NULL, 
	at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	value FLOAT NOT NULL, 
	note VARCHAR(300), 
	recorded_by INTEGER, 
	created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES companies (id) ON DELETE CASCADE, 
	FOREIGN KEY(point_id) REFERENCES mn_monitor_points (id) ON DELETE CASCADE, 
	FOREIGN KEY(recorded_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS ix_mn_monitor_readings_point_id ON mn_monitor_readings (point_id);
CREATE INDEX IF NOT EXISTS ix_mn_monitor_readings_company_id ON mn_monitor_readings (company_id);
