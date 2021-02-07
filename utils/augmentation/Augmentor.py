from pydub import AudioSegment
from utils.augmentation.song_extensions import song_extensions
from werkzeug.utils import secure_filename


def join_songs(prev_song, next_song):
    # Default so far cross fade
    song_segment = prev_song.transition.apply(prev_song, next_song, cross_fade=5000)
    return song_segment


class Augmentor:
    _song_list = list()

    def __init__(self, song_list):
        self._song_list = song_list

    def create_mix(self):
        final_mix = AudioSegment.empty()
        for i in range(len(self._song_list) - 1):
            curr_song_file = self._song_list[i + 1]
            prev_song_file = self._song_list[i]
            # Create segment to add to final mix
            mixed_song_segment = join_songs(prev_song_file, curr_song_file)
            final_mix = final_mix + mixed_song_segment

        return final_mix

    @property
    def song_list(self):
        return self._song_list

    @song_list.setter
    def song_list(self, song_list):
        self._song_list = song_list
