SELECT household_key, age_desc, marital_status_code, income_desc, homeowner_desc, hh_comp_desc, household_size_desc, kid_category_desc
FROM {{ source('raw', 'hh_demographic') }}