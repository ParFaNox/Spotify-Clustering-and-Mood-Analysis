from auth import get_spotify_client
import requests
import os
from dotenv import load_dotenv
load_dotenv()
def get_recently_played():
    sp = get_spotify_client()
    tracks=[]
    response= sp.current_user_recently_played(limit=50)
    while True:
        for item in response['items']:
            tracks.append({
                'id': item['track']['id'],
                'name': item['track']['name'],
                'artist' : item['track']['artists'][0]['name'],
                'played_at': item['played_at']
                })
        if response['cursors'] and response['cursors']['before']:
            response = sp.current_user_recently_played(
                limit =50,
                before=response['cursors']['before']
            )
        else:
            break
    print(tracks)
    return tracks
# def get_audio_features_freqblog(tracks):
#     # sp = get_spotify_client()
#     # ids=[t['id'] for t in tracks]
#     # features = []
#     # for i in range(0, len(ids), 100):
#     #     batch = sp.audio_features(ids[i:i+100])
#     #     features.extend(batch)
#     # return features
#     api_key = os.getenv("FREQBLOG_API_KEY")
#     payload = [
#         {"track": t['name'], 'artist': t['artist']}
#         for t in tracks
#     ]
#     results=[]
#     for i in range(0, len(payload),50):
#         batch = payload[i:i+50]
#         response = requests.post(
#             'https://api.freqblog.com/bulk',
#             json=batch,
#             headers={"X-Api-Key": api_key}
#         )
#         print(response.json)
#         results.extend(response.json()['audio_features'])
#     return results
#def get_audio_features_freqblog(tracks):
    # api_key = os.getenv("FREQBLOG_API_KEY")
    # headers = {"X-Api-Key": api_key}
    # results = []
    
    # for track in tracks:
    #     response = requests.get(
    #         "https://api.freqblog.com/lookup",
    #         params={"track": track["name"], "artist": track["artist"]},
    #         headers=headers
    #     )
    #     if response.status_code == 200:
    #         results.append(response.json())
    
    # return results
    

#tracks is a list of dicts. Each dict has keys: id, name, artist, played_at.
#So when you extract IDs, you'd do:
#ids = [t['id'] for t in tracks]


def get_audio_features_freqblog(tracks):
    api_key = os.getenv("FREQBLOG_API_KEY")
    results = []
    
    for track in tracks:
        response = requests.get(
            f"https://api.freqblog.com/lookup",
            params={"track": track["name"], "artist": track["artist"]},
            headers={"X-Api-Key": api_key}
        )
        print(f"Status for {track['name']}: {response.status_code}")
        if response.status_code == 200:
            results.append(response.json())
    
    print(f"Total results: {len(results)}")
    return results