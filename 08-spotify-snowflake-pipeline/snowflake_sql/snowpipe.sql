CREATE OR REPLACE PIPE spotify_db.raw.albums_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO spotify_db.raw.tblAlbum
  FROM @spotify_db.raw.spotify_s3_stage/albums/
  ON_ERROR = 'CONTINUE';

CREATE OR REPLACE PIPE spotify_db.raw.artists_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO spotify_db.raw.tblArtist
  FROM @spotify_db.raw.spotify_s3_stage/artists/
  ON_ERROR = 'CONTINUE';

CREATE OR REPLACE PIPE spotify_db.raw.songs_pipe
  AUTO_INGEST = TRUE
  AS
  COPY INTO spotify_db.raw.tblSongs
  FROM @spotify_db.raw.spotify_s3_stage/songs/
  ON_ERROR = 'CONTINUE';

SHOW PIPES IN SCHEMA spotify_db.raw;