SELECT description, campaign, start_day, end_day
FROM {{ source('raw', 'campaign_desc') }}