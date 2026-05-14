-- Q4: Top locations by demand, Nov vs Dec comparison
WITH nov_data AS (
    SELECT loc, SUM(count) AS loc_count
    FROM opal_data
    WHERE period = 'nov' AND loc != '-1'
    GROUP BY loc
    ORDER BY loc_count DESC
    LIMIT 10
),
dec_data AS (
    SELECT loc, SUM(count) AS loc_count
    FROM opal_data
    WHERE period = 'dec' AND loc != '-1'
    GROUP BY loc
    ORDER BY loc_count DESC
    LIMIT 10
)
SELECT
    nov_data.loc,
    nov_data.loc_count AS nov_loc_count,
    dec_data.loc,
    dec_data.loc_count AS dec_loc_count,
    ROUND(((nov_data.loc_count - dec_data.loc_count)::numeric / nov_data.loc_count) * 100, 2) AS pct_drop_from_nov
FROM nov_data
FULL OUTER JOIN dec_data ON nov_data.loc = dec_data.loc
ORDER BY nov_data.loc_count DESC;

-- Q4: Peak time of day per top location (window function)
SELECT * FROM (
    SELECT loc, time, total_taps,
        ROW_NUMBER() OVER (PARTITION BY loc ORDER BY total_taps DESC) AS row_num
    FROM (
        SELECT loc, time, SUM(count) AS total_taps
        FROM opal_data
        WHERE loc != '-1' AND loc != 'UNKNOWN' AND time != '-1'
        GROUP BY loc, time
    ) inner_query
) ranked
WHERE row_num = 1
AND loc IN (
    '2000', 'Town Hall Station', 'Central Station', 'Wynyard Station',
    'Parramatta Station', 'Chatswood Station', 'Bondi Junction Station',
    'North Sydney Station', 'Circular Quay Station', '2022'
);