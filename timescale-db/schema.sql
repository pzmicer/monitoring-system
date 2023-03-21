DROP TABLE IF EXISTS sensor_data CASCADE;
DROP TABLE IF EXISTS station CASCADE;
DROP TABLE IF EXISTS device CASCADE;
DROP VIEW IF EXISTS get_stations_info CASCADE;

CREATE TABLE station(
    station_id SERIAL PRIMARY KEY,
    station_name TEXT NOT NULL,
    latitude NUMERIC,
    longitude NUMERIC
);

CREATE TABLE device(
    device_id SERIAL PRIMARY KEY,
    device_name TEXT,
    station_id INTEGER REFERENCES station(station_id)
);

CREATE TABLE sensor_data(
    device_id INTEGER NOT NULL REFERENCES device(device_id),
    time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    temp_c DOUBLE PRECISION NULL,
    humidity DOUBLE PRECISION NULL,
    PRIMARY KEY(device_id, time)
);
SELECT create_hypertable('sensor_data', 'time');

CREATE VIEW get_stations_info AS
SELECT  c.station_name, avg(temp_c) as "avg_temp" 
FROM sensor_data a 
    LEFT JOIN device b 
    ON a.device_id = b.device_id 
    LEFT JOIN station c 
    ON b.station_id = c.station_id 
GROUP BY c.station_id;