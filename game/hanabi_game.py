from random import shuffle
from enum import Enum

class ActionType(Enum):
    PLAY_CARD = "play_card"
    DISCARD_CARD = "discard_card"
    GIVE_HINT = "give_hint"

class HintType(Enum):
    COLOUR = "colour"
    NUMBER = "number"

class Action:
    def __init__(self, action_type: ActionType, player_index: int = None, card_index: int = None, hint_type: HintType = None, hint_value: int = None, target_player_index: int = None):
        self.type = action_type
        self.player_index = player_index
        self.str = f"{action_type} {player_index}"
        if self.type == ActionType.PLAY_CARD or self.type == ActionType.DISCARD_CARD:
            if card_index is None:
                raise ValueError("Card index must be provided for play or discard actions.")
            if card_index < 0:
                raise ValueError("Card index must be non-negative.")
            self.card_index = card_index
            self.str += f" {card_index}"
        if self.type == ActionType.GIVE_HINT:
            if hint_value is None:
                raise ValueError("Hint value must be provided for give hint actions.")
            if hint_type is None:
                raise ValueError("Hint type must be provided for give hint actions.")
            if target_player_index is None:
                raise ValueError("Target player must be provided for give hint actions.")
            self.hint_type = hint_type
            self.hint_value = hint_value
            self.target_player_index = target_player_index
            self.str += f" {hint_type.value} {hint_value} {target_player_index}"

    def __repr__(self):
        return self.str

class CardState(Enum):
    IN_DECK = "IN DECK"
    PLAYER_0_HAND = "PLAYER 0 HAND"
    PLAYER_1_HAND = "PLAYER 1 HAND"
    PLAYER_2_HAND = "PLAYER 2 HAND"
    PLAYER_3_HAND = "PLAYER 3 HAND"
    PLAYER_4_HAND = "PLAYER 4 HAND"
    BOARD = "BOARD"
    DISCARD = "DISCARD"

    def CardStateInPlayerHand(player: int):
        if player == 0:
            return CardState.PLAYER_0_HAND
        elif player == 1:
            return CardState.PLAYER_1_HAND
        elif player == 2:
            return CardState.PLAYER_2_HAND
        elif player == 3:
            return CardState.PLAYER_3_HAND
        elif player == 4:
            return CardState.PLAYER_4_HAND
        else:
            raise ValueError("Invalid player index. Must be between 0 and 4.")

class HanabiGame:
    """
    Represents the Hanabi game state and logic.
    Initializes the game with a specified number of players.
    
    Args:
        num_players (int): Number of players in the game (2-5).
    
    Raises:
        ValueError: If the number of players is not between 2 and 5.

    Attributes:
        NUM_PLAYERS (int): Number of players in the game.
        COLOURS (list): List of colours used in the game.
        CARDS_PER_COLOUR (list): Distribution of cards per colour.
        CARDS_PER_PLAYER (int): Number of cards each player starts with.
        deck (list): The deck of cards used in the game.
        NUM_CARDS_IN_DECK (int): Total number of cards in the deck.
        playstate (dict): Dictionary mapping card indices to their state.
        current_player_index (int): Index of the player whose turn it is.
        turn_count (int): Count of turns taken in the game.
        current_top_card (int): Index of the next card to be drawn from the deck.
        log (str): Log of game actions and events.
        hints_available (int): Number of hints available to give.
        lives (int): Number of lives remaining in the game.
        board (dict): Current state of the board, mapping colours to their played counts.
        last_round (str): Last round played, used for logging.
    
    Methods:
        apply_action(action: Action): Applies the given action to the game state.
        apply_action_play(player_index: int, card_index_in_hand: int): Plays a card from the player's hand.
        apply_action_discard(player_index: int, card_index_in_hand: int): Discards a card from the player's hand.
        apply_action_hint(target_player: int, hint_type: str, hint_value: str): Gives a hint to the specified player.
        draw_new_card(player_index: int): Draws a new card for the player if the deck is not empty.
        pass_turn(): Passes the turn to the next player.
        is_deck_empty(): Checks if the deck is empty.
        is_game_over(): Checks if the game is over based on lives, board state, and deck state.
        get_score(): Returns the current score based on the board state.
    """
    def __init__(self, num_players: int):
        if num_players < 2 or num_players > 5:
            raise ValueError("Number of players must be between 2 and 5.")
        # initialize deck, players, tokens, board
        self.NUM_PLAYERS = num_players
        self.COLOURS = ['red', 'green', 'blue', 'yellow', 'white']
        self.CARDS_PER_COLOUR = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]  # Distribution of cards per color
        self.CARDS_PER_PLAYER = 5  # Number of cards each player starts with
        if num_players > 3:
            self.CARDS_PER_PLAYER = 4  # Adjust for more players
        self.deck = [(colour, number) for colour in self.COLOURS for number in self.CARDS_PER_COLOUR]
        self.NUM_CARDS_IN_DECK = len(self.deck)
        
        self.playstate = {i: CardState.IN_DECK for i in range(len(self.deck))}
        self.hints = {i:[] for i in range(len(self.deck))}  # Hints for each card index
        self.current_player_index = 0  # Index of the player whose turn it is
        self.turn_count = 0  # Count of turns taken
        self.current_top_card = 0
        self.log = ""

        #shuffle the deck
        shuffle(self.deck)

        #deal cards to players
        self.cards_in_players_hands = [[] for _ in range(self.NUM_PLAYERS)]
        for player_index in range(self.NUM_PLAYERS):
            for _ in range(self.CARDS_PER_PLAYER):
                if self.deck:
                    card_index = self.current_top_card
                    self.current_top_card += 1
                    card = self.deck[card_index]
                    self.log += f"Player {player_index} received card {card} with index = {card_index}\n"
                    self.cards_in_players_hands[player_index].append(card_index)
                    self.playstate[card_index] = CardState.CardStateInPlayerHand(player_index)
        
        self.MAX_HINTS = 8
        self.hints_available = 8  # Initial hints available
        self.lives = 3  # Initial lives
        self.board = {colour: 0 for colour in self.COLOURS}  # Board
        self.discard = {colour: [] for colour in self.COLOURS}  # Discard pile
        self.last_round = self.log  # Last round played
        pass

    def apply_action(self, action: Action):
        """
        Changes the state of the game according to the action taken by the player.
        """
        self.last_round = ""
        if self.is_game_over():
            raise ValueError("Game is already over. Cannot apply action.")

        if action.type == ActionType.PLAY_CARD:
            self.apply_action_play(action.player_index, action.card_index)
        elif action.type == ActionType.DISCARD_CARD:
            self.apply_action_discard(action.player_index, action.card_index)
        elif action.type == ActionType.GIVE_HINT:
            self.apply_action_hint(action.player_index, action.target_player_index, action.hint_type, action.hint_value)

        self.log += f"Player {action.player_index} action: {action}\n"
        self.pass_turn()
        pass
    
    def apply_action_hint(self, player_index :int, target_player: int, hint_type: str, hint_value: str):
        """
        Gives the hint for the specified player, of hint type and value.
        """
        print(f"Hint given to player {target_player}: {hint_type} {hint_value}")
        if hint_type not in [HintType.COLOUR, HintType.NUMBER]:
            raise ValueError("Hint type must be 'colour' or 'number'.")
        if hint_value not in self.COLOURS and hint_type == HintType.COLOUR:
            raise ValueError(f"Invalid colour: {hint_value}. Must be one of {self.COLOURS}.")
        if hint_value not in self.CARDS_PER_COLOUR and hint_type == HintType.NUMBER:
            raise ValueError(f"Invalid number: {hint_value}. Must be one of {self.CARDS_PER_COLOUR}.")
        if self.hints_available <= 0:
            raise ValueError("No hints available to give.")
        if target_player == player_index:
            raise ValueError("Cannot give hint to yourself.")

        self.hints_available -= 1
        hint = []
        
        if hint_type == HintType.COLOUR:
            # Provide a colour hint
            for index, card_index in enumerate(self.cards_in_players_hands[target_player]):
                card = self.deck[card_index]
                if card[0] == hint_value:
                    # Update the player's hand with the hint
                    hint.append(index)
                    self.hints[card_index].append(str(hint_value))
                else:
                    self.hints[card_index].append("N-" + str(hint_value))
        elif hint_type == HintType.NUMBER:
            # Provide a number hint
            for index, card_index in enumerate(self.cards_in_players_hands[target_player]):
                card = self.deck[card_index]
                if card[1] == hint_value:
                    hint.append(index)
                    # Update the player's hand with the hint
                    self.hints[card_index].append(str(hint_value))
                else:
                    self.hints[card_index].append("N-" + str(hint_value))
        self.log += f"Hint given to player {target_player}: {hint_type} {hint_value} at indices [{hint}]\n"
        return hint

    def apply_action_play(self, player_index: int, card_index_in_hand: int):
        """
        Validates input
        Takes a card from the player's hand and plays it on the board.
        If the card fits the board, increases the card count for that colour.
        If the card does not fit, it loses a life.
        The status of the card is updated in playstate, to BOARD or DISCARD respectively.
        If there are cards available in the deck, it draws a new card. Current top card is incremented.
        Else it does not draw a new card.
        """
        #Verify input
        if player_index < 0 or player_index >= self.NUM_PLAYERS:
            raise ValueError("Invalid player index.")
        if card_index_in_hand < 0 or card_index_in_hand >= len(self.cards_in_players_hands[player_index]):
            raise ValueError("Invalid card index.")
        
        #Get the card from the player's hand
        card_index = self.cards_in_players_hands[player_index][card_index_in_hand]
        card = self.deck[card_index]

        # Check if the card can be played
        if self.board[card[0]] + 1 == card[1]:
            # Valid play
            self.board[card[0]] += 1
            self.playstate[card_index] = CardState.BOARD
            self.log += f"Player {player_index} played card {card}\n"
        else:
            # Invalid play, lose a life
            self.lives -= 1
            self.playstate[card_index] = CardState.DISCARD
            self.log += f"Player {player_index} played card {card} incorrectly. Lives left: {self.lives}\n"
        
        #Remove the card from the player's hand
        del self.cards_in_players_hands[player_index][card_index_in_hand]

        # If there are cards left in the deck, draw a new card
        self.draw_new_card(player_index)
        pass
        
    def draw_new_card(self, player_index: int):
        """
        Draws a new card for the player if the deck is not empty.
        """
        if not self.is_deck_empty():
            self.cards_in_players_hands[player_index].append(self.current_top_card)
            self.playstate[self.current_top_card] = CardState.CardStateInPlayerHand(player_index)
            self.log += f"Player {player_index} drew a new card = {self.deck[self.current_top_card - 1]}. Current top card index: {self.current_top_card - 1}\n"
            self.last_round += f"Player {player_index} drew a new card = {self.deck[self.current_top_card - 1]}. Current top card index: {self.current_top_card - 1}\n"
            self.current_top_card += 1
        pass

    def apply_action_discard(self, player_index: int, card_index_in_hand: int):
        """
        Validates input
        Updates the playstate of the card to DISCARD.
        Discards a card from the player's hand.
        Draws a new card if there are cards left in the deck.
        """
        #Validate input
        if player_index < 0 or player_index >= self.NUM_PLAYERS:
            raise ValueError("Invalid player index.")
        if card_index_in_hand < 0 or card_index_in_hand >= len(self.cards_in_players_hands[player_index]):
            raise ValueError("Invalid card index.")
        
        #Get the card from the player's hand
        card_index = self.cards_in_players_hands[player_index][card_index_in_hand]
        card = self.deck[card_index]
        
        self.playstate[card_index] = CardState.DISCARD
        if self.hints_available < self.MAX_HINTS:
            self.hints_available += 1
        self.log += f"Player {player_index} discarded card {card}.\n"
        
        #Remove the card from the player's hand
        del self.cards_in_players_hands[player_index][card_index_in_hand]

        # If there are cards left in the deck, draw a new card
        self.draw_new_card(player_index)
        pass

    def pass_turn(self):
        """
        Passes the turn to the next player.
        """
        self.current_player_index = (self.current_player_index + 1) % self.NUM_PLAYERS
        self.turn_count += 1
        self.log += f"Turn passed to player {self.current_player_index}\n"

    def is_deck_empty(self):
        """
        Checks if the deck is empty.
        """
        return self.current_top_card >= self.NUM_CARDS_IN_DECK
    
    def is_game_over(self):
        if self.lives <= 0:
            return True
        if all([self.board[colour] == max(self.CARDS_PER_COLOUR) for colour in self.COLOURS]):
            return True
        if not self.is_deck_empty():
            return False
        if all([len(hand) == self.CARDS_PER_PLAYER - 1 for hand in self.cards_in_players_hands]):
            return True
        return False

    def get_score(self):
        """
        Returns the current score based on the board state.
        """
        return sum(self.board.values())

    def status(self, player_index: int):
        """
        Returns the status of the game from the point of view of a specified player.
        """
        status = f"Player {player_index} status:\n"
        status += f"Current player index: {self.current_player_index}\n"
        status += f"Turn count: {self.turn_count}\n"
        status += f"Current top card index: {self.current_top_card}\n"
        status += f"Hints available: {self.hints_available}\n"
        status += f"Lives remaining: {self.lives}\n"
        status += f"Board state: {self.board}\n"
        status += f"Discard pile: {self.discard}\n"
        status += f"Cards in hand of other players:\n"
        for i in range(self.NUM_PLAYERS):
            if not i == player_index:
                status += f"Player {i}: {[self.deck[card_index] for card_index in self.cards_in_players_hands[i]]}\n"
        status += f"Hinted cards in hand of other players:\n"
        for i in range(self.NUM_PLAYERS):
            status += f"Player {i}: {[self.hints[card_index] for card_index in self.cards_in_players_hands[i]]}\n"

        status += f"Game log last round:\n{self.last_round}\n"
        return status
