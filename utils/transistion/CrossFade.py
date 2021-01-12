from utils.transistion.Transition import Transition
import pydub


class CrossFade(Transition):

    def __init__(self):
        pass

    def apply(self, prev_song, next_song, **kwargs):
        cross_fade_amount = kwargs.pop('cross_fade')
        combined = prev_song.append(next_song, crossfade=cross_fade_amount)
        return combined
