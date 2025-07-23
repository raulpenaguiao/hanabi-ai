# Hanabi AI: Multi-Agent Reinforcement Learning

This project aims to train intelligent agents to cooperatively play the card game **Hanabi** using **reinforcement learning** and **recurrent neural networks (RNNs)**. Each agent learns to remember game history and act based on partial information—just like real Hanabi players.

## 🎯 Project Goals

- Build a game engine that simulates Hanabi for 2–5 players.
- Use RNN-based agents to model memory and sequence of actions.
- Train each agent group independently using reinforcement learning.
- Allow simulation and logging of played games to verify behavior.

---

## 📁 Project Structure

hanabi-ai/

├── agents/

│   |── players.py             # Abstract players class for agents

│   |── player\_set.py         # Defines agent logic and neural models (TODO)

│   |── naive\_player.py       # Defines agent logic for a naive player

│   └── random\_player.py      # Defines agent logic for a random player

├── game/

│   |── hanabi\_game.py        # Game engine with Hanabi rules

│   └── game\_runner.py        # Takes a Players instance and runs the game

├── plots/                     # Generated plots from training and evaluation

├── simulation/

│   |── simulation\_runner.py  # Simulates many games for training

│   └── terminal\_engine.py    # Simulates one game that can be played in the terminal

├── statistics_for_players/

│   └── randomPlayer.py        # Analyzes performance of random player over $2^14$ games

├── training/

│   └── train.py               # Trains models via reinforcement learning

└── README.md


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/raulpenaguiao/hanabi-ai.git
cd hanabi-ai
````

### 2. Install Dependencies

Make sure you have Python 3.8+ and install required packages:

```bash
pip install torch numpy
```

---

## 🧩 Game Engine Overview

The game engine is located in `game/hanabi_game.py` and provides a full simulation of the Hanabi game mechanics.

### Core Classes

- **`ActionType`**: An enum with the three action types:
  - `ActionType.Hint`
  - `ActionType.Discard`
  - `ActionType.Play`

- **`Action`**: A wrapper for player moves.
  - Initialized with `ActionType`, `player_index`, and:
    - For `Hint`: `target_index`, `hint_type`, `hint_value`
    - For `Play` or `Discard`: `card_index`
  - Includes validation and utility methods.

- **`HanabiGame`**: Main game engine.
  - `step(action: Action)`: Applies an action, raises error if invalid.
  - `is_game_over()`: Returns whether the game has ended.
  - `get_score()`: Computes the current score.
  - `get_info(player_index: int)`: Returns what the given player can legally observe and remember.
  - `get_legal_actions()`	Let agents query what actions are valid.
  - `get_current_player()`:	Get's index of current player.
  - `clone()`: Returns a deep copy of the game for simulations.
  - `render(mode='text')`: Helpful for debugging or saving games visually/logically.


This API supports agents interacting with the game through valid, structured moves and receiving player-legal feedback.


---

## 🧠 Training the Agents

Train the agents for a specific number of players (e.g. 2-player):

```bash
python training/train.py --players 2 --episodes 10000 --output param.json
```

This will save the trained model parameters into a file called `param.json`.

---

## 🎮 Simulate a Game with Trained Agents

Once trained, you can watch a game being played and log the result:

```bash
python play/play.py param.json > game.txt
```

This prints the game's progression (moves, hints, discards, scores) to `game.txt`.

---

## 📊 Results

Running the scripts on the directory `statistics_for_players` produces performance plots.
You can find the generated plots in the `plots/` directory. These plots visualize the distribution of scores for the random players across all games.

For instance, for the agent that plays randomly, you can run:
```bash
python3 -m statistics_for_players.randomPlayer
```


---

## 🛠️ Notes

* Each player count (2, 3, 4, 5) should be trained separately.
* The game engine is fully custom—no external environments used.
* Agents use GRUs to track memory of previous moves.

---

## 📌 TODO

* Game printing and logging needs to be improved for better readability.
* Implement PPO-based training for more stable learning.
* Add GUI or CLI visualizer for game.txt logs.
* Benchmark performance across different agent architectures.

---

## 🤝 Contributing

PRs welcome! Feel free to suggest improvements, ideas, or issues.

---

## 📄 License

MIT License

