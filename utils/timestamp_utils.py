import audioowl
import librosa
import numpy as np
from pydub import AudioSegment
from pydub.utils import which
import time
from random import randint


def find_best_sync_point(bottom_file_beats, top_file_beats, max_mix_sample, offset, mode):

    offset = offset
    matches_per_round = []

    # turning args to numpy arrays
    bottom_file_beats = np.array(bottom_file_beats)
    top_file_beats = np.array(top_file_beats)

    for rn in range(bottom_file_beats.shape[0]):

        try:

            zero_sync_samples = bottom_file_beats[rn] - top_file_beats[0]
            slider = top_file_beats + (zero_sync_samples)

            for i in range(len(slider)):
                if slider[i] <= max_mix_sample:
                    continue
                else:
                    slider[i] = slider[i] - max_mix_sample

            matches = []
            tested_beat_index = 0
            all_sample_beats = np.concatenate((slider, bottom_file_beats))
            all_sample_beats.sort()

            for i in range (1, all_sample_beats.shape[0]):
                if all_sample_beats[i] == all_sample_beats[tested_beat_index] or abs(all_sample_beats[i] - all_sample_beats[tested_beat_index]) <= offset:
                    matches.append(all_sample_beats[i])
                    matches.append(all_sample_beats[tested_beat_index])
                    tested_beat_index+=1

                else:
                    tested_beat_index+=1

            matches_per_round.append(len(matches)/2/len(top_file_beats))

        except Exception as err:
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            # print ('\t🔎  We had a sliding window problem :|\n\tError message: {}\n\tError on file: {}\n\tError on line: {}\n'.format(err, exc_traceback.tb_frame.f_code.co_filename, exc_traceback.tb_lineno))
            matches_per_round.append(0)

    if mode == 'first':
        sync_beat_number = np.argmax(matches_per_round)

    else: # random (default)
        sync_beat_number = np.random.choice(np.argwhere(matches_per_round == np.amax(matches_per_round)).reshape(-1,))

    sync_sample = bottom_file_beats[sync_beat_number] - top_file_beats[0]
    sync_beat_accuracy = np.max(matches_per_round)

    return sync_sample, sync_beat_number, sync_beat_accuracy