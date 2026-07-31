# dbt_retail

dbt transformation layer for the Customer Value & Promotion Effectiveness Analysis project.

## Project Structure

- **Staging:** 8 models, one per raw source table. Light cleaning and deduplication.
- **Intermediate:** 4 models. Business logic including promoted transaction flagging, customer purchase frequency baseline, promotion effectiveness measurement, and churn classification.
- **Marts:** 3 models materialised as tables. `fct_promotion_effectiveness`, `dim_customer`, `dim_campaign` -- the final analytical layer consumed by Power BI.

## Running the Project

```bash
dbt run        # run all models
dbt test       # run all 14 schema tests
dbt build      # run models and tests together
```

## Data Quality Tests

14 schema tests across mart tables covering uniqueness, not-null constraints, and accepted value validation for boolean flags.

## CI

GitHub Actions workflow runs `dbt build` automatically on every push to main affecting this project folder.