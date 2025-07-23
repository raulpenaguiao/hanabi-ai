import random
from game.hanabi_game import HanabiGame, HanabiGameState, Action, ActionType, HintType

class RandomPlayers:
    def __init__(self, num_players):
        self.num_players = num_players
        pass

    def update_state(self, game_state: HanabiGameState, current_player_index: int):
        """
        Update the internal state of the player based on the game state.
        This method should be called at the start of each turn.
        """
        pass

    def get_action(self, hanabi_game: HanabiGame, current_player_index: int):
        """
        Plays an action randomly
        """
        if hanabi_game.hints_available <= 0:
            # If no hints are available, randomly choose to play or discard a card
            action_type = random.choice([ActionType.PLAY_CARD, ActionType.DISCARD_CARD])
        else:
            action_type = random.choice([ActionType.PLAY_CARD, ActionType.DISCARD_CARD, ActionType.GIVE_HINT])
        if action_type == ActionType.PLAY_CARD:
            # Play a card
            card_index = random.choice(range(len(hanabi_game.cards_in_players_hands[current_player_index])))
            return Action(action_type, player_index=current_player_index, card_index=card_index)
        elif action_type == ActionType.DISCARD_CARD:
            # Discard a card
            card_index = random.choice(range(len(hanabi_game.cards_in_players_hands[current_player_index])))
            return Action(action_type, player_index=current_player_index, card_index=card_index)
        elif action_type == ActionType.GIVE_HINT:
            # Give a hint
            target_player = random.choice([i for i in range(hanabi_game.NUM_PLAYERS) if i != current_player_index])
            hint_type = random.choice([HintType.COLOUR, HintType.NUMBER])
            if hint_type == HintType.COLOUR:
                hint_colour = random.choice(hanabi_game.COLOURS)
                return Action(action_type, player_index=current_player_index, target_player_index=target_player, hint_type=HintType.COLOUR, hint_value=hint_colour)
            elif hint_type == HintType.NUMBER:
                hint_number = random.choice(hanabi_game.CARDS_PER_COLOUR)
                return Action(action_type, player_index=current_player_index, target_player_index=target_player, hint_type=HintType.NUMBER, hint_value=hint_number)
            else:
                raise ValueError("Unknown hint type selected")
        else:
            raise ValueError("Unknown action type selected")

