from agents.players import Players  # abstract base class
from game.game_runner import run_game
import time

# Example usage
if __name__ == "__main__":
    from agents.random_player import RandomPlayers
    players = RandomPlayers(4)
    SCORES = []
    RUN_NUMBER = 2**14  # 16384 games
    print(f"Running {RUN_NUMBER} games with random players...")
    for i in range(RUN_NUMBER):
        #print(f"Game {i+1}")
        SCORES += [run_game(players, False)]
    print(f"Final score: {sum(SCORES) / RUN_NUMBER}")
    import matplotlib.pyplot as plt
    plt.hist(SCORES, bins=30)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Hanabi Scores for Random Players in {RUN_NUMBER} Games')
    timestamp = int(time.time())
    plt.savefig(f'plots/plot_hanabiscores_randomplayers{timestamp}.png')
    plt.close()
    