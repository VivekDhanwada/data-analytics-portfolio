# NSW Fuel Pricing Analysis

A production-grade analytics pipeline built on official NSW Government fuel pricing data, testing whether the widely-cited "fuel price cycle" actually holds at a granular, actionable level.

**Business Question:** Is there a genuinely reliable "good time to buy" fuel price pattern, and does it hold consistently enough across Sydney suburbs and brands to be actionable, or does common cycle advice wash out once you look at the real data?

## Status

In progress. Built and tested so far: OAuth authentication, ingestion of live prices and station reference data with filtering of non-fuel entries, a data validation script, upload of raw JSON to S3, and a Docker image that runs the same handler locally under the Lambda runtime emulator. The historical monthly files (45 months, Jan 2023 to Sep 2026) are also loaded despite inconsistent layouts, converted to Parquet with a rejects file, and uploaded to S3. Not yet done: deployment to AWS Lambda and the daily schedule (live pulls so far are manual), and everything from Snowflake onward.

## Executive Summary

*TBD, to be written once the analysis is complete.*

## Overview

This project ingests live and historical NSW fuel pricing data via the official FuelCheck API (api.nsw.gov.au) and the published monthly price history files, covering price, brand, and station-level detail for Sydney metro service stations. NSW law requires stations to report any price change within 30 minutes, making this a genuinely near-real-time public data source.

The project follows the ADLC (Analytics Development Lifecycle) pattern: raw ingestion, layered dbt transformation, automated testing, orchestration, and a natural-language query layer on top of the finished marts. It is deliberately built in two phases, a production-style Snowflake/dbt/Airflow stack first, then re-platformed to a cost-sustainable Google Cloud setup for long-term public availability (see [Architecture](#architecture) below).

## Analytical Questions

1. Does the fuel price cycle actually hold in Sydney data, a genuine, roughly regular rise-then-fall pattern, or is it messier than commonly cited advice suggests?
2. Which Sydney suburbs are reliably cheaper on average, and does that ranking hold over time?
3. Which brand is cheapest on average, consistently, not just in a single snapshot?
4. *(Stretch, deprioritized until 1 to 3 are answered)* Do specific brands lead or lag the market when the cycle turns?

## Data

**Source:** NSW FuelCheck, published by NSW Fair Trading / Data.NSW, official government data, [CC BY-SA licensed](https://data.nsw.gov.au). Not scraped. The live feed is accessed via a registered developer app and OAuth 2.0 client-credentials flow, and the history is downloaded from the published monthly files.

**Live API endpoints used:**
- `Get All Prices`, last known price per station per fuel type
- `Get Reference Data` (`/lovs`), station name, brand, full address, and coordinates

**Historical files:** 45 monthly files, Jan 2023 to Sep 2026, a mix of XLSX and CSV, each holding price-change events (station, fuel type, timestamp, price). The source publishes files back to Aug 2016. Months before 2023 have not been profiled.

**Scope:** The raw landing zone holds the full response (NSW plus a small number of ACT stations), after removing non-fuel entries. Sydney metro scoping is applied in the transformation layer using suburb, postcode and coordinates. All reported fuel types are kept (unleaded 91, diesel, premium grades, E10, and others), expanded beyond an initial unleaded-91-only scope to support a live "is today a good day to fill up" query for any fuel type.

**First live pull (8 Oct 2026, after filtering):** 9,673 price rows across 2,379 stations (2,315 NSW, 63 ACT, 1 unparsed address) and 9 fuel type codes.

**Landing zone:** raw data is written to S3 in Sydney (`ap-southeast-2`) with Hive-style partitions:
- `raw/prices/dt=YYYY-MM-DD/` and `raw/stations/dt=YYYY-MM-DD/`, live JSON. A rerun on the same day overwrites that day's file, so a retry cannot create duplicates.
- `raw/historical/month=YYYY-MM/`, clean Parquet, one file per month.
- `raw/historical_source/month=YYYY-MM/`, the original files exactly as published, kept so the cleaning can be rerun.
- `raw/historical_rejects/month=YYYY-MM/`, rows that could not be repaired.

## Data Validation

**Live pull.** The first live pull was profiled before any pipeline was built on top of it (`src/validate.py`).

| Check | Result |
|---|---|
| Null values in stationcode, fueltype, price, lastupdated | 0 |
| Duplicate (station, fuel type) pairs | 0 |
| EV charger rows remaining | 0 |
| Stations outside the NSW/ACT bounding box | 0 |
| Price rows with no matching station in reference data | 78 rows across 17 station codes |
| Price rows updated within 1 day / 7 days / 30 days | 54.1% / 77.3% / 99.0% |
| Oldest price in the pull | 979 days |

**Spot-check against the live source:** three stations in different suburbs (West Ryde, Five Dock, South Coogee) were compared with the FuelCheck app, and all fuel-type prices matched the pipeline output. The app does not display update times, so timestamps were checked separately: the newest `lastupdated` value in the pull sat within minutes of the current UTC time, confirming the field is UTC.

**Historical files.** All 45 files were profiled and loaded through `src/historical.py`, then converted by `src/convert_history.py`.

| Check | Result |
|---|---|
| Months loaded | 45 (Jan 2023 to Sep 2026) |
| Rows read | 3,645,739 |
| Rows written to clean Parquet | 3,645,152 |
| Rows rejected (missing fuel type, timestamp or price) | 587 (0.016%), all in the ten 2023 files |
| Files that needed special handling | 13 of 45 |
| Timestamps outside their file's month, after the loader fixes | 0 |
| Fuel codes | 9 (B20, DL, E10, E85, LPG, P95, P98, PDL, U91), not every code in every month |

**Timezone of the history.** History timestamps are Sydney local time, while the live API is UTC. Two checks support this: one station's price change from the live API appeared in the August 2026 file exactly 10 hours later, and the October 2023, 2024 and 2025 files have no rows in the 2am hour on the day clocks go forward.

**Fill-down check.** In the ten 2023 files, station name, address and brand are written only on the first row of a run and left blank after it, so the loader fills them down. To test this, 96.9% of the (name, address) pairs in October 2023 also appear in November 2023, against 98.4% between November and December 2023, two files that need no fill-down. The pairs are real stations, but this does not prove each individual price sits on the right station.

## Methodology

*TBD, will be finalised once the dbt marts are built.*

## Tech Stack

**Phase 1 (build/demo, target enterprise stack):**
- Python, ingestion, validation and history loading (built)
- AWS S3 landing zone with a scoped IAM user (built)
- Parquet via pyarrow for the history (built)
- Docker image on the AWS Lambda base image, tested locally (built)
- AWS Lambda and EventBridge Scheduler (planned)
- Snowflake, Apache Iceberg tables (planned)
- dbt Core, staging / intermediate / marts (planned)
- Apache Airflow, orchestration built and demoed separately from day-to-day scheduling (planned; see Architecture)
- Cube Core + MCP, semantic layer / natural-language query (planned)
- Power BI (planned)

**Phase 2 (long-term live serving, cost-sustainable, planned):**
- Google BigQuery
- Google Cloud Scheduler + Cloud Functions
- dbt Core (BigQuery adapter)
- Cube Core (re-pointed)
- Looker Studio (public live dashboard)

## Architecture

This project is deliberately built in two phases, not one:

1. **Snowflake phase**, built and run on the full target stack (S3 to Snowpipe to Iceberg RAW to dbt to Airflow) to demonstrate that specific skill set on a production-style pipeline.
2. **BigQuery phase**, before the Snowflake trial period ends, the same pipeline logic is re-platformed to Google Cloud's permanent free tier, so the project keeps running and stays publicly queryable indefinitely at effectively zero ongoing cost.

This is a deliberate infrastructure decision, not a compromise: it's documented here explicitly rather than left for someone to discover that the live-running version differs from the initially-built version.

*Architecture diagram, TBD.*

## Project Structure

```
11-nsw-fuel-pricing-analysis/
├── src/
│   ├── config.py           # API URLs, credentials loading, constants
│   ├── auth.py             # OAuth token retrieval
│   ├── ingest.py           # Fetch prices and reference data, filter non-fuel entries, save locally, upload to S3
│   ├── validate.py         # Profile the live pull: nulls, duplicates, ranges, freshness, coordinates
│   ├── historical.py       # Load one monthly history file: find the header, fill down, parse dates, check
│   ├── convert_history.py  # Convert all months to clean Parquet, write a rejects file
│   └── upload_history.py   # Upload Parquet, original files and rejects to S3
├── data/                   # Local copy of the landing zone (gitignored)
├── dbt/                    # TBD
├── docs/                   # TBD, screenshots, architecture diagram
├── Dockerfile              # Lambda container image
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## Skills Demonstrated

**Data Engineering**
- Data source vetting and governance, evaluated and rejected multiple candidate sources on explicit Terms of Service grounds before selecting an officially licensed government API
- Python ingestion with OAuth 2.0 client-credentials authentication and credentials kept out of source control
- Profiling a live source before building on it: null, duplicate, range, freshness and referential checks, plus a manual spot-check against the real-world source
- Loading 45 monthly files with inconsistent layouts, date formats and timezones into one clean schema, with a rejects file and counts so no rows disappear silently
- Testing a data-cleaning assumption against clean months before relying on it, and keeping the original files so the cleaning can be rerun
- *Remaining items TBD as the pipeline is built: Lambda deployment and scheduling, Iceberg table design, dbt layered modelling, orchestration*

**Analytics Engineering**
*TBD*

**Analytics**
*TBD*

## Hard Problems Solved

- **No geography filter on the all-prices endpoint.** It returns all of NSW plus some ACT stations, so Sydney scoping has to be applied downstream using station coordinates and addresses.
- **Non-fuel entries in the station reference data.** EV charging poles (AGL, Chargefox, Evie Networks and others) and placeholder listings sit alongside real stations. Maintaining a brand blocklist would miss new ones, so the filter is evidence-based instead: a station is kept only if it reports at least one non-EV price. This removed 686 of 3,065 entries.
- **Stale "current" prices.** The prices endpoint returns the last known price per station per fuel type, however old (up to 979 days in the first pull), so the pull date is not the price date. The staging layer will key rows on station, fuel type and `lastupdated`, and flag stale rows rather than treat them as current.
- **Two timezones.** `lastupdated` in the live API is UTC, while the history files are in Sydney local time. Staging converts both using the `Australia/Sydney` timezone, not a fixed offset. When clocks go back in April the 2:00 to 2:59 hour happens twice, so Sydney local timestamps in that hour cannot be converted to UTC unambiguously.
- **Inconsistent history file layouts.** Ten 2023 files have a title row above the header and blank station cells, one 2026 file has a "Time run" line above its header, two CSVs use day-first dates without seconds, and the 2023 dates are text with AM/PM. The catalogue's format column is unreliable (blank for some files, wrong for others), so the loader finds the header by content and tries several date formats.
- **No station ID in the history.** The history identifies stations by name and address only, while the live API uses a numeric code. Two different stations can share a name (two Coles Express stations in Greenacre), so the station key is name plus address, and linking history to live data needs a name and address match in dbt.
- **Duplicate events.** Some files hold repeated rows for the same station, fuel and timestamp, up to 9 a month in the 2023 files and 96 in June 2025, where the CSV timestamps only have minute precision. Staging needs a dedup rule.
- **Orphan prices.** About 0.8% of live price rows (78 rows, 17 station codes) reference stations that do not exist in the reference data, so the staging layer must handle unmatched prices explicitly and track the count.
- **Suspect source values.** Some records look unreliable, for example three Sydney stations showing an identical E85 price of 475.0 that had not been updated for over a year, and what appears to be one regional station listed twice under different addresses. Raw data is kept as received and these are flagged in staging.
- **Inconsistent fuel-type coverage per station.** Not every station reports every fuel type, so the marts layer must handle real nulls rather than assume a uniform grid.
- **Incremental load design.** Per the API documentation, `Get New Prices` tracks "new since" per API key per day, not by a timestamp the caller supplies, which has implications for incremental loading and failure recovery. This is documented behaviour that has not yet been tested.

## AI Tooling Use and Control

*TBD, to document which parts of the pipeline were AI-assisted, what was reviewed/verified before being run against real data or credentials, and specific examples of catching unverified or overstated claims during the build (e.g. cross-checking data-source terms of service directly rather than trusting summarised claims).*

## Limitations

- Live collection is manual. The daily Lambda and schedule are not deployed, so the live data in S3 is a single snapshot.
- Only Jan 2023 to Sep 2026 of the history is loaded. Earlier monthly files back to Aug 2016 exist but have not been profiled.
- Historical continuity has been confirmed at the dataset level only, not for the Sydney-filtered, per-fuel-type slice.
- Monthly row counts roughly double from March 2026 (about 125,000 to 155,000 rows, against about 60,000 to 80,000 through 2025) for a reason not yet investigated, so month-to-month event counts may not be comparable.
- The fill-down for the 2023 files is supported by a statistical check, not verified row by row. The 587 rejected rows are excluded from the clean data.
- The spot-check covered three stations. Timestamps were validated against the current UTC time and a single station, not against every station.
- Some outliers (for example very high regional prices) have not been individually verified.
- *Further limitations TBD as the analysis is completed.*

## Dashboard Preview

*TBD.*

## Business Recommendation

*TBD.*

## Key Takeaway

*TBD.*