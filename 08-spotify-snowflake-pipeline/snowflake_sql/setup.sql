USE ROLE accountadmin;
USE WAREHOUSE compute_wh;

CREATE DATABASE IF NOT EXISTS spotify_db;
CREATE SCHEMA IF NOT EXISTS spotify_db.raw;

CREATE OR REPLACE TABLE spotify_db.raw.tblAlbum (
    album_id VARCHAR,
    name VARCHAR,
    release_date DATE,
    total_tracks NUMBER,
    url VARCHAR
);

CREATE OR REPLACE TABLE spotify_db.raw.tblArtist (
    artist_id VARCHAR,
    artist_name VARCHAR,
    external_url VARCHAR
);

CREATE OR REPLACE TABLE spotify_db.raw.tblSongs (
    song_id VARCHAR,
    song_name VARCHAR,
    duration_ms NUMBER,
    url VARCHAR,
    song_added TIMESTAMP_NTZ,
    album_id VARCHAR,
    artist_id VARCHAR
);