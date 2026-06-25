from data import get_audio_features_freqblog
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from training_data import training_data
import pandas as pd
import main
import joblib, os

def find_feature_by_id(track_name, all_features):
    for feature in all_features:
        if feature is not None and feature.get('track_name') == track_name:
            return feature
    return None
def extract_audio_features(feature):
    return {
        'valence': feature.get('valence', 0),
        'energy': feature.get('energy', 0),
        'danceability': feature.get('danceability', 0),
        'acousticness': feature.get('acousticness', 0),
        'instrumentalness': feature.get('instrumentalness', 0),
        'tempo': feature.get('tempo', 0),
        'loudness': feature.get('loudness', 0)
    }
def train_mood_classifier(all_features):
    all_features = [f for f in all_features if f is not None]
    x = []
    y = []
    for track in training_data:
        track_name = track['track_name']  # change this
        emotion = track['emotion']
        feature = find_feature_by_id(track_name, all_features)  # pass track_name
        if feature:
            x.append(extract_audio_features(feature))
            y.append(emotion)
    # ... rest stays same
    print(f"Matched {len(x)} training samples")
    print(f"X list length: {len(x)}, Y list length: {len(y)}")
    all_features = [f for f in all_features if f is not None]
    #print(f"Non-None features IDs: {[f['id'] for f in all_features]}")
    X_dataframe = pd.DataFrame(x)
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_dataframe, y)
    joblib.dump(model, 'mood_model.pkl')
    
    return model
    #model.predict(X_dataframe)
def load_mood_classifier():
    if os.path.exists('mood_model.pkl'):
        return joblib.load('mood_model.pkl')
    else:
        return None
def classify_moods(features, model):
    x=[extract_audio_features(f) for f in features]
    X_dataframe=pd.DataFrame(x)
    return model.predict(X_dataframe)
        