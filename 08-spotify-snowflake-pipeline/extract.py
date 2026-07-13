import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri='https://127.0.0.1:8888/callback',
    scope=''
))

playlist_link = "https://open.spotify.com/playlist/5e6n2yhtZxQYhMQbx8ec42?si=2teuduxKSFu0u-GcFSUXHg&utm_source=copy-link&pi=PAxUVK1NTaOS8"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

data = sp.playlist_items(playlist_URI)

album_list = []
song_list = []
artist_list = []

for row in data['items']:
    track = row.get('item')
    if track is None or track.get('type') != 'track':
        continue

    # --- Album ---
    album_element = {
        'album_id': track['album']['id'],
        'name': track['album']['name'],
        'release_date': track['album']['release_date'],
        'total_tracks': track['album']['total_tracks'],
        'url': track['album']['external_urls']['spotify']
    }
    album_list.append(album_element)

    # --- Song (popularity removed — not present in current API response) ---
    song_element = {
        'song_id': track.get('id'),
        'song_name': track.get('name'),
        'duration_ms': track.get('duration_ms'),
        'url': track.get('external_urls', {}).get('spotify'),
        'song_added': row.get('added_at'),
        'album_id': track.get('album', {}).get('id'),
        'artist_id': track.get('artists', [{}])[0].get('id')
    }
    song_list.append(song_element)

    # --- Artists (can be multiple per track) ---
    for artist in track['artists']:
        artist_dict = {
            'artist_id': artist['id'],
            'artist_name': artist['name'],
            'external_url': artist['href']
        }
        artist_list.append(artist_dict)

# Build DataFrames
album_df = pd.DataFrame(album_list)
song_df = pd.DataFrame(song_list)
artist_df = pd.DataFrame(artist_list)

# Type conversions
album_df['release_date'] = pd.to_datetime(album_df['release_date'])
song_df['song_added'] = pd.to_datetime(song_df['song_added'])

# Dedup
artist_df = artist_df.drop_duplicates(subset='artist_id').reset_index(drop=True)
album_df = album_df.drop_duplicates(subset='album_id').reset_index(drop=True)

# Validation
print("--- Album Info ---")
print(album_df.info())
print("\n--- Song Info ---")
print(song_df.info())
print("\n--- Artist Info ---")
print(artist_df.info())

# Export to CSV
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

album_df.to_csv(f"{output_dir}/albums.csv", index=False)
song_df.to_csv(f"{output_dir}/songs.csv", index=False)
artist_df.to_csv(f"{output_dir}/artists.csv", index=False)

print(f"\nExported 3 CSV files to ./{output_dir}/")