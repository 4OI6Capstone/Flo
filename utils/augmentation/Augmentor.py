from pydub import AudioSegment
import logging
from utils.timestamp import get_timestamp_loop, get_timestamp
from utils.transition_thresholds import transition_thresholds
from utils.transistion.CrossFade import CrossFade
from utils.transistion.Loopout import Loopout
from utils.transistion.LoopIn import LoopIn
from utils.transistion.Tempo import Tempo
from utils.transistion.SeamlessFade import SeamlessFade

log = logging.getLogger(__name__)

def join_songs(prev_song, next_song, request_id):
    # Get transition specific configs
    transition_config = prev_song.transition.config
    # Check to see if config if a bar transition or time transition
    if transition_config.get("bar_transition"):
        # Get bar transition time
        output_from_module_3 = get_timestamp_loop(prev_song, next_song)
        transition_config["transition_timestamp"] = output_from_module_3[0]
        transition_config["bar_end_timestamp"] = output_from_module_3[1]
    else:
        # Get transition time
        transition_config["transition_time"] = get_timestamp(prev_song, next_song)
    song_segment = prev_song.transition.apply(prev_song, next_song, **transition_config, request_id=str(request_id))
    return song_segment


def find_transition(prev_song, next_song, thresholds):
    bpm_difference = abs(prev_song.bpm - next_song.bpm)
    complexity_difference = abs(prev_song.dynamic_complexity - next_song.dynamic_complexity)
    if complexity_difference > 3:
        if prev_song.dynamic_complexity > next_song.dynamic_complexity:
            log.info("Loopout transition applied")
            return Loopout()
        else:
            log.info("Loopin transition applied")
            return LoopIn()
    if bpm_difference > 15:
        log.info("Tempo transition applied")
        return Tempo()
    if complexity_difference > 1.5:
        log.info("SeamlessFade transition applied")
        return SeamlessFade()
    log.info("Crossfade transition applied")
    return CrossFade()


class Augmentor:
    _song_list = list()

    def __init__(self, song_list):
        self._song_list = song_list
        self.apply_transitions()

    def create_mix(self, request_id):
        final_mix = AudioSegment.empty()
        for i in range(len(self._song_list) - 1):
            curr_song_file = self._song_list[i + 1]
            prev_song_file = self._song_list[i]
            # Create segment to add to final mix
            mixed_song_segment = join_songs(prev_song_file, curr_song_file, request_id)
            final_mix = final_mix + mixed_song_segment

        return final_mix

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