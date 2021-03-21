from pydub import AudioSegment
from pydub import scipy_effects
from utils.augmentation.song_extensions import song_extensions
from utils.transistion.Transition import Transition
from utils.transition_configs import loopout_config


class Loopout(Transition):
    name = "loopout_transition"
    _config = dict()

    def __init__(self):
        self._config = loopout_config
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def apply(self, prev_song, next_song, **kwargs):
        """
           :param next_song: next_song
           :param prev_song: prev_song
           :param bar_timestamp: The point at which the bar we want to start transitioning out of
           :param bar_end_timestamp: The end timing time of the specified bar
           :param prev_cutoff: Low-pass freq cutoff for outgoing song
           :param next_cutoff: Low-pass freq cutoff for incoming song during the loop (will be played underneath)
           :param num_full_bars:Number of times to loop the full bar
           :param num_half_bars:Number of times to loop the half-bar
           :param num_quart_bars:Number of times to loop the quarter bar
           :return: returns an AudioSegment with the loop transition in between the two songs.
        """
        bar_time = kwargs.pop('bar_timestamp')
        bar_end_time = kwargs.pop('bar_end_timestamp')
        prev_song_freq_cutoff = kwargs.setdefault('prev_cutoff', 4000)
        next_song_freq_cutoff = kwargs.setdefault('next_cutoff', 2000)
        full_repeat = kwargs.setdefault('num_full_bars', 4)
        half_repeat = kwargs.setdefault('num_half_bars', 4)
        quarter_repeat = kwargs.setdefault('num_quart_bars', 4)

        # Get extension of song file
        next_ext = song_extensions.get(next_song.mime, next_song.mime)
        prev_ext = song_extensions.get(prev_song.mime, prev_song.mime)
        # Create and AudioSegment object from the song_file
        next_song = AudioSegment.from_file(next_song.filename, format=next_ext)
        prev_song = AudioSegment.from_file(prev_song.filename, format=prev_ext)

        prev_song_stripped = prev_song[:bar_time]
        prev_song_bar = prev_song[bar_time:bar_end_time]
        bar_length = bar_end_time - bar_time
        curr_bar_half = prev_song_bar[:bar_length / 2]
        curr_bar_quarter = prev_song_bar[:bar_length / 4]
        for i in range(full_repeat):
            if i == 0:
                result = prev_song_bar
            else:
                result = result.append(prev_song_bar)
        for i in range(half_repeat):
            result = result.append(curr_bar_half)
        for i in range(quarter_repeat):
            result = result.append(curr_bar_quarter)

        result = scipy_effects.low_pass_filter(result, prev_song_freq_cutoff, order=1)
        overlap_duration = len(result)
        next_song_seg = next_song[:overlap_duration]
        next_song_seg = scipy_effects.low_pass_filter(next_song_seg, next_song_freq_cutoff, order=2)
        result = next_song_seg.overlay(result, gain_during_overlay=-5)

        result = result.append(next_song[overlap_duration:], crossfade=100)
        output = prev_song_stripped.append(result, crossfade=500)
        return output

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config
