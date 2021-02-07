from pydub import AudioSegment
from pydub import scipy_effects


def loop_out(incoming_song, curr_song, bar_time, bar_end_time,low_pass_cut_off, high_pass_cut_off, half_repeat = 4, quarter_repeat = 4):
    curr_song_stripped = curr_song[:bar_time]
    curr_song_bar = curr_song[bar_time:bar_end_time]
    bar_length = bar_end_time - bar_time
    curr_bar_half = curr_song_bar[:bar_length/2]
    curr_bar_quarter = curr_song_bar[:bar_length/4]
    for i in range(4):
        if i == 0:
            result = curr_song_bar
        else:
            result = result.append(curr_song_bar)
    for i in range(4):
        result = result.append(curr_bar_half)
    for i in range(4):
        result = result.append(curr_bar_quarter)
    result = scipy_effects.low_pass_filter(result, 3500, order = 1)
    overlap_duration = len(result)
    incoming_song_seg = incoming_song[:overlap_duration]
    incoming_song_seg = scipy_effects.low_pass_filter(incoming_song_seg,5600,order = 2)
    result = incoming_song_seg.overlay(result, gain_during_overlay = -5)

    result = result.append(incoming_song[overlap_duration:], crossfade = 100)
    output = curr_song_stripped.append(result,crossfade=500)
    return output

