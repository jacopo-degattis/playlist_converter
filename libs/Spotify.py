import spotipy
from libs.Track import Track
import spotipy.util as util
from configparser import ConfigParser

class Spotify(object):

	def __init__(self):
		self.spotify = None
		self.config = ConfigParser()
		'''self.CLIENT_ID = ''
		self.REDIRECT_URI = ''
		self.USERNAME = ''
		self.SCOPE = ''
		self.SECRET_ID ='''
		self._parse_account_details()
		self.login()

	def login(self):
		token = util.prompt_for_user_token(self.USERNAME, self.SCOPE, client_id=self.CLIENT_ID, client_secret=self.SECRET_ID, redirect_uri=self.REDIRECT_URI)
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

	def parse_playlist_from_url(self, url):
		tracks_spotify = []
		pl = self.spotify.playlist(url)
		
		cover_image = pl['images'][0]['url']
		playlist_name = pl['name']
		tracks = pl['tracks']['items']

		for track in tracks:
			try:
				artist_name = track['track']['album']['artists'][0]['name']
				track_name = track['track']['album']['name']
				tracks_spotify.append(Track(artist_name, track_name))
			except Exception as e:
				print('Weird track, something is missing!')


		return tracks_spotify