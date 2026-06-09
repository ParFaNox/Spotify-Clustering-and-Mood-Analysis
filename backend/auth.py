import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
backend_cache_path = os.path.join(backend_dir, ".spotify.cache")
sp_oauth2= SpotifyOAuth(
    client_id = os.getenv("SPOTIFY_CLIENT_ID"),
    
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET"),
    
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI"),
    
    scope= 'user-top-read user-read-recently-played playlist-read-private',
    
    cache_path=backend_cache_path
    )
def get_spotify_client():
    return spotipy.Spotify(auth_manager=sp_oauth2)

