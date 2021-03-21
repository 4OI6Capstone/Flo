from utils.transistion.CrossFade import CrossFade
from utils.transistion.Tempo import Tempo
from utils.transistion.Loopout import Loopout

transition_thresholds = {
    Tempo: {
        'bpm_threshold': 20,
        'danceability_threshold': 0.2,
        'loudness_threshold': 0.2
    },
    CrossFade: {
        'bpm_threshold': 100,
        'danceability_threshold': 1,
        'loudness_threshold': 0.1
    },
    Loopout: {
        'bpm_threshold': 40,
        'danceability_threshold': 1,
        'loudness_threshold': 1
    }
}


