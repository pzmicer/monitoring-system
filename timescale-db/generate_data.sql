TRUNCATE sensor_data CASCADE;
TRUNCATE station CASCADE;
TRUNCATE device CASCADE;


INSERT INTO 
    station(station_id, station_name, latitude, longitude)
VALUES  
    (1, 'Station 1', random()*(90 - (-90)) - 90, random()*(180 - (-180)) - 180),
    (2, 'Station 2', random()*(90 - (-90)) - 90, random()*(180 - (-180)) - 180),
    (3, 'Station 3', random()*(90 - (-90)) - 90, random()*(180 - (-180)) - 180);


INSERT INTO 
    device(device_id, device_name, station_id)
VALUES
    (1, 'dev1', 1),
    (2, 'dev2', 1),
    (3, 'dev3', 2),
    (4, 'dev4', 2),
    (5, 'dev5', 3),
    (6, 'dev6', 3);


INSERT INTO
    sensor_data(device_id, time, temp_c, humidity)
SELECT
    device_id,
    time,
    random()*(40 - (-10)) - 10 AS temp_c,
    random() AS humidity
FROM
    generate_series(
        NOW() - INTERVAL '10 day',
        NOW(),
        INTERVAL '4 hour'
    ) AS g1(time),
    generate_series(1, 5, 1) AS g2(device_id);

