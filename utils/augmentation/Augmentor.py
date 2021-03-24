from pydub import AudioSegment
import logging

from utils.augmentation.song_extensions import song_extensions
from utils.timestamp import get_timestamp_loop, get_timestamp
from utils.transition_thresholds import transition_thresholds
from utils.transistion.CrossFade import CrossFade
from utils.transistion.Loopout import Loopout
from utils.transistion.LoopIn import LoopIn
from utils.transistion.Tempo import Tempo
from utils.transistion.SeamlessFade import SeamlessFade

log = logging.getLogger(__name__)

def join_songs(final_segment, curr_song, prev_song, transition_time, transition_bar_time, request_id):
    # Get transition specific configs
    transition_config = prev_song.transition.config
    curr_song_ext = song_extensions.get(curr_song.mime, curr_song.mime)
    curr_song_segment = AudioSegment.from_file(curr_song.filename, format=curr_song_ext)
    transition_config["curr_song_bpm"] = curr_song.bpm
    transition_config["prev_song_bpm"] = prev_song.bpm
    # Check to see if config if a bar transition or time transition
    if transition_config.get("bar_transition"):
        # Get bar transition time
        transition_config["transition_timestamp"] = transition_time
        transition_config["bar_end_timestamp"] = transition_bar_time
    else:
        # Get transition time
        transition_config["transition_time"] = transition_time
    song_segment = prev_song.transition.apply(final_segment, curr_song_segment, **transition_config,
                                              request_id=str(request_id))
    return song_segment


def find_transition(prev_song, next_song, thresholds):
    return SeamlessFade()
    bpm_difference = abs(prev_song.bpm - next_song.bpm)
    complexity_difference = abs(prev_song.dynamic_complexity - next_song.dynamic_complexity)
    if complexity_difference > 3 or bpm_difference > 30:
        if prev_song.dynamic_complexity > next_song.dynamic_complexity:
            log.info("Loopout transition applied")
            return Loopout()
        else:
            log.info("Loopin transition applied")
            return LoopIn()
    if 15 < bpm_difference < 25:
        log.info("Tempo transition applied")
        return Tempo()
    elif complexity_difference < 1.5:
        log.info("CrossFade transition applied")
        return CrossFade()
    else:
        log.info("SeamlessFade transition applied")
        return SeamlessFade()



class Augmentor:
    _song_list = list()
    current_mix_time_ms = 0

    def __init__(self, song_list):
        self._song_list = song_list
        self.apply_transitions()
        self.find_transition_times()

    def create_mix(self, request_id):
        first_song = self._song_list[0]
        first_song_ext = song_extensions.get(first_song.mime, first_song.mime)
        final_mix = AudioSegment.from_file(first_song.filename, format=first_song_ext)
        for i in range(len(self._song_list) - 1):
            curr_song_file = self._song_list[i + 1]
            prev_song_file = self._song_list[i]
            transition_time = self.current_mix_time_ms + prev_song_file.transition_time
            transition_bar_time = self.current_mix_time_ms + prev_song_file.transition_bar_time
            # Create segment to add to final mix
            mixed_song_segment = join_songs(final_mix, curr_song_file, prev_song_file, transition_time,
                                            transition_bar_time, request_id)
            final_mix = mixed_song_segment
            self.current_mix_time_ms = (final_mix.duration_seconds*1000)-prev_song_file.length

        return final_mix

    def find_transition_times(self):
        for i in range(len(self._song_list) - 1):
            curr_song = self._song_list[i + 1]
            prev_song = self._song_list[i]
            transition_config = prev_song.transition.config
            if transition_config.get("bar_transition"):
                # Get bar transition time
                log.info("Starting Bar transition time finder")
                output_from_module_3 = get_timestamp_loop(prev_song, curr_song)
                transition_time = output_from_module_3[0]
                transition_bar_time = output_from_module_3[1]
            else:
                # Get transition time
                log.info("Starting normal transition time finder")
                transition_time = get_timestamp(prev_song, curr_song)
                transition_bar_time = 0
            prev_song.transition_time = transition_time
            prev_song.transition_bar_time = transition_bar_time

    def apply_transitions(self):
        for i in range(0, len(self._song_list) - 1):
            transition = find_transition(self._song_list[i], self._song_list[i + 1], transition_thresholds)
            self._song_list[i].transition = transition

    @property
    def song_list(self):
        return self._song_list

    @song_list.setter
    def song_list(self, song_list):
        self._song_list = song_list