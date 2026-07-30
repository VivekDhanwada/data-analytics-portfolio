SELECT description, campaign, start_day, end_day
FROM {{ ref('stg_campaign_desc') }}