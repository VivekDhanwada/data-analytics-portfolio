CREATE OR REPLACE FILE FORMAT spotify_db.raw.csv_format
  TYPE = 'CSV'
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  SKIP_HEADER = 1
  PARSE_HEADER = FALSE;

CREATE OR REPLACE PIPE spotify_db.raw.albums_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO spotify_db.raw.tblAlbum
  FROM @spotify_db.raw.spotify_s3_stage/albums/
  FILE_FORMAT = (FORMAT_NAME = 'spotify_db.raw.csv_format')
  ON_ERROR = 'CONTINUE';

CREATE OR REPLACE PIPE spotify_db.raw.artists_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO spotify_db.raw.tblArtist
  FROM @spotify_db.raw.spotify_s3_stage/artists/
  FILE_FORMAT = (FORMAT_NAME = 'spotify_db.raw.csv_format')
  ON_ERROR = 'CONTINUE';

CREATE OR REPLACE PIPE spotify_db.raw.songs_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO spotify_db.raw.tblSongs
  FROM @spotify_db.raw.spotify_s3_stage/songs/
  FILE_FORMAT = (FORMAT_NAME = 'spotify_db.raw.csv_format')
  ON_ERROR = 'CONTINUE';