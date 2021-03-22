from pydub import AudioSegment
from utils.transistion.Transition import Transition
from utils.augmentation.song_extensions import song_extensions
import soundfile as sf
import pyrubberband as pyrb
from flask import current_app
from utils.transition_configs import tempo_config


def augment_segments(audio_segments, start_bpm, end_bpm, request_id, direction):
    """
    :param audio_segments: AudioSegment segments that need slowing down, will convert to wav then slow then convert back
    :param start_bpm: Original Bpm
    :param end_bpm: final bpm
    :param request_id: request_id to store augmented segments
    :param direction: direction of speed up, either speed up or down indicated by -1 and +1
    """
    bpm_change = int(abs(start_bpm - end_bpm))
    bpm_change_per_iteration = 1
    augmented_segment_list = list()
    for i in range(bpm_change):
        file_path = current_app.config['EXPORT_FOLDER'] + str(request_id)
        segment_path = file_path + "/segment_{}".format(i)
        exported_segment_path = file_path + "/segment_exported_{}".format(i)
        curr_segment = audio_segments[i]
        curr_segment.export(segment_path, format="wav")
        y, sr = sf.read(segment_path)
        stretch = (start_bpm + (direction * bpm_change_per_iteration)) / start_bpm
        y_stretch = pyrb.time_stretch(y, sr, stretch)
        bpm_change_per_iteration = bpm_change_per_iteration + 1
        sf.write(exported_segment_path, y_stretch, sr, format='wav')
        augmented_segment = AudioSegment.from_wav(exported_segment_path)
        augmented_segment_list.append(augmented_segment)

    return augmented_segment_list


class Tempo(Transition):
    _segment_list = list()
    name = "tempo_transition"
    _config = dict()

    def __init__(self):
        self._config = tempo_config
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def apply(self, prev_song, next_song, **kwargs):
        """
        :param next_song: next_song
        :param prev_song: prev_song
        :param transition_time: time the transition takes place, the function will apply n segments of
        slowing/speeding up beforehand
        """
        # Grab transition time
        trans_time = round(kwargs.setdefault("transition_time", round(prev_song.length - 1))/1000)
        request_id = kwargs.setdefault("request_id", 1)
        # Find extension of song file
        next_ext = song_extensions.get(next_song.mime, next_song.mime)
        prev_ext = song_extensions.get(prev_song.mime, prev_song.mime)
        # Create and AudioSegment object from the song_file
        next_song_as = AudioSegment.from_file(next_song.filename, format=next_ext)
        prev_song_as = AudioSegment.from_file(prev_song.filename, format=prev_ext)
        # Calculate bpm change and find direction
        bpm_change = int(abs(prev_song.bpm - next_song.bpm))
        if bpm_change < 1:
            return prev_song_as.append(next_song_as, crossfade=2000)
        direction = 1 if prev_song.bpm < next_song.bpm else -1
        # Iterate through transition segments and create segments for every second
        for i in range(bpm_change, 0, -1):
            trans_seg = prev_song_as[(trans_time - i) * 1000:(trans_time - i + 1) * 1000]
            self._segment_list.append(trans_seg)

        # Create augmented segments
        augmented_segments = augment_segments(self._segment_list, prev_song.bpm, next_song.bpm, request_id, direction)
        prev_song_cut = prev_song_as[:((trans_time - bpm_change) * 1000)]
        # Loop through augmented segments and add them back together
        for segment in augmented_segments:
            prev_song_cut = prev_song_cut.append(segment, crossfade=0)

        combined = prev_song_cut.append(next_song_as, crossfade=2000)
        return combined

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config
