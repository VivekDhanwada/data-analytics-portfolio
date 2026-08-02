CREATE OR REPLACE VIEW `dunnhumby-retail-analytics.analytics.clean_causal_data` AS
SELECT
    product_id, store_id, week_no,
    MAX(display) AS display,
    MAX(mailer) AS mailer
FROM `dunnhumby-retail-analytics.raw.causal_data`
GROUP BY product_id, store_id, week_no;


CREATE OR REPLACE VIEW `dunnhumby-retail-analytics.analytics.clean_coupon_data` AS
SELECT coupon_upc, product_id, campaign
FROM `dunnhumby-retail-analytics.raw.coupon`
GROUP BY coupon_upc, product_id, campaign;