# NEM Emissions & Bidding Analysis

Analysis of Australian National Electricity Market (NEM) emissions intensity and generator bidding behaviour using Python, covering 5-minute interval dispatch and emissions data across NEM regions.

## Overview

This project analyses emissions intensity and fossil fuel generator bidding behaviour in the Australian National Electricity Market. The analysis compares selected 2019 and 2025 dispatch periods to identify how carbon intensity changed across regions and how fossil fuel generator bidding behaviour shifted over time.

The project was completed as part of a Macquarie University capstone project and awarded a Distinction.

The dataset covers 1.6M+ rows of 5-minute interval dispatch and emissions data.

## Analytical Questions

1. How did carbon intensity change across NEM regions between 2019 and 2025?
2. How did fossil fuel generator bidding behaviour shift over the same period?
3. What regional and intra-daily emissions patterns were visible in the data?

## Key Findings

**NSW showed the strongest carbon intensity improvement**
NSW achieved a 21.7% reduction in carbon intensity between 2019 and 2025, compared with a national average decline of 7.7%.

**Fossil generator bidding became more volatile**
Fossil generators shifted from baseload providers toward more strategic peak-pricing behaviour. The fossil bid price interquartile range widened from $85/MWh to $210/MWh.

**Regional emissions patterns varied significantly**
Time series and intra-daily trend charts showed clear differences in emissions profiles across NEM regions, highlighting the importance of region-level analysis.

## Tools & Techniques

- Python
- pandas
- Matplotlib
- 5-minute interval dispatch data
- Data cleaning and aggregation
- Time series analysis
- Regional comparison
- Analytical reporting

## Files

- `cleandata.py` - Data extraction, cleaning, and preparation
- `plot1.py` to `plot5.py` - Individual visualisation scripts for project charts
- `Report.pdf` - Group client report with full findings and recommendations

## Skills Demonstrated

- Python data cleaning and preparation
- Time series analysis using 5-minute interval dispatch data
- Data aggregation and regional comparison
- Matplotlib visualisation and analytical reporting
- Translating technical findings into a client-style analytical report

## Contribution Note

This was a group capstone project. My individual contribution focused on Python code development for the bidding behaviour analysis and data cleaning. The final report represents collaborative group work.

## Data Source

Australian National Electricity Market emissions and dispatch data accessed through the CSIRO NEM emissions data source.

## Limitations

- The project compares selected 2019 and 2025 dispatch periods, so findings should be interpreted within the scope of the available data.
- The final report was produced collaboratively, so individual contribution is stated separately above.
- The analysis is descriptive and does not claim causal attribution for market behaviour changes.