DELETE FROM sensor_data;
DELETE FROM station;
DELETE FROM device_station;

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
    generate_series(1, 5, 1) AS g2(device_id);


INSERT INTO 
    station(station_id, station_name)
VALUES  
    (1, 'Station 1'),
    (2, 'Station 2'),
    (3, 'Station 3'),
    (4, 'Station 4');


INSERT INTO 
    device_station
VALUES
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 4);
-- SELECT
--     device_id,
--     station_id,
-- FROM
--     generate_series(1, 5, 1) as g1(device_id),
--     floor(random()*(4 - 0 + 1)+ 0) as g2(station_id);


