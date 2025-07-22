import random
from ..game.hanabi_game import HanabiGame, 

class RandomPlayers:
    def __init__(self, num_players):
        self.num_players = num_players
        pass

    def update_state(self, game_state):
        """
        Update the internal state of the player based on the game state.
        This method should be called at the start of each turn.
        """
        pass

    def get_action(self, hanabi_game: HanabiGame):
        """
        Plays an action randomly
        """
        action = random.randint(1, 3)
        if action == 1:
            # Play a card
            card_index = random.choice(range(len(hanabi_game.cards_in_players_hands[hanabi_game.current_player_index])))
            return hanabi_game.PlayCardAction(card_index)
        elif action == 2:
            # Discard a card
            card_index = random.choice(range(len(hanabi_game.cards_in_players_hands[hanabi_game.current_player_index])))
            return hanabi_game.DiscardCardAction(card_index)
        else:
            # Give a hint
            target_player = random.choice([i for i in range(hanabi_game.num_players) if i != hanabi_game.current_player_index])
            hint_type = random.choice(['colour', 'number'])
            if hint_type == 'colour':
                hint_colour = random.choice(hanabi_game.COLOURS)
                return hanabi_game.GiveHintAction(target_player, hint_colour=hint_colour)
            else:
                hint_number = random.choice(hanabi_game.CARDS_PER_COLOUR)
                return hanabi_game.GiveHintAction(target_player, hint_number=hint_number)


