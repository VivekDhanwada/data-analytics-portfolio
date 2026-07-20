SELECT
    product_id,
    store_id,
    week_no,
    MAX(display) AS display,
    MAX(mailer) AS mailer
FROM {{ source('raw', 'causal_data') }}
GROUP BY product_id, store_id, week_no