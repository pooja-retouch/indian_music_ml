import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# --- Spotify Authentication ---
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- Indian playlists to analyze ---
indian_playlists = {
    "Top Hits India": "37i9dQZF1DX0XUfTFmNBRM",
    "Bollywood Butter": "37i9dQZF1DX1wFVBjmQoez",
    "Indie India": "37i9dQZF1DWXVJK4aT7pmk",
    "Punjabi 101": "37i9dQZF1DX0XUsuxWHRQd",
    "Tollywood Pearls": "37i9dQZF1DX2WkIBRaChxW"
}

all_tracks = []

# --- Loop through each playlist ---
for playlist_name, playlist_id in indian_playlists.items():
    print(f"Fetching: {playlist_name}")
    results = sp.playlist_tracks(playlist_id, market="IN")
    track_ids = []
    tracks_data = []

    for item in results['items']:
        track = item['track']
        if track:
            tracks_data.append({
                "playlist": playlist_name,
                "track_name": track['name'],
                "artist": ", ".join([a['name'] for a in track['artists']]),
                "album": track['album']['name'],
                "release_date": track['album']['release_date'],
                "popularity": track['popularity']
            })
            track_ids.append(track['id'])

    # Get audio features if available
    try:
        features = sp.audio_features(track_ids)
        for i, feat in enumerate(features):
            if feat:
                tracks_data[i].update({
                    "danceability": feat['danceability'],
                    "energy": feat['energy'],
                    "tempo": feat['tempo'],
                    "valence": feat['valence'],
                    "acousticness": feat['acousticness'],
                    "instrumentalness": feat['instrumentalness']
                })
    except Exception as e:
        print("⚠️ Could not fetch audio features:", e)

    all_tracks.extend(tracks_data)

# --- Save to DataFrame ---
df = pd.DataFrame(all_tracks)
df.to_csv("indian_music_dataset.csv", index=False)

print("✅ Saved indian_music_dataset.csv with", len(df), "tracks")
