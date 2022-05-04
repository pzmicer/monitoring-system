DELETE FROM sensor_data;

INSERT INTO
    sensor_data(device_id, time, temp_c, pressure_hpa, wind_speed_ms, latitude, longitude)
SELECT
    device_id,
    time,
    random()*(40 - (-10)) - 10 AS temp_c,
    random()*(1200 - 800) + 800 AS pressure_hpa,
    random()*(15 - 5) + 5 AS wind_speed_ms,
    random()*(90 - (-90)) - 90 AS latitude,
    random()*(180 - (-180)) - 180 AS longitude
FROM
    generate_series(
        NOW() - INTERVAL '10 day',
        NOW(),
        INTERVAL '4 hour'
    ) AS g1(time),
    generate_series(1, 2, 1) AS g2(device_id);