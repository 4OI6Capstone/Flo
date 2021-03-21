from pydub import AudioSegment
from utils.augmentation.song_extensions import song_extensions
from utils.transistion.Transition import Transition

from utils.transition_configs import crossfade_config


class CrossFade(Transition):

    name = "crossfade_transition"
    _config = dict()

    def __init__(self):
        self._config = crossfade_config
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def apply(self, prev_song, next_song, **kwargs):
        cross_fade_amount = kwargs.pop('cross_fade')
        # Find extension of song file
        next_ext = song_extensions.get(next_song.mime, next_song.mime)
        prev_ext = song_extensions.get(prev_song.mime, prev_song.mime)
        # Create and AudioSegment object from the song_file
        next_song = AudioSegment.from_file(next_song.filename, format=next_ext)
        prev_song = AudioSegment.from_file(prev_song.filename, format=prev_ext)
        # Use exit transition to create a segment
        combined = prev_song.append(next_song, crossfade=cross_fade_amount)
        return combined

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config
