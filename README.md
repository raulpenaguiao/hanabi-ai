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

│   └── player\_set.py       # Defines agent logic and neural models

├── game/

│   └── hanabi\_game.py      # Game engine with Hanabi rules

├── simulation/

│   └── simulation\_runner.py # Simulates many games for training

├── training/

│   └── train.py            # Trains models via reinforcement learning

├── play/

│   └── play.py             # Runs a single trained game and logs output

└── README.md


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/hanabi-ai.git
cd hanabi-ai
````

### 2. Install Dependencies

Make sure you have Python 3.8+ and install required packages:

```bash
pip install torch numpy
```

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

## 🛠️ Notes

* Each player count (2, 3, 4, 5) should be trained separately.
* The game engine is fully custom—no external environments used.
* Agents use GRUs to track memory of previous moves.

---

## 📌 TODO

* Implement PPO-based training for more stable learning.
* Add GUI or CLI visualizer for game.txt logs.
* Benchmark performance across different agent architectures.

---

## 🤝 Contributing

PRs welcome! Feel free to suggest improvements, ideas, or issues.

---

## 📄 License

MIT License

