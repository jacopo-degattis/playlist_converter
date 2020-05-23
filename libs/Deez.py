import os
import sys
import time
import requests
import deezer
import webbrowser
from configparser import ConfigParser
from progress.bar import IncrementalBar

# Scrivere documentazione per includere anche la materia di informatica

class Deez(object):

	def __init__(self):
		self.token = None
		self.client = deezer.Client()
		self.config = ConfigParser()
		self.api_url = 'https://api.deezer.com/{}'
		self.token_url = 'https://connect.deezer.com/oauth/access_token.php?app_id={id}&secret={secret}&code={code}&output=json'
		self.base_url = 'https://connect.deezer.com/oauth/auth.php?app_id={}&redirect_uri={}&perms={}'
		if self._get_deezer_specified_param('TOKEN', 1) != '':
			self._parse_user_data()
		else:
			self._parse_user_data()
			self.authenticate()
			self._write_token()

	def _write_token(self):
		section = self.config.sections()[1]
		self.config[section]['TOKEN'] = self.token['access_token']
		with open('data/config.ini', 'w+') as configfile:
			self.config.write(configfile)

	# Section must be an integer ==> it specifies what section of config.ini you're reading
	def _get_deezer_specified_param(self, param_name, section):
		self.config.read('data/config.ini')
		section = self.config.sections()[section]
		return self.config[section][param_name]

	def _parse_user_data(self, filename='data/config.ini'):
		self.config.read(filename)
		cache_name = self.config.sections()[1]
		self.app_id = self.config[cache_name]['APPID']
		self.redirect = self.config[cache_name]['REDIRECT']
		self.perms = self.config[cache_name]['PERMS']
		self.secret = self.config[cache_name]['SECRET']
		self.token = self.config[cache_name]['TOKEN']
		self.base_url = self.base_url.format(self.app_id, self.redirect, self.perms)

	def _get_code(self):
		webbrowser.open(self.base_url)
		url = input("Paste here the url you've been redirected to: ")
		self.code = url.split('code=')[1]

	def _request_access_token(self):
		self._get_code()
		return requests.get(
			self.token_url.format(
				id=self.app_id,
				secret=self.secret,
				code=self.code,
			)
		).json()

	def authenticate(self):
		self.token = self._request_access_token()
		return self.token['access_token']

	def _get_user_id(self):
		return requests.get(self.api_url.format('user/me'), params={'access_token': self.token}).json()['id']

	def add_track_to_playlist(self, track_id, playlist_id):
		payload = {'access_token': self.token, 'songs': str(track_id)}
		return requests.post(self.api_url.format('playlist/'+playlist_id+'/tracks'), data=payload).json()

	def add_tracks_to_playlist(self, tracks, playlist_id):
		bar = IncrementalBar('Transferring...', max = len(tracks))
		for track in tracks:
			try:
				bar.edit_message('Uploading track {} ...'.format(track))
				self.add_track_to_playlist(track, playlist_id)
				bar.next()
			except Exception as e:
				print('Errore adding track: ', e)
		bar.finish()

	def create_playlist(self, playlist_title):
		payload = {'access_token': self.token, 'title': playlist_title}
		user_id = self._get_user_id()
		return requests.post(self.api_url.format('user/'+str(user_id)+'/playlists'), data=payload).json()

	def get_track_url_from_title(self, query):
		result = self.client.search(query)[0]
		return result.link