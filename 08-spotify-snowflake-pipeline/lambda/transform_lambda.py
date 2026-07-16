import json
import os
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO

def album(data):
    album_list = []
    for row in data['items']:
        track = row.get('item')
        if track is None or track.get('type') != 'track':
            continue
        album_list.append({
            'album_id': track['album']['id'],
            'name': track['album']['name'],
            'release_date': track['album']['release_date'],
            'total_tracks': track['album']['total_tracks'],
            'url': track['album']['external_urls']['spotify']
        })
    return album_list

def artist(data):
    artist_list = []
    for row in data['items']:
        track = row.get('item')
        if track is None or track.get('type') != 'track':
            continue
        for a in track['artists']:
            artist_list.append({
                'artist_id': a['id'],
                'artist_name': a['name'],
                'external_url': a['href']
            })
    return artist_list

def songs(data):
    song_list = []
    for row in data['items']:
        track = row.get('item')
        if track is None or track.get('type') != 'track':
            continue
        song_list.append({
            'song_id': track.get('id'),
            'song_name': track.get('name'),
            'duration_ms': track.get('duration_ms'),
            'url': track.get('external_urls', {}).get('spotify'),
            'song_added': row.get('added_at'),
            'album_id': track.get('album', {}).get('id'),
            'artist_id': track.get('artists', [{}])[0].get('id')
        })
    return song_list

def upload_df(s3, df, bucket, folder, name, timestamp):
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    s3.put_object(
        Bucket=bucket,
        Key=f"transformed_data/{folder}/{name}_{timestamp}.csv",
        Body=buffer.getvalue()
    )

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = "etl-pipeline-spotify-vivek"
    to_processed_key = "raw_data/to_processed/"
    processed_key = "raw_data/processed/"

    spotify_data = []
    spotify_keys = []

    listing = s3.list_objects(Bucket=Bucket, Prefix=to_processed_key)
    if 'Contents' not in listing:
        return {'statusCode': 200, 'body': 'No new files to process'}

    for file in listing['Contents']:
        file_key = file['Key']
        if file_key.split('.')[-1] == "json":
            response = s3.get_object(Bucket=Bucket, Key=file_key)
            content = response['Body']
            jsonObject = json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_keys.append(file_key)

    album_list, artist_list, song_list = [], [], []
    for data in spotify_data:
        album_list.extend(album(data))
        artist_list.extend(artist(data))
        song_list.extend(songs(data))

    album_df = pd.DataFrame(album_list).drop_duplicates(subset=['album_id'])
    album_df['release_date'] = pd.to_datetime(album_df['release_date'])

    artist_df = pd.DataFrame(artist_list).drop_duplicates(subset=['artist_id'])

    song_df = pd.DataFrame(song_list)
    song_df['song_added'] = pd.to_datetime(song_df['song_added'])

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    upload_df(s3, album_df, Bucket, "albums", "album_transformed", timestamp)
    upload_df(s3, artist_df, Bucket, "artists", "artist_transformed", timestamp)
    upload_df(s3, song_df, Bucket, "songs", "song_transformed", timestamp)

    # Move each processed raw file from to_processed/ to processed/,
    # so it never gets re-processed on the next run
    for file_key in spotify_keys:
        new_key = file_key.replace(to_processed_key, processed_key, 1)
        s3.copy_object(Bucket=Bucket, CopySource={'Bucket': Bucket, 'Key': file_key}, Key=new_key)
        s3.delete_object(Bucket=Bucket, Key=file_key)

    return {
        'statusCode': 200,
        'body': f"Transformed {len(album_df)} albums, {len(artist_df)} artists, {len(song_df)} songs. Moved {len(spotify_keys)} raw files to processed/"
    }