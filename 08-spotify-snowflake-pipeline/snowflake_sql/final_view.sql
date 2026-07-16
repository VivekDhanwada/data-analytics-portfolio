CREATE OR REPLACE VIEW spotify_db.raw.vw_album_deduped AS
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY album_id ORDER BY album_id) AS rn
    FROM spotify_db.raw.tblAlbum
) WHERE rn = 1;

CREATE OR REPLACE VIEW spotify_db.raw.vw_artist_deduped AS
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY artist_id ORDER BY artist_id) AS rn
    FROM spotify_db.raw.tblArtist
) WHERE rn = 1;