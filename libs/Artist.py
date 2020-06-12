class Artist(object):

	def __init__(self, name, followers, image):
		self.name = name
		self.followers = followers
		self.image = image

	def get_name(self):
		return self.name

	def get_followers(self):
		return self.followers

	def get_image(self):
		return self.image