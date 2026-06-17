from fastapi import FastAPI
import os
from fastapi.responses import RedirectResponse
from auth import get_spotify_client, sp_oauth2
from data import get_recently_played, get_audio_features_freqblog
from mood import train_mood_classifier, classify_moods
app=FastAPI()
@app.get('/login')
def login():
    auth_url = sp_oauth2.get_authorize_url()
    return RedirectResponse(auth_url)
@app.get('/callback')
def callback(code:str):
    sp_oauth2.get_access_token(code)
    return "Auth successful, you can close this tab."
# @app.get('/test-data')
# def test_data():
#     tracks = get_recently_played()
#     features= get_audio_features_freqblog(tracks)
#     return {'track_count':len(tracks), 'features_count': len(features)}
@app.get('/test-data')
def test_data():
    print("Starting test-data...")
    tracks = get_recently_played()
    print(f"Got {len(tracks)} tracks")
    features = get_audio_features_freqblog(tracks)
 #   print(features[0])
    print(f"Got {len(features)} features")
    model= train_mood_classifier(features)
    moods= classify_moods(features, model)
    return {'track_count': len(tracks), 'features_count': len(features), 'moods': moods.tolist()}