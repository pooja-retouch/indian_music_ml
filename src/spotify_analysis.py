import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt

# --- Spotify Authentication ---
CLIENT_ID = "d907d7da04e14ca4886a05e7101557cd"
CLIENT_SECRET = "92f010e221c942ce8383060c29c03cfe"

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# --- A.R. Rahman artist URI ---
artist_uri = "spotify:artist:1mYsTxnqsietFxj1OgoGbG"

# Fetch Top 10 Tracks (India region)
results = sp.artist_top_tracks(artist_uri, country="IN")
top_tracks = results['tracks'][:10]

# Build dataset
songs = [
    {
        "name": t['name'],
        "album": t['album']['name'],
        "release_date": t['album']['release_date'],
        "popularity": t['popularity'],
        "url": t['external_urls']['spotify']
    }
    for t in top_tracks
]

df = pd.DataFrame(songs)
df.to_csv("ar_rahman_top10.csv", index=False, encoding="utf-8")

print("✅ Saved ar_rahman_top10.csv with", len(df), "tracks")

# --- Most Popular Track ---
most_popular = df.loc[df['popularity'].idxmax()]
print(f"🎵 Most Popular Track: {most_popular['name']} (Popularity {most_popular['popularity']})")

# --- Popularity Chart ---
df_sorted = df.sort_values(by="popularity", ascending=True)
plt.figure(figsize=(10,6))
plt.barh(df_sorted["name"], df_sorted["popularity"], color="skyblue")
plt.xlabel("Popularity")
plt.title("A.R. Rahman - Top 10 Tracks Popularity")
plt.tight_layout()
plt.show()
