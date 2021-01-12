from abc import ABC, abstractmethod


class Transition(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def apply(self, prev_song, next_song, **kwargs):
        pass
