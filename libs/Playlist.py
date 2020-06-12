
class Playlist(object):

	def __init__(self, nome, immagine, privata):
		self.nome = nome
		self.immagine = immagine
		self.privata = privata

	def get_nome(self):
		return self.nome

	def get_immagine(self):
		return self.immagine

	def get_privata(self):
		return self.privata