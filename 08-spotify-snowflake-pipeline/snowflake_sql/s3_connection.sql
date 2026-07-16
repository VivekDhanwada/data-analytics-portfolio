-- ============================================
-- Storage Integration Setup (Step 2a: Snowflake ↔ AWS Trust)
-- ============================================

CREATE OR REPLACE STORAGE INTEGRATION spotify_s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::794661976426:role/snowflake_spotify_access_role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://etl-pipeline-spotify-vivek/transformed_data/');

DESC STORAGE INTEGRATION spotify_s3_integration;

-- ============================================
-- File Format + Stage Setup (Step 2b: S3 Path Connection)
-- ============================================

CREATE OR REPLACE FILE FORMAT spotify_db.raw.csv_ff
  TYPE = 'CSV'
  SKIP_HEADER = 1;

CREATE OR REPLACE STAGE spotify_db.raw.spotify_s3_stage
  URL = 's3://etl-pipeline-spotify-vivek/transformed_data/'
  STORAGE_INTEGRATION = spotify_s3_integration
  FILE_FORMAT = spotify_db.raw.csv_ff;

LIST @spotify_db.raw.spotify_s3_stage;

-- ============================================
-- Test load (Step 3: Verify COPY INTO works)
-- ============================================

COPY INTO spotify_db.raw.tblAlbum
FROM @spotify_db.raw.spotify_s3_stage/albums/
ON_ERROR = 'CONTINUE';

COPY INTO spotify_db.raw.tblArtist
FROM @spotify_db.raw.spotify_s3_stage/artists/
ON_ERROR = 'CONTINUE';

COPY INTO spotify_db.raw.tblSongs
FROM @spotify_db.raw.spotify_s3_stage/songs/
ON_ERROR = 'CONTINUE';