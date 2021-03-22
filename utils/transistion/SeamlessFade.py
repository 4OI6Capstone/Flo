from pydub import AudioSegment
from pydub import scipy_effects
from utils.augmentation.song_extensions import song_extensions
from utils.transistion.Transition import Transition
from utils.transition_configs import loopout_config


class SeamlessFade(Transition):
    name = "seamless_transition"
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

        :param prev_song: previous song in transition
        :param next_song: next song in transition
        :param kwargs: dictionary containing: transition timestamp of previous song, a timestamp of the
        ending point of the bar of the previous song
        :return:
        """

        transition_timestamp = kwargs.pop('transition_timestamp')
        bar_end_timestamp = kwargs.pop('bar_end_timestamp')
        # Get extension of song file
        next_ext = song_extensions.get(next_song.mime, next_song.mime)
        prev_ext = song_extensions.get(prev_song.mime, prev_song.mime)
        # Create and AudioSegment object from the song_file
        next_song = AudioSegment.from_file(next_song.filename, format=next_ext)
        prev_song = AudioSegment.from_file(prev_song.filename, format=prev_ext)

        two_bar_timestamp = (bar_end_timestamp - transition_timestamp) * 2
        prev_song_overlay = prev_song[transition_timestamp:transition_timestamp + two_bar_timestamp]
        bar_length = bar_end_timestamp - transition_timestamp
        prev_song_past_transition = prev_song[transition_timestamp + two_bar_timestamp:]
        prev_song = prev_song[:transition_timestamp]
        next_song_overlay = next_song[:two_bar_timestamp]
        next_song_stripped = next_song[two_bar_timestamp:]

        prev_song_freq = [270, 400, 600, 1000, 2000, 2500, 3000, 4000]
        next_song_freq = [350, 450, 600, 1000, 2000, 3000, 4000, 5000]

        beat_length = bar_length / 4
        window_left = 0
        window_right = beat_length
        for i in range(8):
            if i == 0:
                prev_song_seg = scipy_effects.high_pass_filter(prev_song_overlay[window_left:window_right],
                                                               prev_song_freq[i], 1)
                next_song_seg = scipy_effects.low_pass_filter(next_song_overlay[window_left:window_right],
                                                              next_song_freq[i], 1)
            else:
                prev_song_seg = prev_song_seg.append(
                    scipy_effects.high_pass_filter(prev_song_overlay[window_left:window_right], prev_song_freq[i], 1),
                    crossfade=0)
                next_song_seg = next_song_seg.append(
                    scipy_effects.low_pass_filter(next_song_overlay[window_left:window_right], prev_song_freq[i], 1),
                    crossfade=0)
            window_left = window_right
            window_right += beat_length
        window_left = 0
        window_right = bar_length
        for i in range(4):
            prev_song_seg = prev_song_seg.append(scipy_effects.high_pass_filter
                                                 (prev_song_past_transition[window_left:window_right] - ((i + 1) * 5),
                                                  prev_song_freq[7], 1), crossfade=0)
            window_left = window_right
            window_right += beat_length
        next_song = next_song_seg.append(next_song_stripped, crossfade=0)
        next_song = next_song.overlay(prev_song_seg, gain_during_overlay=-1)
        output = prev_song.append(next_song, crossfade=0)
        return output

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config