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

CREATE OR REPLACE VIEW spotify_db.raw.vw_songs_deduped AS
SELECT
    s.song_id,
    s.song_name,
    s.duration_ms,
    s.url,
    s.song_added,
    s.album_id,
    a.name AS album_name,
    s.artist_id
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY song_id, album_id ORDER BY song_id) AS rn
    FROM spotify_db.raw.tblSongs
) s
LEFT JOIN spotify_db.raw.vw_album_deduped a
    ON s.album_id = a.album_id
WHERE s.rn = 1;