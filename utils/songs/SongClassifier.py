from ..songs import Song
import mutagen
from utils.MusicDataFetcher import MusicDataFetcher


class SongClassifier:
    song_list = []

    def __init__(self, song_list):
        self.song_list = song_list

    def deconstruct_songs(self, song_list):
        music_data_fetcher = MusicDataFetcher()
        for file in song_list:
            song = mutagen.File(file, easy=True)
            artist = song.get('artist')
            title = song.get('title')
            album = song.get('album')
            flo_song = Song(artist, title, album)
            flo_song.set_music_brainz_id(music_data_fetcher.
                                         find_music_brainz_id(flo_song))
            self.song_list.append(song_list)
