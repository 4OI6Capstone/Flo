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
    _bpm = None
    _length = None
    _danceability = None
    _loudness = None
    _dynamic_complexity = None
    _transition_time = None
    _transition_bar_time = None

    def __init__(self, artist, album, title, mime, filename, length):
        self._title = title
        self._album = album
        self._artist = artist
        self._mime = mime
        self._filename = filename
        self._length = length*1000

    @property
    def transition_time(self):
        return self._transition_time

    @property
    def danceability(self):
        return self._danceability

    @property
    def dynamic_complexity(self):
        return self._dynamic_complexity

    @property
    def loudness(self):
        return self._loudness

    @property
    def length(self):
        return self._length

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

    @property
    def bpm(self):
        return self._bpm

    @property
    def transition_bar_time(self):
        return self._transition_bar_time

    @transition_bar_time.setter
    def transition_bar_time(self, time):
        self._transition_bar_time = time

    @transition_time.setter
    def transition_time(self, time):
        self._transition_time = time

    @danceability.setter
    def danceability(self, danceability):
        self._danceability = danceability

    @dynamic_complexity.setter
    def dynamic_complexity(self, dynamic_complexity):
        self._dynamic_complexity = dynamic_complexity

    @loudness.setter
    def loudness(self, loudness):
        self._loudness = loudness

    @length.setter
    def length(self, length):
        self._length = length

    @bpm.setter
    def bpm(self, bpm):
        self._bpm = bpm

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
