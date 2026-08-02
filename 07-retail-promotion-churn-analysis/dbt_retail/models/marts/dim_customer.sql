WITH demographics AS (
    SELECT * FROM {{ ref('stg_hh_demographic') }}
),

purchase_frequency AS (
    SELECT * FROM {{ ref('int_customer_purchase_frequency') }}
),

churn AS (
    SELECT * FROM {{ ref('int_customer_churn') }}
)

SELECT
    c.household_key,
    c.is_churned,
    c.days_since_last_purchase,
    c.last_purchase_day,
    p.avg_days_between_purchases,
    p.avg_spend_per_trip,
    p.total_purchases,
    p.first_purchase_day,
    d.age_desc,
    d.marital_status_code,
    d.income_desc,
    d.homeowner_desc,
    d.hh_comp_desc,
    d.household_size_desc,
    d.kid_category_desc
FROM churn c
LEFT JOIN purchase_frequency p
    ON c.household_key = p.household_key
LEFT JOIN demographics d
    ON c.household_key = d.household_key