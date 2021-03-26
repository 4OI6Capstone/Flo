from utils.transistion.CrossFade import CrossFade
from utils.transistion.Tempo import Tempo
from utils.transistion.Loopout import Loopout
from utils.transistion.LoopIn import LoopIn
from utils.transistion.SeamlessFade import SeamlessFade

transition_thresholds = {
    Tempo: {
        'bpm_threshold': 20,
        # 'danceability_threshold': 0.2,
        # 'loudness_threshold': 0.2,
        'dynamic_complexity': 0.5
    },
    SeamlessFade: {
        'bpm_threshold': 50,
        # 'danceability_threshold': .5,
        # 'loudness_threshold': .5,
        'dynamic_complexity': 0.5
    }
}
""",    
    CrossFade: {
        'bpm_threshold': 100,
        # 'danceability_threshold': 1,
        # 'loudness_threshold': 0.1,
        'dynamic_complexity': 0.5
    },
    Loopout: {
        'bpm_threshold': 40,
        'danceability_threshold': 1,
        'loudness_threshold': 1,
        'dynamic_complexity': 0.5
    },
    LoopIn: {
        'bpm_threshold' : 30,
        'danceability_threshold': .8,
        'loudness_threshold': .5,
        'dynamic_complexity': 0.5
    }
"""


