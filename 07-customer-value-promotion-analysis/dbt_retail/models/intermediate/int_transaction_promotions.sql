WITH transactions AS (
    SELECT * FROM {{ ref('stg_transaction_data') }}
),

coupon_redemptions AS (
    SELECT 
        cr.household_key,
        cr.day,
        cr.coupon_upc,
        cr.campaign,
        c.product_id
    FROM {{ ref('stg_coupon_redempt') }} cr
    LEFT JOIN {{ ref('stg_coupon') }} c
        ON cr.coupon_upc = c.coupon_upc
),

causal AS (
    SELECT * FROM {{ ref('stg_causal_data') }}
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
    cr.campaign,
    cr.coupon_upc,
    CASE WHEN cr.household_key IS NOT NULL THEN TRUE ELSE FALSE END AS is_coupon_redeemed,
    CASE WHEN c.display != '0' AND c.display IS NOT NULL THEN TRUE ELSE FALSE END AS is_on_display,
    CASE WHEN c.mailer != '0' AND c.mailer IS NOT NULL THEN TRUE ELSE FALSE END AS is_in_mailer

FROM transactions t
LEFT JOIN coupon_redemptions cr
    ON t.household_key = cr.household_key
    AND t.day = cr.day
    AND t.product_id = cr.product_id
LEFT JOIN causal c
    ON t.product_id = c.product_id
    AND t.store_id = c.store_id
    AND t.week_no = c.week_no