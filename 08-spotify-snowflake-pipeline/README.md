# Spotify Snowflake Pipeline

An end-to-end ETL pipeline extracting listening data from the Spotify API, loading it through AWS into Snowflake with fully automated ingestion via Snowpipe.

**Key Result:** Built a fully automated Extract-Transform-Load pipeline using AWS Lambda, S3, and Snowflake Snowpipe. New playlist data flows from the Spotify API into query-ready Snowflake tables with zero manual intervention, verified end-to-end by triggering a live run and confirming row counts increased purely through automated ingestion.

## Overview

This project builds a serverless ETL pipeline: a scheduled AWS Lambda function extracts playlist data from the Spotify API via OAuth, a second Lambda transforms the raw JSON into structured album, artist, and song datasets, and Snowflake's Snowpipe automatically ingests the transformed files into Snowflake tables as soon as they land in S3, with no manual `COPY INTO` required after initial setup.

This project is scoped as a data engineering and pipeline automation exercise rather than an analytics project. The underlying dataset, a personal Spotify playlist, doesn't have the scale or business-question depth to justify a BI or dashboard layer, so the project's scope ends at Load, with a data-quality layer (deduplicated views) added on top of the raw tables.

## Architecture

![Pipeline Architecture](./images/architecture.png)

## Data & Methodology

### Data Source
- Spotify Web API, accessed via `spotipy` using the Authorization Code OAuth flow (Client Credentials flow was deprecated by Spotify in Feb 2026, requiring Premium and user authentication instead)

### Pipeline Architecture

**1. Extract** (`extract_lambda.py`, Lambda #1: `spotify_api_data_extract`)
- Authenticates via a stored refresh token for server-to-server access, with no browser interaction needed after initial bootstrap
- Fetches playlist tracks from the Spotify API
- Writes raw JSON to `s3://etl-pipeline-spotify-vivek/raw_data/to_processed/`
- Triggered daily via EventBridge

**2. Transform** (`transform_lambda.py`, Lambda #2: `spotify_transformation_load_function`)
- Triggered automatically by an S3 event notification when new raw JSON lands
- Parses raw JSON into three normalised datasets: albums, artists, songs
- Deduplicates albums and artists within each batch
- Writes transformed CSVs to `s3://etl-pipeline-spotify-vivek/transformed_data/{albums,artists,songs}/`
- Archives processed raw files from `to_processed/` to `processed/` for idempotency

**3. Load** (Snowpipe, fully automated)
- A Snowflake Storage Integration establishes IAM role-based trust with AWS, with no static credentials stored in Snowflake
- Three Snowpipes (`albums_pipe`, `artists_pipe`, `songs_pipe`) watch their respective S3 prefixes via S3 event notifications routed through SQS
- New transformed files are auto-ingested into `tblAlbum`, `tblArtist`, `tblSongs` within seconds of landing in S3, with no manual trigger required

### Key Decisions

- **Storage Integration over static credentials:** chose IAM role-based trust (STORAGE_AWS_ROLE_ARN plus an external ID handshake) over embedding AWS access keys directly in Snowflake, since it avoids long-lived secrets and scopes access to exactly one S3 path.
- **SQS as the notification layer:** S3 event notifications route through SQS rather than triggering Snowpipe directly, since Snowpipe polls its queue rather than being invoked. SQS provides a durable buffer with at-least-once delivery, decoupling when a file lands from when it gets ingested, and lets multiple pipes share one queue.
- **Deduplication handled via views, not at ingestion:** Snowpipe only supports `COPY INTO`, not `MERGE`, so raw tables accumulate duplicate rows on repeated loads, for example an album reappearing across multiple playlist extracts. Rather than complicating the ingestion layer, deduplication is handled by two views (`vw_album_deduped`, `vw_artist_deduped`) that self-correct on every query with zero manual maintenance.

## Key Findings

**Pipeline verification:** Triggered a live end-to-end test by manually invoking the Extract Lambda. Without any manual intervention, row counts increased automatically as new data flowed through the full chain: `tblAlbum` 20 to 32, `tblArtist` 2 to 3, `tblSongs` 127 to 177, confirming the automated Load layer works as designed.

**Data quality:** Raw ingestion revealed real duplicate accumulation. For example, the artist table contained 3 rows despite only 1 unique artist appearing across the entire playlist. This is expected behaviour given Snowpipe's `COPY INTO`-only ingestion model, and is solved permanently via deduplicated views rather than manual cleanup.

## Project Structure

**Lambda (`lambda/`)**
- [`extract.py`](./lambda/extract.py) - Local development/testing version using interactive OAuth (kept to document the dev process)
- [`extract_lambda.py`](./lambda/extract_lambda.py) - Deployed Lambda #1: refresh-token authentication, playlist fetch, raw JSON upload to S3
- [`refresh_token.py`](./lambda/refresh_token.py) - One-time OAuth bootstrap script to generate the stored refresh token
- [`transform_lambda.py`](./lambda/transform_lambda.py) - Deployed Lambda #2: JSON parsing, album/artist/song extraction, deduplication, S3 upload, raw file archiving

**Snowflake SQL (`snowflake_sql/`)**
- [`setup.sql`](./snowflake_sql/setup.sql) - Database, schema, and table creation
- [`s3_connection.sql`](./snowflake_sql/s3_connection.sql) - Storage Integration and stage setup (S3 to Snowflake IAM trust)
- [`snowpipe.sql`](./snowflake_sql/snowpipe.sql) - Snowpipe creation for automated ingestion
- [`final_view.sql`](./snowflake_sql/final_view.sql) - Deduplicated views for data quality

## Tech Stack

- Python (`spotipy`, `boto3`, `pandas`), for extraction and transformation logic
- SQL, for Snowflake schema design, storage integration, and deduplication logic
- AWS Lambda, serverless compute for Extract and Transform stages
- AWS S3, raw and transformed data staging
- AWS IAM, role-based trust for Snowflake's Storage Integration
- Snowpipe, automated ingestion into Snowflake via S3 event notifications and SQS
- Snowflake, data warehouse, storage integration, deduplicated views

## Skills Demonstrated

- Serverless ETL pipeline design (AWS Lambda, event-driven architecture)
- OAuth 2.0 authentication and API integration
- Cloud storage integration and IAM role-based trust configuration
- Automated data ingestion (Snowpipe, S3 event notifications, SQS)
- Data quality problem identification and resolution (declarative deduplication)
- End-to-end pipeline verification and testing

## Limitations

- Song records are not deduplicated across loads, since a song legitimately reappearing across separate listening sessions isn't a data quality defect in the same way a duplicated album or artist row is.
- Raw tables (`tblAlbum`, `tblArtist`, `tblSongs`) will continue to accumulate duplicate rows indefinitely, since Snowpipe only supports append-only `COPY INTO`. Deduplicated views should be used for any downstream querying rather than the raw tables directly.
- No BI or dashboard layer, by design. The personal-playlist dataset doesn't have sufficient scale or business-question depth to justify one; this project's scope is intentionally the pipeline itself.

## Verification

*(screenshot of before/after row counts confirming automated Snowpipe ingestion, add here)*