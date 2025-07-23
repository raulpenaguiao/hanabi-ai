# agents/naive_player.py
from game.hanabi_game import Action, ActionType
from agents.players import Players

class NaivePlayers(Players):
    def update_state(self, game_state):
        self.game_state = game_state

    def get_action(self, hanabi_game):
        current_player = hanabi_game.current_player_index
        hand = self.game_state["hand"]

        # Naively: if we have hint tokens, always give a hint
        if hanabi_game.hint_tokens > 0:
            for target in range(hanabi_game.num_players):
                if target != current_player:
                    return Action(ActionType.Hint, current_player,
                                  target_index=target, hint_type="number", hint_value=1)

        # Otherwise, just play the first card
        return Action(ActionType.PLAY_CARD, current_player, card_index=0)
