DROP TABLE sensor_data;
DROP TABLE station;

CREATE TABLE sensor_data(
    device_id TEXT NOT NULL,
    time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    temp_c DOUBLE PRECISION NULL,
    pressure_hpa DOUBLE PRECISION NULL,
    wind_speed_ms DOUBLE PRECISION NULL,
    latitude NUMERIC,
    longitude NUMERIC
);
SELECT create_hypertable('sensor_data', 'time');

CREATE TABLE station(
    station_id INTEGER PRIMARY KEY,
    station_name TEXT NOT NULL
);

CREATE TABLE device_station(
    device_id TEXT NOT NULL,
    station_id INTEGER NOT NULL,
    PRIMARY KEY(device_id, station_id)
);

CREATE VIEW get_stations_info AS
SELECT  c.station_name, avg(temp_c) as "avg_temp" 
FROM sensor_data a 
    LEFT JOIN device_station b 
    ON a.device_id = b.device_id 
    LEFT JOIN station c 
    ON b.station_id = c.station_id 
GROUP BY c.station_id;