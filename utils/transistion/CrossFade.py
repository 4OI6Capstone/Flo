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
        # Use exit transition to create a segment
        combined = prev_song.append(next_song, crossfade=cross_fade_amount)
        return combined

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config
