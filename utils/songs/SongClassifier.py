import mutagen
from utils.MusicDataFetcher import *
from utils.songs.Song import Song


class SongClassifier:
    song_list = dict()

    def __init__(self, song_list=dict()):
        self.song_list = song_list

    def deconstruct_songs(self, song_list, request_id):
        self.song_list[str(request_id)] = []
        for file in song_list:
            song = mutagen.File(file, easy=True)
            artist = song.get('artist')
            title = song.get('title')
            album = song.get('album')
            flo_song = Song(artist, album, title)
            music_brainz_id = find_music_brainz_id_by_recording(flo_song)
            flo_song.set_music_brainz_id(music_brainz_id)
            self.song_list[str(request_id)].append(flo_song)
