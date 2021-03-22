from pydub import AudioSegment

from utils.timestamp import get_timestamp_loop, get_timestamp
from utils.transition_thresholds import transition_thresholds
from utils.transistion.CrossFade import CrossFade


def join_songs(prev_song, next_song, request_id):
    # Get transition specific configs
    transition_config = prev_song.transition.config
    # Check to see if config if a bar transition or time transition
    if transition_config.get("bar_transition"):
        # Get bar transition time
        transition_config["bar_timestamp"] = get_timestamp_loop(prev_song, next_song)
    else:
        # Get transition time
        transition_config["transition_time"] = get_timestamp(prev_song, next_song)
    song_segment = prev_song.transition.apply(prev_song, next_song, **transition_config, request_id=str(request_id))
    return song_segment


def find_transition(prev_song, next_song, thresholds):
    bpm_difference = abs(prev_song.bpm - next_song.bpm)
    dancabililty_difference = abs(prev_song.danceability - next_song.danceability)
    loudness_difference = abs(prev_song.loudness - next_song.loudness)
    # Loop through transitions and compare difference tresholds to song differences
    for transition in thresholds:
        transition_config = thresholds[transition]
        bpm_threshold = transition_config.get('bpm_threshold')
        danceability_threshold = transition_config.get('danceability_threshold')
        loudness_threshold = transition_config.get('loudness_threshold')
        if bpm_difference <= bpm_threshold and \
                dancabililty_difference <= danceability_threshold and \
                loudness_difference <= loudness_threshold:
            return transition()
    # Default transition to return for now
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