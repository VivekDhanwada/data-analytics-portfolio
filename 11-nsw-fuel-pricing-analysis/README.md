# NSW Fuel Pricing Analysis

A production-grade analytics pipeline built on official NSW Government fuel pricing data, testing whether the widely-cited "fuel price cycle" actually holds at a granular, actionable level.

**Business Question:** Is there a genuinely reliable "good time to buy" fuel price pattern, and does it hold consistently enough across Sydney suburbs and brands to be actionable, or does common cycle advice wash out once you look at the real data?

## Executive Summary

*TBD, to be written once the analysis is complete.*

## Overview

This project ingests live and historical NSW fuel pricing data via the official FuelCheck API (api.nsw.gov.au), covering price, brand, and station-level detail for Sydney metro service stations. NSW law requires stations to report any price change within 30 minutes, making this a genuinely near-real-time public data source.

The project follows the ADLC (Analytics Development Lifecycle) pattern: raw ingestion, layered dbt transformation, automated testing, orchestration, and a natural-language query layer on top of the finished marts. It is deliberately built in two phases, a production-style Snowflake/dbt/Airflow stack first, then re-platformed to a cost-sustainable Google Cloud setup for long-term public availability (see [Architecture](#architecture) below).

## Analytical Questions

1. Does the fuel price cycle actually hold in Sydney data, a genuine, roughly regular rise-then-fall pattern, or is it messier than commonly cited advice suggests?
2. Which Sydney suburbs are reliably cheaper on average, and does that ranking hold over time?
3. Which brand is cheapest on average, consistently, not just in a single snapshot?
4. *(Stretch, deprioritized until 1 to 3 are answered)* Do specific brands lead or lag the market when the cycle turns?

## Data

**Source:** NSW FuelCheck API, published by NSW Fair Trading / Data.NSW, official government API, [CC BY-SA licensed](https://data.nsw.gov.au). Not scraped; accessed via a registered developer app and OAuth 2.0 client-credentials flow.

**Endpoints used:**
- `Get All Prices`, current price per station per fuel type
- `Get Reference Data` (`/lovs`), station name, brand, full address, and coordinates

**Scope:** Sydney metro, all reported fuel types (unleaded 91, diesel, premium grades, E10, expanded beyond an initial unleaded-91-only scope to support a live "is today a good day to fill up" query for any fuel type). Historical continuity confirmed at the dataset level; confirming continuity for the specific Sydney-filtered slice is a first-week validation step (see Limitations).

## Methodology

*TBD, will be finalised once the historical backfill and dbt marts are built.*

## Tech Stack

**Phase 1 (build/demo, target enterprise stack):**
- Python (ingestion)
- AWS S3, Lambda, EventBridge Scheduler, Docker
- Snowflake, Apache Iceberg tables
- dbt Core (staging / intermediate / marts)
- Apache Airflow (orchestration, built and demoed separately from day-to-day scheduling; see Architecture)
- Cube Core + MCP (semantic layer / natural-language query)
- Power BI

**Phase 2 (long-term live serving, cost-sustainable):**
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
11-nsw-fuel-pricing-analysis/
├── src/
│ ├── config.py # API URLs, credentials loading, constants
│ ├── auth.py # OAuth token retrieval, tested and working
│ └── ingest.py # Fetch + filter prices & reference data, written, local test pending
├── data/ # Local landing zone (gitignored), mirrors future S3/Iceberg partition structure
├── dbt/ # TBD
├── docs/ # TBD, screenshots, architecture diagram
├── .env.example
├── .gitignore
└── README.md


## Skills Demonstrated

**Data Engineering**
- Data source vetting and governance, evaluated and rejected multiple candidate sources on explicit Terms of Service grounds before selecting an officially licensed government API
- Python ingestion with OAuth 2.0 client-credentials authentication
- *Remaining sections TBD as the pipeline is built: cloud landing zone, Iceberg table design, dbt layered modelling, containerised deployment, orchestration*

**Analytics Engineering**
*TBD*

**Analytics**
*TBD*

## Hard Problems Solved

- No server-side Sydney-geography filter on the live prices endpoint, full-state pulls must be filtered client-side using station reference data.
- Reference data includes non-fuel entries (EV charging poles under brands like AGL, Chargefox, Evie Networks, and blank-brand placeholder listings) that must be excluded before it's usable as a clean station dimension.
- Inconsistent fuel-type coverage per station, not every station reports every fuel type, so the marts layer must handle real nulls rather than assuming a uniform grid.
- The `Get New Prices` endpoint resets its "new since" tracking per API key, per day, it is not a conventional `updated_since` timestamp cursor, which has implications for incremental load design and failure recovery.

## AI Tooling Use and Control

*TBD, to document which parts of the pipeline were AI-assisted, what was reviewed/verified before being run against real data or credentials, and specific examples of catching unverified or overstated claims during the build (e.g. cross-checking data-source terms of service directly rather than trusting summarised claims).*

## Limitations

- Confirming historical data continuity for the Sydney-filtered, per-fuel-type slice specifically (not just the dataset as a whole) is an outstanding validation step.
- *Further limitations TBD as the analysis is completed.*

## Dashboard Preview

*TBD.*

## Business Recommendation

*TBD.*

## Key Takeaway

*TBD.*