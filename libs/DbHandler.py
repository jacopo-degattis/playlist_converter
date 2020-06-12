import time
import mysql.connector
import hashlib
from data.credentials import credentials 
from libs.Track import Track
from progress.bar import IncrementalBar

class DatabaseHandler(object):

	def __init__(self):
		self.host = credentials["host"]
		self.user = credentials["user"]
		self.password = credentials["password"]
		self.database = credentials["database"]

		self.db = mysql.connector.connect(
			host=self.host,
			user=self.user,
			password=self.password,
			database=self.database,
			buffered = True,
		)

	def login(self, username, password):
		password = hashlib.md5(password.encode()).hexdigest()
		cursor = self.db.cursor()
		query = f'SELECT * FROM Utente WHERE username="{username}" AND password="{password}"'
		cursor.execute(query)
		results = cursor.fetchone()
		if results:
			return True
		else:
			return False
		return False

	def user_exists(self, username):
		cursor = self.db.cursor()
		# Possibile cambiare con SELECT id_utente from ....
		query = f'SELECT * FROM Utente WHERE username="{username}"'
		cursor.execute(query)
		results = cursor.fetchall()
		if results:
			return results[0][5]
		else:
			return None
		return None

	def create_account(self, username, password, max_playlist, max_brani_playlist, max_brani_totale):
		cursor = self.db.cursor()
		query = f'''INSERT INTO Utente (username, password, max_playlist, max_brani_playlist, max_brani_totale)
					VALUES ("{username}", "{password}", {max_playlist}, {max_brani_playlist}, {max_brani_totale})'''
		cursor.execute(query)
		self.db.commit()

	def check_playlist(self, playlist_name):
		cursor = self.db.cursor()
		query = f'SELECT * FROM Playlist WHERE nome="{playlist_name}"'
		cursor.execute(query)
		results = cursor.fetchone()
		if results:
			return True
		else:
			return False

	def create_playlist(self, playlist_name, playlist_cover, private, user_id):
		success = False
		cursor = self.db.cursor()
		query = f'''INSERT INTO Playlist (nome, immagine, privata, id_utente)
					VALUES ("{playlist_name}", "{playlist_cover}", "{int(private)}", "{user_id}")'''
		try:
			cursor.execute(query)
			self.db.commit()
			success = True
		except Exception as e:
			print(e)
			success = False

		return success

	def get_playlist_id_from_name(self, name):
		cursor = self.db.cursor()
		query = f'SELECT Playlist.id_playlist FROM Playlist WHERE Playlist.nome="{name}"'
		try:
			cursor.execute(query)
			result = cursor.fetchone()[0]
			return result
		except Exception as e:
			print(e)
			return None
		return None

	def _get_track_id_from_name(self, name):
		cursor = self.db.cursor()
		query = f'SELECT id_traccia FROM TracciaAudio WHERE nome="{name}"'
		cursor.execute(query)
		track_id = cursor.fetchone()[0]
		return track_id

	def _create_artist(self, obj_artist):
		cursor = self.db.cursor()
		query = f"INSERT INTO Artista (nome, followers, image) VALUES ('{obj_artist.get_name()}', {obj_artist.get_followers()}, '{obj_artist.get_image()}')"
		cursor.execute(query)
		self.db.commit()

	def _get_artist_id_from_name(self, name):
		cursor = self.db.cursor()
		query = f'SELECT id_artista FROM Artista WHERE nome="{name}"'
		cursor.execute(query)
		artist_id = cursor.fetchone()[0]
		return artist_id

	def _create_relation_artist_track(self, artist_id, track_id):
		cursor = self.db.cursor()
		# Cambiare nome relazione
		query = f'INSERT INTO relation2 (id_artista, id_traccia) VALUES ({artist_id}, {track_id})'
		cursor.execute(query)
		self.db.commit()

	def _create_relation_playlist_track(self, track_id, playlist_id):
		cursor = self.db.cursor()
		query = f'INSERT INTO Contiene (id_traccia, id_playlist) VALUES ({track_id}, {playlist_id})'
		cursor.execute(query)
		self.db.commit()

	def get_track_list(self, playlist_name):
		track_lists = []
		playlist_id = self.get_playlist_id_from_name(playlist_name)

		# Ottengo tutti gli id delle tracce appartenti alla playlist
		cursor = self.db.cursor()
		query = f'SELECT id_traccia FROM Contiene WHERE id_playlist={playlist_id}'
		cursor.execute(query)
		# Lista di id relativi alle tracce appartenenti alla playlist
		results = cursor.fetchall()
		bar = IncrementalBar('Exporting...', max=len(results))
		# Scorro tutti gli id delle tracce
		for id_track in results:
			query = f'SELECT * FROM TracciaAudio WHERE id_traccia={id_track[0]}'
			cursor.execute(query)
			# Trasformo in lista per comodita
			results = list(cursor.fetchone())
			track_name = results[0]
			track_duration = results[2]

			# Ottenere id artista della traccia
			query = f'SELECT id_artista FROM relation2 WHERE id_traccia={id_track[0]}'
			cursor.execute(query)
			id_artista = cursor.fetchone()[0]

			# Ottenere nome artista
			query = f'SELECT Artista.nome FROM Artista WHERE Artista.id_artista={id_artista}'
			cursor.execute(query)
			artist_name = cursor.fetchone()[0]

			track_lists.append(
				Track(artist=artist_name,
					track_name=track_name,
					duration=track_duration,
					cover_image=None
				)
			)
			bar.next()
		bar.finish()
		return track_lists

	def _artist_exists(self, artist_name):
		cursor = self.db.cursor()
		query = f'SELECT * FROM Artista WHERE Artista.nome="{artist_name}"'
		cursor.execute(query)
		results = cursor.fetchone()
		if results:
			return True
		else:
			return False
		return False

	def create_audio_tracks(self, listtracks, playlist_id):
		cursor = self.db.cursor()
		bar = IncrementalBar('Importing...', max=len(listtracks))
		query = '''INSERT INTO TracciaAudio (nome, categoria, durata, addr_risorsa)
					VALUES ("{}", "{}", {}, "{}")'''
		for track in listtracks:
			#print(track.get_artist().get_name() + ' / ' + track.get_track_name())
			curr_query = query.format(
							track.get_track_name(),
							"Not yet available",
							track.get_duration(),
							'/tracks'
						)
			cursor.execute(curr_query)
			self.db.commit()
			track_id = self._get_track_id_from_name(track.get_track_name())
			self._create_relation_playlist_track(track_id, playlist_id)
			
			if not self._artist_exists(track.get_artist().get_name()):
				self._create_artist(track.get_artist())

			artist_id = self._get_artist_id_from_name(track.get_artist().get_name())
			self._create_relation_artist_track(artist_id, track_id)
			bar.next()
		bar.finish()