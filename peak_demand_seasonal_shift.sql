-- Q1/Q2: Peak demand by time of day (Nov vs Dec)
WITH nov_data AS (
    SELECT time, SUM(count) AS total_taps_nov
    FROM opal_data WHERE time != '-1' AND period = 'nov'
    GROUP BY time
),
dec_data AS (
    SELECT time, SUM(count) AS total_taps_dec
    FROM opal_data WHERE time != '-1' AND period = 'dec'
    GROUP BY time
)
SELECT nov_data.time, total_taps_nov AS nov_sum, total_taps_dec AS dec_sum,
    ROUND(((total_taps_nov - total_taps_dec)::numeric / total_taps_nov) * 100, 2) AS pct_drop_from_nov
FROM nov_data
JOIN dec_data ON nov_data.time = dec_data.time
ORDER BY nov_sum DESC;

-- Q1/Q2: Peak demand by mode (Nov vs Dec)
WITH nov_data AS (
    SELECT mode, SUM(count) AS total_taps_nov
    FROM opal_data WHERE period = 'nov'
    GROUP BY mode
),
dec_data AS (
    SELECT mode, SUM(count) AS total_taps_dec
    FROM opal_data WHERE period = 'dec'
    GROUP BY mode
)
SELECT nov_data.mode, total_taps_nov AS nov_sum, total_taps_dec AS dec_sum,
    ROUND(((total_taps_nov - total_taps_dec)::numeric / total_taps_nov) * 100, 2) AS pct_drop_from_nov
FROM nov_data
JOIN dec_data ON nov_data.mode = dec_data.mode
ORDER BY nov_sum DESC;

-- Q1/Q2: Weekday vs weekend demand (Nov vs Dec)
WITH nov_data AS (
    SELECT
        CASE
            WHEN EXTRACT(DOW FROM TO_DATE(date, 'YYYYMMDD')) IN (1,2,3,4,5) THEN 'weekday'
            WHEN EXTRACT(DOW FROM TO_DATE(date, 'YYYYMMDD')) IN (0,6) THEN 'weekend'
        END AS day_type,
        SUM(count) AS total_taps
    FROM opal_data WHERE period = 'nov'
    GROUP BY day_type
),
dec_data AS (
    SELECT
        CASE
            WHEN EXTRACT(DOW FROM TO_DATE(date, 'YYYYMMDD')) IN (1,2,3,4,5) THEN 'weekday'
            WHEN EXTRACT(DOW FROM TO_DATE(date, 'YYYYMMDD')) IN (0,6) THEN 'weekend'
        END AS day_type,
        SUM(count) AS total_taps
    FROM opal_data WHERE period = 'dec'
    GROUP BY day_type
)
SELECT nov_data.day_type, nov_data.total_taps AS nov_sum, dec_data.total_taps AS dec_sum,
    ROUND(((nov_data.total_taps - dec_data.total_taps)::numeric / nov_data.total_taps) * 100, 2) AS pct_drop_from_nov
FROM nov_data
JOIN dec_data ON nov_data.day_type = dec_data.day_type
ORDER BY nov_sum DESC;
