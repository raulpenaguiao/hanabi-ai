class HanabiGame:
    def __init__(self, num_players: int):
        # initialize deck, players, tokens, board
        pass

    def get_observation(self, player_index: int):
        # returns what this player can see
        pass

    def apply_action(self, player_index: int, action):
        # apply action, update game state, return reward
        pass

    def is_game_over(self):
        pass

    def get_score(self):
        pass
