# Australian Population & Migration Trends Analysis

Analysis of 20 years of ABS census data (1996–2016) across three interactive Power BI dashboards covering national population growth, country-of-birth composition, and fastest-growing migrant communities by state and gender.

## Overview

This project uses Australian Bureau of Statistics (ABS) census data to explore how Australia's population and migration patterns changed over two decades. Three Power BI dashboards were built to address distinct analytical objectives, progressing from national-level trends to granular migration insights.

## Dashboards

**Dashboard 1 — National Population Overview**
Covers total population growth, state-level comparisons, gender distribution, and age group demographics from 1996 to 2016. Interactive slicers allow filtering by region, sex, and year.

**Dashboard 2 — Population by Country of Birth**
Explores the country-of-birth composition of Australian residents, revealing migration diversity across gender and region. Top 10 origin countries visualised with clustered column, pie, and horizontal bar charts.

**Dashboard 3 — Fastest-Growing Migrant Communities (2001–2016)**
Storytelling dashboard identifying countries with the highest percentage population growth, excluding dominant groups. Nepal grew from 2,430 to over 59,000 residents — a 2,330% increase. Countries like Bhutan, Liberia, and Mongolia also showed exceptional relative growth.

## Key Findings

- Australia's population grew steadily from 1996 to 2016, with NSW and Victoria contributing the largest absolute increases.
- The population shows signs of ageing, with increasing representation in the 50–74 age cohort.
- England, India, China, and New Zealand are the largest migrant communities.
- Nepal was the fastest-growing migrant group in percentage terms, increasing 2,330% from 2001 to 2016.
- Bhutan, Liberia, and Mongolia also showed high relative growth, reflecting humanitarian and education migration pathways.

## Tools & Methodology

- Power BI Web (Mac environment — Power BI Desktop unavailable)
- ABS census data across five census years: 1996, 2001, 2006, 2011, 2016
- Percentage growth for Dashboard 3 pre-calculated in Excel due to DAX limitations on Power BI Web
- Interactive slicers for region, sex, age, and country of birth across all dashboards

## Limitations

- Data covers 1996–2016 only; post-2016 trends not captured
- Power BI Web does not support DAX or custom measures — percentage growth calculated externally in Excel
- Top 10 country selections are static, not dynamically updated by slicers
- Age categories grouped for clarity (e.g. 0–24, 25–49)

## Files

- `Dashboard 1.pbix` — National Population Overview
- `Dashboard 2.pbix` — Population by Country of Birth
- `Dashbboard 3.pbix` — Fastest-Growing Migrant Communities
- `Report.pdf` — Full client briefing report with visualisations and findings