WITH customer_activity AS (
    SELECT
        household_key,
        last_purchase_day,
        avg_days_between_purchases,
        avg_spend_per_trip,
        total_purchases,
        711 - last_purchase_day AS days_since_last_purchase
    FROM {{ ref('int_customer_purchase_frequency') }}
)

SELECT
    household_key,
    last_purchase_day,
    days_since_last_purchase,
    avg_days_between_purchases,
    avg_spend_per_trip,
    total_purchases,
    CASE WHEN last_purchase_day < 627 THEN TRUE ELSE FALSE END AS is_churned
FROM customer_activity