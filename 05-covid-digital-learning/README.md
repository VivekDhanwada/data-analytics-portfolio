# COVID-19 Impact on Digital Learning

Analysis of how the COVID-19 pandemic affected student engagement with digital learning platforms across five US school districts in 2020, using R and ggplot2.

## Overview

This project analyses engagement and broadband access data from five school districts (IDs: 1000, 1039, 1044, 1052, 1131) across 2020 to understand how the pandemic shifted student interaction with online learning tools. The analysis covers data cleaning, exploratory visualisation, and findings across three analytical questions.

This project was completed as part of the Master of Business Analytics program at Macquarie University.

## Analytical Questions

1. What was the relationship between digital connectivity and student engagement in 2020?
2. How did engagement change during different phases of the COVID-19 pandemic?
3. Which types of education technology platforms showed the strongest engagement patterns?

## Key Findings

- District 1044 contributed the largest data volume, while District 1131 had significantly lower engagement data throughout.
- A strong positive correlation exists between broadband access and engagement index. Higher connectivity consistently corresponded with higher participation.
- Engagement and percentage access declined between June and August 2020, followed by a recovery phase across all five districts.
- Districts 1052 and 1000 exceeded pre-COVID engagement levels post-recovery, suggesting accelerated digital adoption. District 1039 did not fully recover, indicating ongoing structural challenges.
- Google Docs was the highest-engagement learning platform across all districts. Learning & Curriculum platforms dominated overall engagement, consistent with the majority of available tools being categorised as Learning & Curriculum.

## Tools & Techniques

- R, ggplot2, plotly, dplyr, tidyverse
- Data cleaning: standardising inconsistent state and locale labels, handling date format errors, removing duplicates and missing values
- Visualisations: bar charts, scatter plots, line graphs, faceted plots, and interactive plotly charts

## Skills Demonstrated

- R-based exploratory data analysis
- Data cleaning and preparation
- ggplot2 visualisation
- Correlation and trend analysis
- Education technology usage analysis
- Communicating pandemic-related digital learning insights

## Files

- `47895403.Rmd` - R Markdown file with full analysis and code
- `Report.pdf` - Submitted report with visualisations and findings

## Data Source

LearnPlatform COVID-19 Impact on Digital Learning dataset, including district engagement, product information, and district demographic data across five US school districts in 2020.