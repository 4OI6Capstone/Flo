from pydub import AudioSegment
from pydub import scipy_effects
from pydub import silence
from utils.augmentation.song_extensions import song_extensions
from utils.transistion.Transition import Transition
from utils.transition_configs import loopout_config


class LoopIn(Transition):
    name = "loopin_transition"
    _config = dict()

    def __init__(self):
        self._config = loopin_config
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def apply(self, prev_song, next_song, **kwargs):
        """
        :param prev_song: previous song in the transition
        :param next_song: next song segment in the transition
        :param kwargs: dictionary containing prev_song_timestamp, next_song_timestamp
        :return: Audiosegment with the loopin transition applied.
        """

        prev_song_timestamp = kwargs.pop('transition_timestamp')

        # Get extension of song file
        next_ext = song_extensions.get(next_song.mime, next_song.mime)
        prev_ext = song_extensions.get(prev_song.mime, prev_song.mime)
        next_song_timestamp = 4 / (next_song.bpm / 60) * 1000
        # Create and AudioSegment object from the song_file
        next_song = AudioSegment.from_file(next_song.filename, format=next_ext)
        prev_song = AudioSegment.from_file(prev_song.filename, format=prev_ext)

        #idk about this, it strips the silence of the incoming song

        start_of_song = silence.detect_leading_silence(next_song, chunk_size=2)

        next_song_bar = next_song[start_of_song:next_song_timestamp]
        next_song_stripped = next_song[next_song_timestamp:]
        # freqs for the low pass filter; to introduce the song
        freq_cutoffs = [270, 400, 600, 1000, 2000, 2500, 3000, 4000]
        freq_highpass_cutoffs = [350, 450, 600, 1000, 2000, 3000, 4000, 5000]
        for i in range(8):
            if i == 0:
                next_song_loop = scipy_effects.low_pass_filter(next_song_bar, freq_cutoffs[i], 1)
            else:
                next_song_loop = next_song_loop.append(scipy_effects.low_pass_filter(next_song_bar, freq_cutoffs[i], 1))
        next_song = next_song_loop.append(next_song_stripped)
        loop_in_duration = len(next_song_loop)
        increment_length = len(next_song_loop) / 8
        loop_in_start_time = (prev_song_timestamp - loop_in_duration)
        window_left = loop_in_start_time
        window_right = window_left + increment_length

        for i in range(8):
            if i == 0:
                prev_song_seg = scipy_effects.high_pass_filter(prev_song[window_left:window_right],
                                                               freq_highpass_cutoffs[i], 1)
            else:
                prev_song_seg = prev_song_seg.append(scipy_effects.high_pass_filter(prev_song[window_left:window_right],
                                                                                    freq_highpass_cutoffs[i], 1),
                                                     crossfade=0)
            window_left = window_right
            window_right += increment_length
        prev_song = prev_song[:loop_in_start_time]
        next_song_overlayed = next_song.overlay(prev_song_seg, gain_during_overlay=-1)
        output = prev_song.append(next_song_overlayed)
        return output

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config