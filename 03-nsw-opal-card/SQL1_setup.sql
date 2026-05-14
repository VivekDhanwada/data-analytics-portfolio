DROP TABLE IF EXISTS alerts_data;
DROP TABLE IF EXISTS opal_data;
DROP TABLE IF EXISTS opal_data1;
DROP TABLE IF EXISTS opal_data2;

CREATE TABLE alerts_data ( start_time TIMESTAMPTZ, end_time TIMESTAMPTZ, affected_routes TEXT, affected_stops TEXT, affected_trips TEXT, alert_header TEXT, alert_description TEXT, alert_type TEXT );

CREATE TABLE opal_data1 (
    mode TEXT,
    date TEXT,
    tap TEXT,
    time TEXT,
    loc TEXT,
    count INTEGER
);

COPY opal_data1 FROM '/tmp/time_loc_20161121-27.csv' DELIMITER ',' CSV Header;

CREATE TABLE opal_data2 (
    mode TEXT,
    date TEXT,
    tap TEXT,
	time TEXT,
    loc TEXT,
    count INTEGER
);

COPY opal_data2 FROM '/tmp/dec_fixed2.csv' DELIMITER ',' CSV HEADER;

COPY alerts_data FROM '/tmp/alerts20161121-20170101.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE opal_data (
    mode TEXT,
    date TEXT,
    tap TEXT,
    time TEXT,
    loc TEXT,
    count INTEGER,
    period TEXT
);

INSERT INTO opal_data SELECT *, 'nov' FROM opal_data1;
INSERT INTO opal_data SELECT *, 'dec' FROM opal_data2;