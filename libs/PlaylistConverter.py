import os
import sys
import configparser
from libs.Deez import Deez
from libs.Spotify import Spotify

class PlaylistConverter(object):
	def __init__(self):
		self.deezer = Deez()
		self.spotify = Spotify()
		self.config = configparser.ConfigParser()

	def _check_config_file(self, filename='data/config.ini'):
		if os.path.isfile(filename):
			return True
		else:
			return False
		return False

	def _check_parameters(self, filename='data/config.ini'):
		check = True
		self.config.read(filename)
		secs = self.config.sections()
		for s in secs:
			for key in self.config[s]:
				value = self.config[s][key]
				if value == "''":
					check = False
		return check

	# se il cache_file esiste significa che non devo effettuare nuovamente il login con spotify
	def check_cache_file(self, filename='data/config.ini'):
		self.config.read(filename)
		cache_name = config.sections()[0]
		username = str(self.config[cache_name]['username']).strip("'")
		if os.path.isfile('.cache-{}'.format(username)):
			return True
		else:
			return False
		return False

	def get_deezer_urls_from_list(self, list_tracks):
		tracks_url = []
		
		for track in list_tracks:
			try:
				track_name = '{} - {}'.format(track.get_track_name(), track.get_artist())
				track_deezer_url = self.deezer.get_track_url_from_title(track_name)
				tracks_url.append(track_deezer_url)
			except:
				pass #Track not found on Deezer platform

		return tracks_url

	def get_deezer_tracks_ids_from_list(self, deezer_tracks_list):
		tracks_ids = []

		for track in deezer_tracks_list:
			track_id = track.split('https://www.deezer.com/track/')[1]
			tracks_ids.append(track_id)

		return tracks_ids

	def convert(self, spotify_url):
		if self._check_config_file() and self._check_parameters():
			# verifico che l'url della playlist sia valido 
			try:
				if self.spotify.check_playlist_url(spotify_url):			
					playlist_id = self.spotify.get_playlist_id(spotify_url)
					sys.stdout.write('* Loading tracks from spotifys playlist\r')
					sys.stdout.flush()
					# salvo gli oggetti Tracks all'interno di una lista che rappresenta la playlist
					listtracks = self.spotify.parse_playlist_from_url(playlist_id)
					sys.stdout.write('* Tracks succesfully loaded from spotify playlist\r')
					sys.stdout.flush()

					spotify_playlist_name = self.spotify.get_playlist_name_from_url(spotify_url)
					sys.stdout.write('* Creating playlist on deezer\r')
					sys.stdout.flush()

					try:
						playlist_id = str(self.deezer.create_playlist(spotify_playlist_name)['id'])
						sys.stdout.write('[+] Playlist created with name %s !\r' %spotify_playlist_name)
						sys.stdout.flush()
						spotify_playlist_tracks = self.spotify.parse_playlist_from_url(spotify_url)
						deezer_tracks_urls = self.get_deezer_urls_from_list(spotify_playlist_tracks)
						deezer_tracks_ids = self.get_deezer_tracks_ids_from_list(deezer_tracks_urls)
						self.deezer.add_tracks_to_playlist(deezer_tracks_ids, playlist_id)
					except Exception as e:
						print("an error occurred: ", e)
				else:
					print('[-] The provided url is not valid!')
			except Exception as e:
				print('[-] Error while retrieving playlists tracks: ', e)
		else:
			print('config file does not exists or is not configured in the right way')