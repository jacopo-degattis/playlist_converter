from libs.Artist import Artist

class Track(object):
    def __init__(self, artist, track_name, cover_image, duration):
        self.artist = artist
        self.track_name = track_name
        self.cover_image = cover_image
        self.duration = duration
        self.artist = artist

    def get_artist(self):
        return self.artist

    def get_track_name(self):
        return self.track_name

    def get_cover_image(self):
    	return self.cover_image

    def get_duration(self):
        return self.duration

    def get_artist(self):
        return self.artist