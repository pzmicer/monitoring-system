DROP TABLE sensor_data;

CREATE TABLE sensor_data(
    device_id TEXT NOT NULL,
    time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    temp_c DOUBLE PRECISION NULL,
    pressure_hpa DOUBLE PRECISION NULL,
    wind_speed_ms DOUBLE PRECISION NULL,
    latitude NUMERIC,
    longitude NUMERIC
);

SELECt create_hypertable('sensor_data', 'time');