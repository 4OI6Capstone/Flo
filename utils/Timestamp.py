import audioowl
import librosa
import numpy as np
from pydub import AudioSegment
from pydub.utils import which
import time
from random import randint
from songs import Song
import Timestamp_utils as tu





s1 = Song()
s2 = Song()

#top_file represents the first music file that's being mixed and bottom_file represents the second song being brought in
def get_timestamp(s1, s2, sr=22050, mix_mode='random', offset=880, trim_silence=False):

    # loading the first song in the transition
    y_top_file, sr = librosa.load(s1.filename, sr=sr)

    if trim_silence:
        try:
            yt, i = librosa.effects.trim(y_top_file, top_db=28)

            # trimming only the leading silence
            y_top_file = y_top_file[i[0]:]
        except:
            pass

    # loading second song in the transition
    y_bottom_file, sr = librosa.load(s2.filename, sr=sr)

    # checking if the durations allow proper mixing
    y_bottom_file_repetitions = 1
    while (y_bottom_file.shape[0] * y_bottom_file_repetitions) < y_top_file.shape[0] :
        y_bottom_file_repetitions+=1

    # repeating y_bottom_file (second song in transition) if needed
    if (y_bottom_file_repetitions > 1):
        y_bottom_file_duplications = []
        for i in range(y_bottom_file_repetitions):
            y_bottom_file_duplications.append(y_bottom_file)
        y_bottom_file = np.hstack((y_bottom_file_duplications))


    # analyzing the files
    top_file_data = audioowl.analyze_samples(y_top_file, sr)
    bottom_file_data = audioowl.analyze_samples(y_bottom_file, sr)

    # find mixing point
    sync_sample, sync_beat_number, sync_beat_accuracy = tu.find_best_sync_point(
                                                        top_file_beats=top_file_data['beat_samples'],
                                                        bottom_file_beats=bottom_file_data['beat_samples'],
                                                        max_mix_sample=y_bottom_file.shape[0],
                                                        offset=offset,
                                                        mode=mix_mode)


    #calculate the timestamp
    sync_time_ms = sync_sample / sr * 1000


    return sync_time_ms

def get_timestamp_loop(s1, s2, sr=22050, mix_mode='random', offset=880, trim_silence=False,):

    # loading top file
    y_top_file, sr = librosa.load(s1.filename, sr=sr)

    if trim_silence:
        try:
            yt, i = librosa.effects.trim(y_top_file, top_db=28)

            # trimming only the leading silence
            y_top_file = y_top_file[i[0]:]
        except:
            print ('[MixingBear] Failed to trim leading silence')
            pass

    # loading bottom file
    y_bottom_file, sr = librosa.load(s2.filename, sr=sr)

    # checking if the durations allow proper mixing
    y_bottom_file_repetitions = 1
    while (y_bottom_file.shape[0] * y_bottom_file_repetitions) < y_top_file.shape[0] :
        y_bottom_file_repetitions+=1

    # repeating y_bottom_file if needed
    if (y_bottom_file_repetitions > 1):
        y_bottom_file_duplications = []
        for i in range(y_bottom_file_repetitions):
            y_bottom_file_duplications.append(y_bottom_file)
        y_bottom_file = np.hstack((y_bottom_file_duplications))


    # analyzing the files
    top_file_data = audioowl.analyze_samples(y_top_file, sr)
    bottom_file_data = audioowl.analyze_samples(y_bottom_file, sr)

    # find mixing point
    sync_sample, sync_beat_number, sync_beat_accuracy = tu.find_best_sync_point(
                                                        top_file_beats=top_file_data['beat_samples'],
                                                        bottom_file_beats=bottom_file_data['beat_samples'],
                                                        max_mix_sample=y_bottom_file.shape[0],
                                                        offset=offset,
                                                        mode=mix_mode)


    # mix the files
    sync_time_ms = sync_sample / sr * 1000

    return (sync_time_ms - ((4/(s1.bpm()/60))*1000))