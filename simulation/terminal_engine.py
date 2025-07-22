from game.hanabi_game import HanabiGame, Action, ActionType, HintType

def get_valid_player_count():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            print("Player count must be between 2 and 5")
        except ValueError:
            print("Please enter a valid number")

def main():
    # Get player count and initialize game
    n_players = get_valid_player_count()
    game = HanabiGame(n_players)
    
    # Main game loop
    while not game.is_game_over():
        current_player = game.current_player_index
        print(f"\nPlayer {current_player}'s turn")
        print(game.status(current_player))

        # Wait for player input
        action = [c for c in input("Enter your action: ").split(" ")]
        print(f"Action received: {action}")
        if action[0] == "P":#ex: P 2 plays card at index 2
            card_index = int(action[1])
            action = Action(ActionType.PLAY_CARD, player_index = current_player, card_index = card_index)
        elif action[0] == "D":#ex: D 3 discards card at index 3
            card_index = int(action[1])
            action = Action(ActionType.DISCARD_CARD, player_index = current_player, card_index = card_index)
        elif action[0] == "H":
            #ex: H 1 C red gives hint to player 1 about colour red
            #ex: H 3 N 4 gives hint to player 3 about number 4
            target_player = int(action[1])
            hint_type = action[2]
            if hint_type == "C":
                hint_colour = action[3]
                action = Action(
                    ActionType.GIVE_HINT, 
                    player_index = current_player, 
                    target_player_index = target_player, 
                    hint_type=HintType.COLOUR, 
                    hint_value=hint_colour)
            elif hint_type == "N":
                hint_number = int(action[3])
                action = Action(
                    ActionType.GIVE_HINT, 
                    player_index = current_player, 
                    target_player_index = target_player, 
                    hint_type=HintType.NUMBER, 
                    hint_value=hint_number)
        elif action[0] == "L":
            print("Current game log:")
            print(game.log)
            continue
        else:
            print("Invalid action. Use P <card_index>, D <card_index>, or H <target_player> <C/N> [<colour/number>]")
            continue

        try:
            game.apply_action(action)
        except Exception as e:
            print(f"Error applying action: {e}\n")
            print(f"Try again with a valid action.\n")
    print("Game over!")
    print(f"Final score: {game.get_score()}")
    print("Game log:")
    print(game.log)


if __name__ == "__main__":
    while True:
        main()