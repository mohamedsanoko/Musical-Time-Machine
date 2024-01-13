import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

CLIENT_ID = os.environ.get("PLAYLIST_CLIENT_ID", "Key does not exist.")
CLIENT_SECRET = os.environ.get("PLAYLIST_CLIENT_SECRET", "Key does not exist.")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "Key does not exist.")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
url = "https://www.billboard.com/charts/hot-100/"
date_url = f"{url}{date}/"
response = requests.get(date_url)
data = response.text
soup = BeautifulSoup(data, 'html.parser')
title_tags = soup.select(selector="li #title-of-a-story")
song_titles = []
for title_tag in title_tags:
    song_titles.append(title_tag.text.strip())

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private"))

user_infos = sp.current_user()
user_id = user_infos['id']
date_info = date.split("-")
year = date_info[0]
results = []
uri_song_lists = []
for song in song_titles:
    query = f"track:{song} year:{year}"
    result = sp.search(q=query, limit=1, offset=0, type="track")
    try:
        uri_song = result["tracks"]["items"][0]["uri"]
        uri_song_lists.append(uri_song)
    except KeyError:
        print("Song was not found on Spotify")
        continue
name_new_playlist = f"{date} Billboard 100"

playlist_id = sp.user_playlist_create(user=user_id, name=name_new_playlist, public=False, collaborative=True, description="")['id']
sp.playlist_add_items(playlist_id, uri_song_lists)
