import spotipy
import requests
import json
from libs.Track import Track
import spotipy.util as util
from configparser import ConfigParser
from libs.Artist import Artist
from libs.Playlist import Playlist

class Spotify(object):

	def __init__(self):
		self.spotify = None
		self.config = ConfigParser()
		self._parse_account_details()
		self.login()

	def login(self):
		token = util.prompt_for_user_token(self.USERNAME, self.SCOPE, client_id=self.CLIENT_ID, client_secret=self.SECRET_ID, redirect_uri=self.REDIRECT_URI)
		self.token = token
		if token:
			self.spotify = spotipy.Spotify(auth=token)
		else:
			print('error retrieving token')

	def _parse_account_details(self, filename='data/config.ini'):
		self.config.read(filename)
		cache_name = self.config.sections()[0]
		self.USERNAME = self.config[cache_name]['username']
		self.CLIENT_ID = self.config[cache_name]['client_id']
		self.REDIRECT_URI = self.config[cache_name]['redirect_uri']
		self.SCOPE = self.config[cache_name]['scope']
		self.SECRET_ID = self.config[cache_name]['secret_id']
	
	def get_playlist_id(self, url):
		return url.split('https://open.spotify.com/playlist/')[1]

	def check_playlist_url(self, url):
		return 'spotify' in url and 'playlist' in url

	def get_playlist_name_from_url(self, url):
		return self.spotify.playlist(url)['name']

	def get_playlist_cover(self, url):
		return self.spotify.playlist(url)["images"][0]["url"]

	def get_playlist_private(self, url):
		return self.spotify.playlist(url)["public"]

	def get_playlist_object(self, playlist_url):
		name = self.get_playlist_name_from_url(playlist_url)
		cover = self.get_playlist_cover(playlist_url)
		private = self.get_playlist_private(playlist_url)
		playlist_obj = Playlist(name, cover, private)
		return playlist_obj

	def _create_playlist(self, playlist_name):
		user_id = self.spotify.me()['id']
		playlist_infos = self.spotify.user_playlist_create(user_id, playlist_name, True)
		return playlist_infos['id']

	# Id della playlist che si trova su spotify
	def upload_tracks(self, tracks_list, playlist_name):
		tracks_uris = []
		uri = 'https://api.spotify.com/v1/playlists/{}/tracks'

		playlist_id = self._create_playlist(playlist_name)

		for traccia in tracks_list:
			query = '{} {}'.format(traccia.get_track_name(), traccia.get_artist())
			result = self.spotify.search(query)
			tracks_uris.append(result['tracks']['items'][0]['uri'])

		headers = {"Authorization": f"Bearer {self.token}"}
		body = {
			"uris": tracks_uris,
		}
		response = requests.post(uri.format(playlist_id), headers=headers, data=json.dumps(body)).json()
		return response

	def get_user_infos(self):
		return self.spotify.me()

	def parse_playlist_from_url(self, url):
		tracks_spotify = []
		pl = self.spotify.playlist(url)
		
		cover_image = pl['images'][0]['url']
		playlist_name = pl['name']
		tracks = pl['tracks']['items']

		for track in tracks:

			# Track Infos
			try:
				track_name = track['track']['name']
				duration = track['track']['duration_ms'] 
				track_cover = track['track']['album']['images'][0]['url']

			# Artist infos
				artist_id = track['track']['album']['artists'][0]['id']
				artist_infos_json = self.spotify.artist(artist_id)
				artist_followers = artist_infos_json['followers']['total']
				artist_image = artist_infos_json['images'][0]['url']
				artist_name = artist_infos_json['name']
			except Exception as e:
				# Gestire meglio eccezioni
				pass

			artist_object = Artist(artist_name, artist_followers, artist_image)

			minute_duration = float(f"{(duration/60000):.2f}")
			tracks_spotify.append(Track(artist_object, track_name, track_cover, minute_duration))


		return tracks_spotify