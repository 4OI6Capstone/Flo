import mutagen
from utils.music_data_fetcher import *
from utils.songs.Song import Song
from utils.transistion.CrossFade import CrossFade
import pathlib
from werkzeug.utils import secure_filename


class SongClassifier:
    _song_list = dict()
    _save_location = "./uploaded_files/{}/{}"

    def __init__(self, song_list=dict()):
        self._song_list = song_list

    def deconstruct_songs(self, song_list, request_id):
        self.song_list[str(request_id)] = []
        for file in song_list:
            filename = self.save_song(file, request_id)
            song = mutagen.File(filename, easy=True)
            artist = song.get('artist')
            title = song.get('title')
            album = song.get('album')
            mime = song.mime.pop(0)
            mime = mime.split("/")[1]
            flo_song = Song(artist, album, title, mime, filename)
            music_brainz_id = find_music_brainz_id_by_recording(flo_song)
            flo_song.set_music_brainz_id(music_brainz_id)
            # Default set to crossfade until we implement the ML model that determines transitions
            flo_song.transition = CrossFade()
            self.song_list[str(request_id)].append(flo_song)

    def save_song(self, file, request_id):
        save_location = self._save_location.format(request_id, secure_filename(file.filename))
        file.save(save_location)
        return save_location

    @property
    def song_list(self):
        return self._song_list

    @song_list.setter
    def song_list(self, song_list):
        self._song_list = song_list
