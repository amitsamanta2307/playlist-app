import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

CLIENT_ID = ''
CLIENT_SECRET = ''

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.find_all(name="span", class_="chart-element__information__song")
song_names = [item.getText() for item in song_names_spans]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# Creating a new private playlist in Spotify
playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
print(playlist["id"])
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
