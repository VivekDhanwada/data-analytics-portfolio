# Customer Value & Promotion Effectiveness Analysis

A commercial retail analytics project using Dunnhumby "The Complete Journey" dataset to analyse customer segments and promotional strategies, ending with a concrete budget reallocation recommendation.

**Business Question:** How should a retailer reallocate promotional spend to maximise repeat purchasing and long-term customer value?

## Overview

This project analyses two years of real retail transaction data covering household demographics, purchase history, coupon redemptions, and campaign exposure. The analysis identifies which customer segments generate the greatest post-promotion revenue lift and which segments churn regardless of promotional activity, producing a data-driven recommendation on where to increase and reduce promotional investment.

The project follows a full modern analytics stack: Python ingestion pipeline, cloud data warehousing in BigQuery, SQL transformations with star schema modelling, and an interactive Power BI dashboard with DAX measures.

## Analytical Questions

1. Which customer segments generate the greatest revenue lift following a promotion?
2. Do promotions accelerate repeat purchasing beyond a customer's baseline inter-purchase frequency?
3. Which segments churn regardless of promotional activity, and what does this mean for spend allocation?
4. Where should the retailer reallocate promotional budget to maximise long-term customer value?

## Data

**Source:** Dunnhumby "The Complete Journey" — real retail transaction data from a US grocery retailer covering approximately 2,500 households over two years.

**Tables:**
- `transaction_data` — line-level purchase records including spend, discounts, and basket identifiers
- `causal_data` — store-level promotional display and mailer activity by product and week
- `hh_demographic` — household demographics including age, income, household size, and marital status
- `coupon` — products included in each campaign coupon
- `coupon_redempt` — household-level coupon redemption records
- `campaign_desc` — campaign type and date range
- `campaign_table` — households targeted by each campaign
- `product` — product master including department, brand, and commodity

## Methodology

**Long-term value proxy:** Post-promotion revenue within an 8-week window compared to each customer's historical baseline spend.

**Promotion effectiveness definition:** A promotion is effective if the customer generated above-baseline revenue AND returned faster than their average inter-purchase gap within 8 weeks post-promotion.

**Churn definition:** A household with no recorded transaction for 12+ weeks following their last purchase.

## Tech Stack

- Python (ingestion and validation pipeline)
- Google BigQuery (cloud data warehouse)
- SQL (CTEs, window functions, star schema modelling)
- Power Query (light shaping in Power BI)
- Power BI and DAX (interactive dashboard)

## Project Structure