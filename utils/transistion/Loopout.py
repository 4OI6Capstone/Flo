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
           :return: returns an AudioSegment with the loop transition in between the two songs.
        """
        bar_time = kwargs.pop('transition_timestamp')
        bar_end_time = kwargs.pop('bar_end_timestamp')

        prev_song_stripped = prev_song[:bar_time]
        prev_song_bar = prev_song[bar_time:bar_end_time]
        bar_length = bar_end_time - bar_time
        prev_bar_half = prev_song_bar[:bar_length / 2]
        prev_bar_quarter = prev_song_bar[:bar_length / 4]
        quarter_bar_time = len(prev_bar_quarter)

        four_bar_loop = prev_song_bar

        four_bar_loop = four_bar_loop.append(prev_song_bar).append(prev_song_bar).append(prev_song_bar)
        four_bar_loop_length = len(four_bar_loop)
        freq_to_cutoff_1 = [270, 400, 600, 1000]
        freq_to_cutoff_2 = [2000, 2500, 3000, 3500]
        # 4k,4k,5k,5k or 4 5 6 7
        freq_to_cutoff_3 = [4000, 4000, 5000, 5000]

        for i in range(4):
            four_bar_loop = four_bar_loop.append(scipy_effects.high_pass_filter
                                                 (prev_song_bar, freq_to_cutoff_1[i], 5))
        for i in range(4):
            four_bar_loop = four_bar_loop.append(
                scipy_effects.high_pass_filter(prev_bar_half, freq_to_cutoff_2[i], 5))
        for i in range(4):
            four_bar_loop = four_bar_loop.append(
                scipy_effects.high_pass_filter(prev_bar_quarter, freq_to_cutoff_3[i]))
        prev_song_stripped = prev_song_stripped.append(four_bar_loop, crossfade=0)
        # start processing for next song here
        next_song_seg = next_song[:len(four_bar_loop) * 2]
        window_left = 0
        window_right = len(prev_song_bar)
        freq_to_cutoff = [270, 400, 600, 1000, 2000, 2500, 3000, 3500]
        for i in range(8):
            if i == 0:
                next_song_seg_filtered = scipy_effects.low_pass_filter(next_song_seg[window_left:window_right],
                                                                       freq_to_cutoff[i])
            else:
                next_song_seg_filtered = next_song_seg_filtered.append(
                    scipy_effects.low_pass_filter(next_song_seg[window_left:window_right], freq_to_cutoff[i]),
                    crossfade=0)
            window_left = window_right
            window_right += quarter_bar_time

        next_song_seg_filtered = next_song_seg_filtered.append(next_song_seg[len(next_song_seg_filtered):], crossfade=0)
        next_song_stripped = next_song[len(next_song_seg_filtered):]
        next_song_seg_filtered = next_song_seg_filtered.append(next_song_stripped)
        # overlay songs here
        overlap_time = bar_time + four_bar_loop_length
        overlap_for_next_song = len(prev_song_stripped[overlap_time:])
        next_song_overlay = next_song_seg_filtered[:overlap_for_next_song]
        next_song_seg_filtered = next_song_seg_filtered[len(next_song_overlay):]
        output = prev_song_stripped.overlay(next_song_overlay, position=overlap_time, gain_during_overlay=0)
        output = output.append(next_song_seg_filtered)

        return output

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config
