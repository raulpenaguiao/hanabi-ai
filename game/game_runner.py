# game_runner.py
from game.hanabi_game import HanabiGame
from agents.players import Players  # abstract base class

def run_game(players: 'Players', verbose=False):
    game = HanabiGame(num_players=players.num_players)
    while not game.is_game_over():
        current_player = game.current_player_index
        action = players.get_action(game, current_player)
        game_step_results = game.step(action, current_player)
        players.update_state(game_step_results, current_player)
        if verbose:
            print(f"Turn {game.turn_count}: Player {current_player} -> {action}")
    return game.get_score()

# Example usage
if __name__ == "__main__":
    from agents.random_player import RandomPlayers
    players = RandomPlayers(4)
    score = run_game(players, True)
    print(f"Final score: {score}")
    
    #from agents.naive_players import NaivePlayers
    #players = NaivePlayers(4)
    #run_game(players, True)