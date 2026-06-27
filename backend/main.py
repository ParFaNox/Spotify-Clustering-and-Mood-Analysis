from fastapi import FastAPI
import os
from fastapi.responses import RedirectResponse
from auth import get_spotify_client, sp_oauth2
from data import get_recently_played, get_audio_features_freqblog
from mood import train_mood_classifier, classify_moods, load_mood_classifier
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/login')
def login():
    auth_url = sp_oauth2.get_authorize_url()
    return RedirectResponse(auth_url)
@app.get('/callback')
def callback(code: str):
    sp_oauth2.get_access_token(code)
   # return "Auth successful, you can close this tab."
    return RedirectResponse("http://localhost:3000?logged_in=true")
# @app.get('/test-data')
# def test_data():
#     tracks = get_recently_played()
#     features= get_audio_features_freqblog(tracks)
#     return {'track_count':len(tracks), 'features_count': len(features)}
@app.get("/test-data")
def test_data():
    tracks = get_recently_played()
    features = get_audio_features_freqblog(tracks)
    
    model = load_mood_classifier()
    if model is None:
        model = train_mood_classifier(features)
    
    moods = classify_moods(features, model)
    
    return {
        "track_count": len(tracks),
        "features_count": len(features),
        "tracks": tracks,
        "moods": moods
    }
@app.get("/debug-features")
def debug_features():
    tracks = get_recently_played()
    features = get_audio_features_freqblog(tracks)
    
    output = []
    for f in features:
        if f is not None:
            output.append({
                "track_name": f.get("track_name"),
                "valence": f.get("valence"),
                "energy": f.get("energy"),
                "danceability": f.get("danceability"),
                "acousticness": f.get("acousticness"),
                "mood": f.get("mood")  # FreqBlog's own mood guess, for comparison
            })
    
    return output