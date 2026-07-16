import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

auth_manager = SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri='https://127.0.0.1:8888/callback',
    scope=''
)

token_info = auth_manager.get_access_token(as_dict=True)
print(token_info)