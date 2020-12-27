from utils import MusicDataFetcher


class Song:
    title = None
    album = None
    artist = None
    music_brainz_id = None

    def __init__(self, title, album, artist):
        self.title = title
        self.album = album
        self.artist = artist

    def set_music_brainz_id(self, brainz_id):
        self.music_brainz_id = brainz_id
