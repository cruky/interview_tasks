DROP TABLE IF EXISTS smart_readings CASCADE;
CREATE TABLE smart_readings (
    id SERIAL PRIMARY KEY,
	smart_meter_id int4 NOT NULL,
	time_stamp timestamp NOT NULL,
	energy_kwh NUMERIC (2, 1) NOT NULL
	);
CREATE INDEX readings_timestamp_idx ON smart_readings
 USING btree (time_stamp DESC);
 --USING BRIN (time_stamp) --Its better algorithm but fits into real time series data