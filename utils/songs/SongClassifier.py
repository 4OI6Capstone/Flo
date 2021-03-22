import mutagen
from pydub import AudioSegment
from utils.music_data_fetcher import *
from utils.songs.Song import Song
from werkzeug.utils import secure_filename

def create_song_from_metadata(song, filename):
    artist = song.get('artist')
    title = song.get('title')
    album = song.get('album')
    length = song.info.length
    mime = song.mime.pop(0)
    mime = mime.split("/")[1]
    # Create flo_song object
    return Song(artist, album, title, mime, filename, length)


def add_fetched_acoustic_brainz_info(flo_song, acoustic_brainz_info):
    rhythm_data = acoustic_brainz_info.get("rhythm")
    low_level_data = acoustic_brainz_info.get("lowlevel")
    flo_song.bpm = round(rhythm_data.get("bpm"), 1)
    flo_song.danceability = rhythm_data.get("danceability")
    flo_song.loudness = low_level_data.get("average_loudness")
    return flo_song


class SongClassifier:
    _song_list = dict()
    _save_location = "./uploaded_files/{}/{}"

    def __init__(self, song_list=dict()):
        self._song_list = song_list

    def deconstruct_songs(self, song_list, request_id):
        self.song_list[str(request_id)] = []
        for file in song_list:
            # Saves song onto server
            filename, filename_wav = self.save_song(file, request_id)
            # mutagen retrieves the metadata
            song = mutagen.File(filename, easy=True)
            flo_song = create_song_from_metadata(song, filename_wav)
            music_brainz_id = find_music_brainz_id_by_recording(flo_song)
            acoustic_brainz_low_info = get_acoustic_brainz_data(music_brainz_id, level="low-level")
            flo_song.music_brainz_id = music_brainz_id
            flo_song = add_fetched_acoustic_brainz_info(flo_song, acoustic_brainz_low_info)
            # Default set to crossfade until we implement the ML model that determines transitions
            #flo_song.transition = Tempo()
            self.song_list[str(request_id)].append(flo_song)

    def save_song(self, file, request_id):
        save_location = self._save_location.format(request_id, secure_filename(file.filename))
        file.save(save_location)
        my_mutagen = mutagen.File(save_location, easy=True)
        mime = my_mutagen.mime.pop(0)
        mime = mime.split("/")[1]
        song_wav = AudioSegment.from_file(save_location, mime)
        filename = file.filename.split(".")
        filename = "{}.{}".format(filename[0], "wav")
        save_location_wav = self._save_location.format(request_id, secure_filename(filename))
        song_wav.export(save_location_wav, format="wav")
        return save_location, save_location_wav

    @property
    def song_list(self):
        return self._song_list

    @song_list.setter
    def song_list(self, song_list):
        self._song_list = song_list
