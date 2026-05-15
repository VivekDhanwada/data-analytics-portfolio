# Customer Retention & Revenue Analysis

Exploratory analysis of customer retention drivers and revenue trends across a 100,000-row synthetic Amazon e-commerce dataset using Tableau.

## Overview

An exploratory analysis of a synthetic Amazon e-commerce dataset (100,000 rows, 20 columns) built across three Tableau dashboards. The project investigates what drives customer retention and examines revenue performance across five years (2020–2024).

## Business Questions

1. Do discounts influence repeat purchasing behaviour?
2. Does retention vary across product category, price tier, or payment method?
3. What does revenue performance look like over time, and are there notable patterns?

## Key Findings

**Dashboard 1 — Impact of Discount on Customer Retention**
59.75% of repeat customers had a discounted first order, almost identical to the 59.85% rate across all customers. Discounts do not appear to drive retention.

**Dashboard 2 — Retention Across Key Segments**
Retention holds at ~86% regardless of product category, price tier, or payment method. No tested segment factor meaningfully differentiates retention rates.

**Dashboard 3 — Temporal Business Performance**
Total revenue of $91.8M is stable year-on-year. A consistent February revenue dip (~9.4% below monthly average) appears across all five years, suggesting a recurring seasonal demand pattern.

## Limitations

- Findings are descriptive, not causal
- Factors outside the dataset (customer service, delivery experience) may better explain retention consistency
- Dataset is synthetic — patterns may not reflect real Amazon behaviour

## Files

- `CustomerRetentionRevenueAnalysis.twbx` — Tableau workbook with all three dashboards

## Live Dashboard

[View on Tableau Public](https://public.tableau.com/shared/2RJJMHJR9)
