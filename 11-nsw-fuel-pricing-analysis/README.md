# NSW Fuel Pricing Analysis

A production-grade analytics pipeline built on official NSW Government fuel pricing data, testing whether the widely-cited "fuel price cycle" actually holds at a granular, actionable level.

**Business Question:** Is there a genuinely reliable "good time to buy" fuel price pattern, and does it hold consistently enough across Sydney suburbs and brands to be actionable, or does common cycle advice wash out once you look at the real data?

## Status

In progress. Built and tested so far: OAuth authentication, ingestion of live prices and station reference data, filtering of non-fuel entries, and a data validation script. Everything else listed under Tech Stack is planned.

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
- `Get All Prices`, last known price per station per fuel type
- `Get Reference Data` (`/lovs`), station name, brand, full address, and coordinates

**Scope:** The raw landing zone holds the full API response (NSW plus a small number of ACT stations), after removing non-fuel entries. Sydney metro scoping is applied in the transformation layer using station addresses and coordinates. All reported fuel types are kept (unleaded 91, diesel, premium grades, E10, and others), expanded beyond an initial unleaded-91-only scope to support a live "is today a good day to fill up" query for any fuel type.

**First live pull (8 Oct 2026, after filtering):** 9,673 price rows across 2,379 stations (2,315 NSW, 63 ACT, 1 unparsed address) and 9 fuel type codes.

## Data Validation

The first live pull was profiled before any pipeline was built on top of it (`src/validate.py`).

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

## Methodology

*TBD, will be finalised once the historical backfill and dbt marts are built.*

## Tech Stack

**Phase 1 (build/demo, target enterprise stack):**
- Python (ingestion and validation, built)
- AWS S3, Lambda, EventBridge Scheduler, Docker (planned)
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
│   ├── config.py        # API URLs, credentials loading, constants
│   ├── auth.py          # OAuth token retrieval
│   ├── ingest.py        # Fetch prices and reference data, filter non-fuel entries, save raw JSON
│   └── validate.py      # Profile the raw pull: nulls, duplicates, ranges, freshness, coordinates
├── data/                # Local landing zone (gitignored), mirrors future S3 partition structure
├── dbt/                 # TBD
├── docs/                # TBD, screenshots, architecture diagram
├── .gitignore
└── README.md
```

## Skills Demonstrated

**Data Engineering**
- Data source vetting and governance, evaluated and rejected multiple candidate sources on explicit Terms of Service grounds before selecting an officially licensed government API
- Python ingestion with OAuth 2.0 client-credentials authentication and credentials kept out of source control
- Profiling a live source before building on it: null, duplicate, range, freshness and referential checks, plus a manual spot-check against the real-world source
- *Remaining items TBD as the pipeline is built: cloud landing zone, Iceberg table design, dbt layered modelling, containerised deployment, orchestration*

**Analytics Engineering**
*TBD*

**Analytics**
*TBD*

## Hard Problems Solved

- **No geography filter on the all-prices endpoint.** It returns all of NSW plus some ACT stations, so Sydney scoping has to be applied downstream using station coordinates and addresses.
- **Non-fuel entries in the station reference data.** EV charging poles (AGL, Chargefox, Evie Networks and others) and placeholder listings sit alongside real stations. Maintaining a brand blocklist would miss new ones, so the filter is evidence-based instead: a station is kept only if it reports at least one non-EV price. This removed 686 of 3,065 entries.
- **Stale "current" prices.** The prices endpoint returns the last known price per station per fuel type, however old (up to 979 days in the first pull), so the pull date is not the price date. The staging layer will key rows on station, fuel type and `lastupdated`, and flag stale rows rather than treat them as current.
- **UTC timestamps.** `lastupdated` is in UTC, not Sydney time. Daylight saving changes the offset during the year, so timestamps are converted using the `Australia/Sydney` timezone, not a fixed offset.
- **Orphan prices.** About 0.8% of price rows (78 rows, 17 station codes) reference stations that do not exist in the reference data, so the staging layer must handle unmatched prices explicitly and track the count.
- **Suspect source values.** Some records look unreliable, for example three Sydney stations showing an identical E85 price of 475.0 that had not been updated for over a year, and what appears to be one regional station listed twice under different addresses. Raw data is kept as received and these are flagged in staging.
- **Inconsistent fuel-type coverage per station.** Not every station reports every fuel type, so the marts layer must handle real nulls rather than assume a uniform grid.
- **Incremental load design.** Per the API documentation, `Get New Prices` tracks "new since" per API key per day, not by a timestamp the caller supplies, which has implications for incremental loading and failure recovery. This is documented behaviour that has not yet been tested.

## AI Tooling Use and Control

*TBD, to document which parts of the pipeline were AI-assisted, what was reviewed/verified before being run against real data or credentials, and specific examples of catching unverified or overstated claims during the build (e.g. cross-checking data-source terms of service directly rather than trusting summarised claims).*

## Limitations

- Only one snapshot has been collected so far. Price history for the cycle analysis will come from the historical monthly files on Data.NSW, which have not yet been downloaded or profiled.
- Historical continuity has been confirmed at the dataset level only, not for the Sydney-filtered, per-fuel-type slice.
- The spot-check covered three stations. Timestamps were validated against the current UTC time, not against individual stations.
- Some outliers (for example very high regional prices) have not been individually verified.
- *Further limitations TBD as the analysis is completed.*

## Dashboard Preview

*TBD.*

## Business Recommendation

*TBD.*

## Key Takeaway

*TBD.*