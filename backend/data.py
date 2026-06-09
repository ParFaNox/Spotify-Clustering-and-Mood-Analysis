from auth import get_spotify_client
import requests
import os
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
    return tracks
def get_audio_features_freqblog(tracks):
    # sp = get_spotify_client()
    # ids=[t['id'] for t in tracks]
    # features = []
    # for i in range(0, len(ids), 100):
    #     batch = sp.audio_features(ids[i:i+100])
    #     features.extend(batch)
    # return features
    api_key = os.getenv("FREQBLOD_API_KEY")
    payload = [
        {"track": t['name'], 'artist': t['artist']}
        for t in tracks
    ]
    results=[]
    for i in range(0, len(payload),50):
        batch = payload[i:i+50]
        response = requests.post(
            'https://api.freqblog.com/bulk',
            json=batch,
            headers={"X-Api-Key": api_key}
        )
        results.extend(response.json()['results'])
    return results