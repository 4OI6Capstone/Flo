from utils import MusicDataFetcher


class Song:
    _title = None
    _album = None
    _artist = None
    _music_brainz_id = None

    def __init__(self, artist, album, title):
        self._title = title
        self._album = album
        self._artist = artist

    def set_music_brainz_id(self, brainz_id):
        self._music_brainz_id = brainz_id

    @property
    def music_brainz_id(self):
        return self._music_brainz_id

    @property
    def artist(self):
        return self._artist

    @property
    def album(self):
        return self._album

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @album.setter
    def album(self, album):
        self._album = album

    @artist.setter
    def artist(self, artist):
        self._artist = artist

    @music_brainz_id.setter
    def music_brainz_id(self, music_brainz_id):
        self._music_brainz_id = music_brainz_id


