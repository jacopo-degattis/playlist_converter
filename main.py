#!/usr/bin/env python3

import os
import sys
import getpass
import argparse
import random
import hashlib 
from libs.Spotify import Spotify
from libs.DbHandler import DatabaseHandler

spotify = Spotify()
dbhand = DatabaseHandler()
parser = argparse.ArgumentParser(
	description='Spotify Playlist'
)

spotify_logo = '''
   _____             _   _  __       
  / ____|           | | (_)/ _|      
 | (___  _ __   ___ | |_ _| |_ _   _ 
  \___ \| '_ \ / _ \| __| |  _| | | |
  ____) | |_) | (_) | |_| | | | |_| |
 |_____/| .__/ \___/ \__|_|_|  \__, |
        | |                     __/ |
        |_|                    |___/ 
'''

parser.add_argument('--importa', type=str, help='Import a spotify playlist in MyAudio')
parser.add_argument('--export', type=str, help='Export a MyAudio in Spotify')
parser.add_argument('--create', type=str, help='Create an account on MyAudio Platform')
parser.add_argument('--user', type=str, help='username')
args = parser.parse_args()

# Manca da realizzare l'esportazione dei dati da MyAudio a piattaforma esterna

if __name__ == '__main__':

	# Migliorare main creando classe Conversione che contenga tutte queste procedure
	if args.create:
		username = args.create
		password = getpass.getpass()
		dbhand.create_account(
			username,
			hashlib.md5(password.encode()).hexdigest(),
			random.randint(10, 20),
			random.randint(200, 400),
			random.randint(100, 200)
		)
		print('Accout creato')
	elif args.importa and args.user:
		password = getpass.getpass()
		username = args.user
		os.system('/usr/bin/clear')
		print(spotify_logo)
		if dbhand.login(username, password):
			spotify_url = args.importa

			# Carico le tracce dalla playlist
			spotify_playlist_id = spotify.get_playlist_id(spotify_url)
			sys.stdout.write('[!] Getting tracks from spotify playlist\r')
			listtracks = spotify.parse_playlist_from_url(spotify_playlist_id)
			sys.stdout.write('[+] Done!\r')
			# Creo un oggetto di tipo Playlist
			playlist_object = spotify.get_playlist_object(spotify_url)
			
			# Verifico che l'utente esista sulla piattaforma MyAudio
			'''username = spotify.get_user_infos()['id']'''
			user_id=dbhand.user_exists(username)

			sys.stdout.write('[!] Creating myaudio playlist\r')
			dbhand.create_playlist(
				playlist_object.get_nome(),
				playlist_object.get_immagine(),
				playlist_object.get_privata(),
				user_id
			)
			sys.stdout.write('[+] Playlist created!\r')
			playlist_id = dbhand.get_playlist_id_from_name(playlist_object.get_nome())
			sys.stdout.write('[!] Creating audio tracks\r')
			dbhand.create_audio_tracks(listtracks, playlist_id)
			sys.stdout.write('[+] Tracks written succesfully!\r')
		else:
			print('Credenziali non valide!')
	elif args.export and args.user:
		password = getpass.getpass()
		username = args.user
		print(spotify_logo)
		if dbhand.login(username, password):
			playlist_name = args.export
			if dbhand.check_playlist(playlist_name):
				# Se la playlist esiste proseguo
				sys.stdout.write('[!] Reading local tracks...\r')
				listatracce = dbhand.get_track_list(playlist_name)
				sys.stdout.write('[+] Loaded succesfully!\r')
				sys.stdout.write('[!] Uploading tracks to spotify...\r')
				spotify.upload_tracks(listatracce, playlist_name)
				sys.stdout.write('[+] Uploaded succesfully!\r')
			else:
				print('La playlist indicata non esiste!')
		else:
			print('Credenziali non valide!')