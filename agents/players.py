# agents/base.py
from abc import ABC, abstractmethod

class Players(ABC):
    def __init__(self, num_players):
        self.num_players = num_players

    @abstractmethod
    def update_state(self, game_state):
        pass

    @abstractmethod
    def get_action(self, hanabi_game):
        pass
