SELECT product_id, department, manufacturer, brand, curr_size_of_product, commodity_desc, sub_commodity_desc
FROM {{ source('raw', 'product') }}