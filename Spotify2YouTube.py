import sys
import json
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QTextEdit, QMessageBox, QInputDialog, QProgressBar
)
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic

def load_credentials(config_path='spotify.json'):
    try:
        with open(config_path, 'r') as f:
            creds = json.load(f)
            return creds['SPOTIFY_CLIENT_ID'], creds['SPOTIFY_CLIENT_SECRET']
    except Exception as e:
        raise Exception(f"Failed to load Spotify credentials: {e}")

class PlaylistViewer(QWidget):
    def __init__(self, spotify_client, ytmusic_client):
        super().__init__()
        self.sp = spotify_client
        self.ytmusic = ytmusic_client
        self.track_list = []

        self.setWindowTitle("Spotify to YouTube Music Exporter")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        # Spotify playlist URL input
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Paste Spotify playlist URL here...")
        self.layout.addWidget(self.input)

        # Button to load Spotify playlist tracks
        self.load_button = QPushButton("Load Playlist", self)
        self.load_button.clicked.connect(self.load_playlist)
        self.layout.addWidget(self.load_button)

        # Button to export loaded tracks to YouTube Music
        self.export_button = QPushButton("Export to YouTube Music", self)
        self.export_button.clicked.connect(self.export_to_ytmusic)
        self.layout.addWidget(self.export_button)

        # Progress bar to show export progress
        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.layout.addWidget(self.progress)

        # Text output for listing tracks
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

    # Extract Spotify playlist ID from the URL
    def extract_playlist_id(self, url):
        match = re.search(r'playlist/([a-zA-Z0-9]+)', url)
        return match.group(1) if match else None

    # Load playlist tracks from the given Spotify URL
    def load_playlist(self):
        url = self.input.text()
        playlist_id = self.extract_playlist_id(url)

        if not playlist_id:
            QMessageBox.warning(self, "Error", "Invalid Spotify playlist URL.")
            return

        try:
            limit = 100
            offset = 0
            tracks = []

            while True:
                results = self.sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
                items = results['items']
                if not items:
                    break
                tracks.extend(items)
                offset += limit

            self.track_list.clear()
            self.output.clear()

            for idx, item in enumerate(tracks, start=1):
                track = item['track']
                name = track['name']
                artists = ', '.join([artist['name'] for artist in track['artists']])
                self.track_list.append({'name': name, 'artist': artists})
                self.output.append(f"{idx}. {name} - {artists}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load playlist:\n{e}")

    # Export loaded tracks to YouTube Music with a progress bar update
    def export_to_ytmusic(self):
        if not self.track_list:
            QMessageBox.warning(self, "Error", "No tracks loaded to export.")
            return

        name, ok = QInputDialog.getText(self, "Playlist Name", "Enter a name for the YouTube Music playlist:")
        if not ok or not name:
            return

        try:
            # Create a new YouTube Music playlist
            playlist_id = self.ytmusic.create_playlist(name, "Created from Spotify playlist")
            total = len(self.track_list)
            added = 0
            self.progress.setMaximum(total)
            self.progress.setValue(0)

            # Loop over each track and try to add it
            for index, track in enumerate(self.track_list, start=1):
                query = f"{track['name']} {track['artist']}"
                search_results = self.ytmusic.search(query, filter="songs")
                if search_results:
                    video_id = search_results[0].get("videoId")
                    if video_id:
                        self.ytmusic.add_playlist_items(playlist_id, [video_id])
                        added += 1
                # Update progress bar as we process each track
                self.progress.setValue(index)

            QMessageBox.information(self, "Success", f"YouTube Music playlist created!\n{added} songs added.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export playlist:\n{e}")
        finally:
            self.progress.setValue(0)  # Optionally reset progress bar after completion

if __name__ == "__main__":
    try:
        # Load Spotify credentials from config.json
        client_id, client_secret = load_credentials()
        sp_auth = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(auth_manager=sp_auth)

        ytmusic = YTMusic("ytmusic.json")

        # Create and run the Qt application
        app = QApplication(sys.argv)
        viewer = PlaylistViewer(sp, ytmusic)
        viewer.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Startup failed: {e}")

