SELECT household_key, day, coupon_upc, campaign
FROM {{ source('raw', 'coupon_redempt') }}
GROUP BY household_key, day, coupon_upc, campaign
