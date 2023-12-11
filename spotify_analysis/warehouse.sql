-- Create View of gold layer
CREATE OR REPLACE VIEW home.artist AS
SELECT * FROM HDFS.gold_layer."gold_artists.parquet";

CREATE OR REPLACE VIEW home.album AS
SELECT * FROM HDFS.gold_layer."gold_albums.parquet";

CREATE OR REPLACE VIEW home.track AS
SELECT * FROM HDFS.gold_layer."gold_tracks.parquet";

CREATE OR REPLACE VIEW home.genre AS
SELECT * FROM HDFS.gold_layer."gold_genres.parquet";

CREATE OR REPLACE VIEW home.track_feat AS
SELECT * FROM HDFS.gold_layer."gold_tracks_features.parquet";

------- Spotify Analysis --------
-- V_1_1
CREATE OR REPLACE VIEW home.V_1_1 AS
SELECT count(*) as TotalArtists
FROM HDFS.gold_layer."gold_artists.parquet";

-- V_1_2
CREATE OR REPLACE VIEW home.V_1_2 AS
SELECT name AS ArtistName,
        popularity
FROM HDFS.gold_layer."gold_artists.parquet"
ORDER BY popularity;

-- V_1_3
CREATE OR REPLACE VIEW home.V_1_3 AS
SELECT name AS ArtistName,
        followers
FROM HDFS.gold_layer."gold_artists.parquet" 
ORDER BY followers;

-- V_1_4
CREATE OR REPLACE VIEW home.V_1_4 AS
SELECT name as ArtistName,
        popularity AS Popularity,
        followers AS Followers
FROM HDFS.gold_layer."gold_artists.parquet";

-- V_1_5
CREATE OR REPLACE VIEW home.V_1_5 AS
SELECT ar.name                  as ArtistName
        , ar.artist_id          as ArtistID
        , ar.followers          as ArtistFollowers
        , ar.popularity         as ArtistPopularity
        , ab.album_id           as AlbumID
        , ab.name               as AlbumName
        , ab.popularity         as AlbumPopularity
        , ab.release_date       as AlbumReleaseDate
        , ab.total_tracks       as AlbumTotalTrack
        , ab.album_type         as AlbumType
FROM HDFS.gold_layer."gold_artists.parquet" ar
LEFT JOIN HDFS.gold_layer."gold_albums.parquet" ab on ar.artist_id = ab.artist_id;

-- V_1_6
CREATE OR REPLACE VIEW home.V_1_6 AS
SELECT ar.name                as ArtistName
        , ar.followers          as ArtistFollowers
        , ar.popularity         as ArtistPopularity
        , ge.genre              as ArtistGener
FROM HDFS.gold_layer."gold_artists.parquet" ar
JOIN HDFS.gold_layer."gold_genres.parquet" ge on ar.artist_id = ge.artist_id;  

-- V_3_1
CREATE OR REPLACE VIEW home.V_3_1 AS
SELECT tt.track_id as TrackID
        , tt.artist_id        AS ArtistID
        , tt.album_id           AS AlbumID
        , tt.name             AS TrackName
        , tt.popularity         AS TrackPopularity
        , tt.track_number       AS TrackNumber
        , tf.danceability       AS TrackDanceability
        , tf.energy             AS TrackEnergy
        , tf.loudness           AS TrackLoudness
        , tf.mode               AS TrackMode
        , tf.speechiness        AS TrackSpeechiness
        , tf.acousticness       AS TrackAcousticness
        , tf.instrumentalness   AS TrackInstrumentalness
        , tf.liveness           AS TrackLiveness
        , tf.valence            AS TrackValence
        , tf.tempo              AS TrackTempo
        , tf.duration_ms        AS TrackDuration
        , tf.time_signature     AS TrackTime
FROM HDFS.gold_layer."gold_tracks.parquet" tt
LEFT JOIN HDFS.gold_layer."gold_tracks_features.parquet" tf ON tt.track_id = tf.track_id;

-- V_1_7
CREATE OR REPLACE VIEW home.V_1_7 AS
SELECT ar.name     AS ArtistName
        , ar.followers  AS ArtistFollowers
        , ar.popularity AS ArtistPopularity
        , tt.*
FROM HDFS.gold_layer."gold_artists.parquet" ar
LEFT JOIN home.V_3_1 tt on ar.artist_id = tt.ArtistID;

-- V_2_1
CREATE OR REPLACE VIEW home.V_2_1 AS
SELECT  al.AlbumName
        , al.AlbumPopularity
        , al.AlbumReleaseDate
        , al.AlbumTotalTrack
        , al.AlbumType
        , al.ArtistName
        , al.ArtistID
        , al.ArtistFollowers
        , al.ArtistPopularity
        , tt.*
FROM home.V_1_5 al
LEFT JOIN home.V_3_1 tt on al.AlbumID = tt.AlbumID;

----------- Searching View --------------

CREATE OR REPLACE VIEW home.searchs AS
            SELECT track.track_id AS track_id, track.name AS track_name, track.external_urls AS track_url, track.popularity as track_popularity, track.preview_url as track_preview, artist.name AS artist_name, artist.popularity AS artist_popularity, artist.image_url AS artist_image, SUBSTRING(album.release_date, 1, 4) AS track_release_year, album.name AS album_name, track_features.danceability, track_features.energy, track_features.key, track_features.loudness, track_features.mode, track_features.speechiness, track_features.acousticness, track_features.instrumentalness, track_features.liveness, track_features.valence, track_features.tempo, track_features.duration_ms, track_features.time_signature, LISTAGG(artist_genres.genre, ', ') AS genres
            FROM home.track AS track
            JOIN home.album AS album
            ON track.album_id = album.album_id
            JOIN home.artist AS artist
            ON track.artist_id = artist.artist_id
            JOIN home.track_feat AS track_features
            ON track.track_id = track_features.track_id
            JOIN home.genre as artist_genres
            ON artist.artist_id = artist_genres.artist_id
            GROUP BY track_id, track_name, track_url, track_popularity, track_preview, artist_name, artist_popularity, artist_image, track_release_year, album_name, track_features.danceability, track_features.energy, track_features.key, track_features.loudness, track_features.mode, track_features.speechiness, track_features.acousticness, track_features.instrumentalness, track_features.liveness, track_features.valence, track_features.tempo, track_features.duration_ms, track_features.time_signature
            ORDER BY track_popularity
