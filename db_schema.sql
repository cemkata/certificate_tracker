BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "certificates_info_tbl" (
	"id"	INTEGER NOT NULL UNIQUE,
	"server_ip"	TEXT NOT NULL,
	"server_service"	TEXT,
	"server_name"	TEXT,
	"certificates_authority"	TEXT NOT NULL,
	"generated_on_day"	INTEGER NOT NULL,
	"generated_on_month"	INTEGER NOT NULL,
	"generated_on_year"	INTEGER NOT NULL,
	"valid_to_day"	INTEGER NOT NULL,
	"valid_to_month"	INTEGER NOT NULL,
	"valid_to_year"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
COMMIT;
