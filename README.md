# 🧭 Maze Explorer Agent — A* Pathfinding Visualizer

An interactive, real-time visualization of the **A\* (A-Star)** pathfinding algorithm built with **Python** and **Pygame**. Watch the agent intelligently explore a randomly generated maze and find the shortest path from start to goal.

---

## ✨ Features

- 🗺️ **Random Maze Generation** — a new solvable maze is generated every run (or on demand)
- 🔍 **Real-time A\* Visualization** — see the open/closed sets expand step by step
- 🏆 **Optimal Path Reconstruction** — the shortest path is highlighted in gold once found
- 🎮 **Interactive Controls** — trigger the algorithm or regenerate the maze with a single key press
- 🎨 **Color-coded Grid** — each cell state has a distinct, readable color

---

## 🖼️ Color Legend

| Color | Meaning |
|---|---|
| 🔵 Blue | Start node |
| 🟣 Violet | End / Goal node |
| 🟡 Gold | Optimal path |
| 🟢 Light Green | Open set (frontier being explored) |
| 🔴 Tomato Red | Closed set (already explored) |
| ⬜ Smoke White | Free cell |
| 🟫 Dark Gray | Wall / obstacle |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [Pygame](https://www.pygame.org/)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/maze_explorer_agent.git
cd maze_explorer_agent

# Create and activate a virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\activate.bat      # Windows
source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install pygame
```

### Run

```bash
python main.py
```

---

## 🎮 Controls

| Key | Action |
|---|---|
| `SPACE` | Run the A\* algorithm on the current maze |
| `R` | Generate a new random maze and reset |
| ✖ Window close | Quit the application |

---

## 🧠 How It Works

The agent uses the **A\* search algorithm**, which finds the shortest path by minimising:

```
f(n) = g(n) + h(n)
```

| Term | Description |
|---|---|
| `g(n)` | Cost from the **start** node to node `n` |
| `h(n)` | Heuristic estimate from `n` to the **goal** (Manhattan distance) |
| `f(n)` | Total estimated cost through node `n` |

The **Manhattan distance** heuristic is used since movement is restricted to 4 directions (up, down, left, right), making it both admissible and consistent.

---

## 📁 Project Structure

```
maze_explorer_agent/
├── README.md
├── main.py                 # Core entry point (initializes Pygame and runs the main loop)
└── src/
    ├── __init__.py
    ├── config.py           # Screen dimensions, settings, and color palettes
    ├── node.py             # Nodo class representing grid cells and their states
    ├── grid.py             # Grid creation and management functions
    ├── astar.py            # A* search algorithm, Manhattan heuristic, and path reconstruction
    ├── maze_gen.py         # Maze generation algorithms (currently random walls)
    └── renderer.py         # Pygame drawing functions for rendering grid and nodes
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
