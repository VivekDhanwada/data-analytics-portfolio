WITH purchase_days AS (
    SELECT
        household_key,
        day,
        basket_id,
        SUM(sales_value) AS basket_spend
    FROM {{ ref('stg_transaction_data') }}
    GROUP BY household_key, day, basket_id
),

purchase_gaps AS (
    SELECT
        household_key,
        day,
        basket_spend,
        LAG(day, 1) OVER (PARTITION BY household_key ORDER BY day) AS prev_purchase_day,
        day - LAG(day, 1) OVER (PARTITION BY household_key ORDER BY day) AS days_since_last_purchase
    FROM purchase_days
)

SELECT
    household_key,
    COUNT(*) AS total_purchases,
    AVG(days_since_last_purchase) AS avg_days_between_purchases,
    AVG(basket_spend) AS avg_spend_per_trip,
    MIN(day) AS first_purchase_day,
    MAX(day) AS last_purchase_day
FROM purchase_gaps
WHERE days_since_last_purchase IS NOT NULL
GROUP BY household_key