from google.cloud import bigquery
import pandas as pd
from scipy.stats import chi2_contingency

# Connect to BigQuery
client = bigquery.Client(project="dunnhumby-retail-analytics")

# Query -- get promoted vs non-promoted customers and whether they made a repeat purchase
query = """
WITH customer_promotion AS (
    SELECT
        household_key,
        MAX(CASE WHEN is_coupon_redeemed = TRUE 
                   OR is_on_display = TRUE 
                   OR is_in_mailer = TRUE 
            THEN 1 ELSE 0 END) AS was_promoted,
        COUNT(DISTINCT day) AS total_purchase_days
    FROM `dunnhumby-retail-analytics.analytics_analytics.fct_promotion_effectiveness`
    GROUP BY household_key
)

SELECT
    was_promoted,
    CASE WHEN total_purchase_days > 1 THEN 1 ELSE 0 END AS made_repeat_purchase,
    COUNT(*) AS customer_count
FROM customer_promotion
GROUP BY was_promoted, made_repeat_purchase
ORDER BY was_promoted, made_repeat_purchase
"""

df = client.query(query).to_dataframe()
print("Raw data:")
print(df)

# Build contingency table
# Rows: promoted (0/1), Columns: repeat purchase (0/1)
contingency_table = df.pivot_table(
    index='was_promoted',
    columns='made_repeat_purchase',
    values='customer_count',
    fill_value=0
).values

print("\nContingency table:")
print(contingency_table)

# Run chi-square test
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"\nChi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Degrees of freedom: {dof}")

if p_value < 0.05:
    print("\nResult: REJECT null hypothesis")
    print("There IS a statistically significant difference in repeat purchase rate between promoted and non-promoted customers.")
else:
    print("\nResult: FAIL TO REJECT null hypothesis")
    print("There is NO statistically significant difference in repeat purchase rate between promoted and non-promoted customers.")