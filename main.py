#!/usr/bin/python3

import sys
from libs.PlaylistConverter import PlaylistConverter
p = PlaylistConverter()

# Rimuovere dal config file tutti gli strip()
# Questo perche basta rimuovere gli apici dal file config.ini

logo_print = '''
   _____             _   _  __       
  / ____|           | | (_)/ _|      
 | (___  _ __   ___ | |_ _| |_ _   _ 
  \___ \| '_ \ / _ \| __| |  _| | | |
  ____) | |_) | (_) | |_| | | | |_| |
 |_____/| .__/ \___/ \__|_|_|  \__, |
        | |                     __/ |
        |_|                    |___/ 

'''

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print('[!] Usage: ./convert spotify_url')
	else: 
		print(logo_print)
		#Contiene l'url della playlist di spotify da convertire
		#spotify_url = input('* Playlist url to convert : ')
		p.convert(sys.argv[1])