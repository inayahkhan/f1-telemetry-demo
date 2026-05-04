CREATE EXTENSION IF NOT EXISTS timescaledb;

DROP TABLE IF EXISTS f1_telemetry;

CREATE TABLE f1_telemetry (
    time TIMESTAMPTZ NOT NULL,
    car_id TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    team_name TEXT NOT NULL,
    lap_number INT NOT NULL,
    speed_kph DOUBLE PRECISION,
    throttle_percent DOUBLE PRECISION,
    brake_percent DOUBLE PRECISION,
    tyre_temp_c DOUBLE PRECISION,
    engine_temp_c DOUBLE PRECISION,
    battery_percent DOUBLE PRECISION,
    gear INT
);

SELECT create_hypertable('f1_telemetry', 'time');

INSERT INTO f1_telemetry
SELECT
    NOW() - INTERVAL '10 minutes' + (s * INTERVAL '1 second') AS time,
    'SF-16' AS car_id,
    'Charles Leclerc' AS driver_name,
    'Scuderia Ferrari' AS team_name,
    FLOOR(s / 60) + 1 AS lap_number,
    180 + random() * 140 AS speed_kph,
    60 + random() * 40 AS throttle_percent,
    CASE
        WHEN random() > 0.75 THEN 40 + random() * 60
        ELSE random() * 15
    END AS brake_percent,
    80 + random() * 30 AS tyre_temp_c,
    95 + random() * 20 AS engine_temp_c,
    40 + random() * 60 AS battery_percent,
    FLOOR(1 + random() * 8)::INT AS gear
FROM generate_series(0, 599) AS s;

CREATE INDEX IF NOT EXISTS idx_f1_telemetry_lap
ON f1_telemetry(lap_number, time DESC);