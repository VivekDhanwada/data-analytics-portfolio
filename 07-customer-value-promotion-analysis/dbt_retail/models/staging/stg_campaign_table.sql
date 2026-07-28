SELECT description, household_key, campaign
FROM {{ source('raw', 'campaign_table') }}