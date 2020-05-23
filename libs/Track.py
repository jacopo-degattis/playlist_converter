class Track(object):
    def __init__(self, artist, track_name):
        self.artist = artist
        self.track_name = track_name

    def get_artist(self):
        return self.artist

    def get_track_name(self):
        return self.track_name