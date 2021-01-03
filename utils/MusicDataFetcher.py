import musicbrainzngs
import requests

acousticbrainz_url = "https://acousticbrainz.org"
musicbrainzngs.set_useragent("McMaster 4OI6 Capstone Project", "0.1",
                             "https://github.com/4OI6Capstone/Flo")


def find_music_brainz_id_by_recording(flo_song):
    song_artists = flo_song.artist
    song_titles = flo_song.title
    for song_title in song_titles:
        for song_artist in song_artists:
            # Make a request to music brainz to find all recordings found for this artist and title
            result = musicbrainzngs.search_recordings(artist=song_artist, recording=song_title)
            # Loop through results and probe the acoustic brainz library
            for entry in result['recording-list']:
                temp_id = entry['id']
                request_url = "{}/{}/{}".format(acousticbrainz_url, temp_id, "low-level")
                # Probe request
                response = requests.get(request_url)
                # Return id if response is ok
                if response.ok:
                    return temp_id
                else:
                    continue


# Acoustic Brainz Request, default set to high level
def get_acoustic_brainz_data(music_brainz_id, level="high-level"):
    request_url = "{}/{}/{}".format(acousticbrainz_url, music_brainz_id, level)
    try:
        response = requests.get(request_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errhttp:
        print("Http Error:", errhttp)
    except requests.exceptions.ConnectionError as errconnection:
        print("Error Connecting:", errconnection)
    except requests.exceptions.Timeout as errtimeout:
        print("Timeout Error:", errtimeout)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    return response.json()
