SELECT

    coupon_upc,
    product_id,
    campaign
FROM {{ source('raw', 'coupon') }}
GROUP BY product_id, coupon_upc, campaign