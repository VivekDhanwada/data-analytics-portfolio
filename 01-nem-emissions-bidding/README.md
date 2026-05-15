# Australian National Electricity Market — Emissions & Bidding Analysis

Analysis of 6 years of 5-minute interval emissions and generator bidding data across all NEM regions, identifying carbon intensity trends and shifts in fossil fuel generator behaviour between 2019 and 2025.

## Overview

This project analyses Australian National Electricity Market (NEM) data sourced via the CSIRO API, covering emissions intensity and generator bidding behaviour across all NEM regions. The analysis was completed as a Macquarie University capstone project and awarded a Distinction.

The dataset covers 1.6M+ rows of 5-minute interval data across 2019 and 2025 dispatch periods.

## Analytical Questions

1. How has carbon intensity changed across NEM regions between 2019 and 2025?
2. How has fossil fuel generator bidding behaviour shifted over this period?
3. What are the intra-daily and regional patterns in emissions intensity?

## Key Findings

- NSW achieved a 21.7% reduction in carbon intensity between 2019 and 2025, compared to a national average decline of only 7.7%.
- Fossil generators shifted from baseload providers to strategic peak-pricers over the same period, with the fossil bid price interquartile range widening from $85/MWh to $210/MWh.
- Regional time series and intra-daily trend charts reveal significant variation in emissions profiles across states.
- Analysis delivered investment recommendations in a structured client report format.

## Tools & Techniques

- Python (Pandas, Matplotlib, Seaborn)
- CSIRO API for data extraction
- 5-minute interval dispatch data across all NEM regions
- Data cleaning, aggregation, and time series visualisation

## Files

- `cleandata.py` — Data extraction, cleaning, and preparation
- `plot1.py` to `plot5.py` — Individual visualisation scripts for each chart
- `Report.pdf` — Group client report with full findings and recommendations

## Notes

This was a group capstone project. The Python code and data cleaning in this repository reflects individual contribution. The report represents collaborative group work across all tasks.

## Data Source

CSIRO NEM emissions API — 5-minute interval dispatch and emissions data across all NEM regions, 2019 and 2025.