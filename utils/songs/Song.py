from utils import music_data_fetcher
from utils.transistion.Transition import Transition
import logging
log = logging.getLogger(__name__)


class Song:
    _title = None
    _album = None
    _artist = None
    _music_brainz_id = None
    _transition = None
    _mime = None
    _filename = None

    def __init__(self, artist, album, title, mime, filename):
        self._title = title
        self._album = album
        self._artist = artist
        self._mime = mime
        self._filename = filename

    def set_music_brainz_id(self, brainz_id):
        self._music_brainz_id = brainz_id

    @property
    def music_brainz_id(self):
        return self._music_brainz_id

    @property
    def artist(self):
        return self._artist

    @property
    def mime(self):
        return self._mime

    @property
    def album(self):
        return self._album

    @property
    def title(self):
        return self._title

    @property
    def transition(self):
        return self._transition

    @property
    def filename(self):
        return self._filename

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

    @transition.setter
    def transition(self, transition):
        if isinstance(transition, Transition):
            self._transition = transition
        else:
            log.error("Invalid transition type")
            raise TypeError(type(transition), "Invalid Transition Type")


    @mime.setter
    def mime(self, mime):
        self._mime = mime

    @filename.setter
    def filename(self, filename):
        self._filename = filename
