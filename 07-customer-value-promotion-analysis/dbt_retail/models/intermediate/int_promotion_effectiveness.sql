WITH redemptions AS (
    SELECT DISTINCT
        household_key,
        day AS redemption_day,
        campaign,
        coupon_upc
    FROM {{ ref('stg_coupon_redempt') }}
),

baseline AS (
    SELECT
        household_key,
        avg_days_between_purchases AS baseline_gap,
        avg_spend_per_trip,
        total_purchases,
        first_purchase_day,
        last_purchase_day
    FROM {{ ref('int_customer_purchase_frequency') }}
),

post_promo_transactions AS (
    SELECT
        r.household_key,
        r.redemption_day,
        r.campaign,
        r.coupon_upc,
        t.day AS return_day,
        t.sales_value,
        t.basket_id
    FROM redemptions r
    LEFT JOIN {{ ref('stg_transaction_data') }} t
        ON r.household_key = t.household_key
        AND t.day > r.redemption_day
        AND t.day <= r.redemption_day + 56
),

post_promo_summary AS (
    SELECT
        household_key,
        redemption_day,
        campaign,
        coupon_upc,
        COUNT(DISTINCT basket_id) AS post_promo_trips,
        SUM(sales_value) AS post_promo_revenue,
        MIN(return_day) - redemption_day AS days_to_first_return
    FROM post_promo_transactions
    GROUP BY household_key, redemption_day, campaign, coupon_upc
)

SELECT
    p.household_key,
    p.redemption_day,
    p.campaign,
    p.coupon_upc,
    p.post_promo_trips,
    p.post_promo_revenue,
    p.days_to_first_return,
    b.baseline_gap,
    CASE 
        WHEN p.days_to_first_return < b.baseline_gap THEN TRUE 
        ELSE FALSE 
    END AS returned_faster_than_baseline,
    CASE 
        WHEN p.post_promo_revenue > ((56.0 / b.baseline_gap) * b.avg_spend_per_trip) THEN TRUE 
        ELSE FALSE 
    END AS above_baseline_revenue
FROM post_promo_summary p
LEFT JOIN baseline b
    ON p.household_key = b.household_key