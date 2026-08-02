WITH transactions AS (
    SELECT * FROM {{ ref('int_transaction_promotions') }}
),

effectiveness AS (
    SELECT * FROM {{ ref('int_promotion_effectiveness') }}
),

churn AS (
    SELECT
        household_key,
        is_churned,
        days_since_last_purchase
    FROM {{ ref('int_customer_churn') }}
)

SELECT
    t.household_key,
    t.basket_id,
    t.day,
    t.product_id,
    t.store_id,
    t.week_no,
    t.sales_value,
    t.quantity,
    t.retail_disc,
    t.coupon_disc,
    t.campaign,
    t.coupon_upc,
    t.is_coupon_redeemed,
    t.is_on_display,
    t.is_in_mailer,
    e.post_promo_revenue,
    e.days_to_first_return,
    e.returned_faster_than_baseline,
    e.above_baseline_revenue,
    e.baseline_gap,
    c.is_churned,
    c.days_since_last_purchase
FROM transactions t
LEFT JOIN effectiveness e
    ON t.household_key = e.household_key
    AND t.day = e.redemption_day
LEFT JOIN churn c
    ON t.household_key = c.household_key