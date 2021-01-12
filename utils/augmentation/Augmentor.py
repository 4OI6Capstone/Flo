from pydub import AudioSegment
from utils.augmentation.song_extensions import song_extensions
from werkzeug.utils import secure_filename


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
            mixed_song_segment = self.join_songs(prev_song_file, curr_song_file)
            final_mix = final_mix + mixed_song_segment

        return final_mix

    def join_songs(self, prev_flo_song, curr_flo_song):
        # Find extension of song file
        curr_ext = song_extensions.get(curr_flo_song.mime, curr_flo_song.mime)
        prev_ext = song_extensions.get(prev_flo_song.mime, prev_flo_song.mime)
        # Create and AudioSegment object from the song_file
        curr_song = AudioSegment.from_file(curr_flo_song.filename, format=curr_ext)
        prev_song = AudioSegment.from_file(prev_flo_song.filename, format=prev_ext)
        # Use exit transition to create a segment
        # Default so far cross fade
        song_segment = prev_flo_song.transition.apply(prev_song, curr_song, cross_fade=5000)
        return song_segment

    @property
    def song_list(self):
        return self._song_list

    @song_list.setter
    def song_list(self, song_list):
        self._song_list = song_list
