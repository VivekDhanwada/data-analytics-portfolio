import json
import os
import requests
import base64
import spotipy
import boto3
from datetime import datetime

def get_access_token():
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN')

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers={'Authorization': f'Basic {auth_header}'},
        data={'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    )
    return response.json()['access_token']

def lambda_handler(event, context):
    access_token = get_access_token()
    sp = spotipy.Spotify(auth=access_token)

    playlist_link = "https://open.spotify.com/playlist/5e6n2yhtZxQYhMQbx8ec42"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    data = sp.playlist_items(playlist_URI)

    s3_client = boto3.client('s3')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    s3_client.put_object(
    Bucket="etl-pipeline-spotify-vivek",
    Key=f"raw_data/to_processed/spotify_data_{timestamp}.json",
    Body=json.dumps(data)
    )

    return {
        'statusCode': 200,
        'body': f"Fetched and uploaded {len(data['items'])} items to S3"
    }