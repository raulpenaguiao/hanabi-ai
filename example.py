from game.hanabi_game import HanabiGame
from agents.players import Players  # abstract base class
from game.game_runner import run_game

# Example usage
if __name__ == "__main__":
    from agents.random_player import RandomPlayers
    players = RandomPlayers(4)
    score = run_game(players, True)
    print(f"Final score: {score}")
    
    #from agents.naive_players import NaivePlayers
    #players = NaivePlayers(4)
    #run_game(players, True)