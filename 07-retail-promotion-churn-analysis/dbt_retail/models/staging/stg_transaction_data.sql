SELECT household_key, day, basket_id, product_id, quantity, sales_value, retail_disc, store_id, trans_time, week_no, coupon_disc, coupon_match_disc
FROM {{ source('raw', 'transaction_data') }}