# Spotify2YouTubeMusic
This is a tool where you can paste a Spotify Playlist link and create a new playlist on YouTube Music

# Setup

## Requirements
```bash
pip install PyQt5 spotipy ytmusicapi
```
## Spotify JSON
1. Navigate to https://developer.spotify.com/dashboard
2. Create a new app
3. Enable the following uses:
    * Web API
    * Web Playback SDK
4. Create the file `spotify.json` from `spotify.json.example` and place the values `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` 

## YouTube Music JSON
1. Open YouTube Music in Your Browser:
    * Navigate to https://music.youtube.com and ensure you're logged into your account.
2. Access Developer Tools:
    * Press F12 or right-click anywhere on the page and select "Inspect" to open the Developer Tools.
3. Navigate to the Network Tab:
    * In the Developer Tools, click on the "Network" tab.
4. Filter for Specific Requests:
    * In the filter bar, type browse to narrow down the network requests.
5. Trigger a Network Request:
    * Click on the "Library" button or scroll through your library to generate network activity.
6. Select the Appropriate Request:
    * Look for a request named browse with the method POST.
7. Extract Headers:
```
    Extract the following headers and their values:
        Authorization
        X-Goog-AuthUser
        X-Goog-Visitor-Id
        User-Agent
        Accept
        Accept-Language
        Content-Type
        Cookie
        x-origin (should be https://music.youtube.com)
```
8. Create `ytmusic.json` from `ytmusci.json.example` and the values you extracted:

# Use
Open the UI
```bash
python Spotify2YouTube.py
```
Paste the Spotify Playlist url, load the songs and create the new playlist