# Spotify Snowflake Pipeline

> 🚧 **In Progress** — this pipeline is actively being built. Sections below will be filled in as each stage is completed.

An end-to-end ELT pipeline extracting data from the Spotify API, loading it through AWS into Snowflake, and modelling it for reporting in Power BI.

**Purpose:** Built to develop hands-on Snowflake and cloud pipeline fluency — analytics engineering depth supporting a Commercial Data Analyst skill set.

## Overview

This project builds a full Extract-Load-Transform pipeline: Python extracts data from the Spotify API, raw data lands in AWS S3, Snowpipe automatically loads it into Snowflake, SQL transforms it into a dimensional model, and Power BI connects for reporting.

## Analytical Questions

*To be added once pipeline scope is finalised.*

## Data

**Source:** Spotify Web API

**Extraction method:** Python (`spotipy`)

**Tables/entities:** *To be added once schema is built.*

## Methodology

*To be added once transformation logic is built.*

## Tech Stack

- Python (`spotipy`, `boto3`) — extraction and AWS integration
- AWS S3 — raw data staging
- Snowpipe — automated ingestion into Snowflake
- Snowflake — data warehouse, SQL transformations, dimensional modelling
- Power BI and DAX — dashboard and reporting layer

## Project Structure