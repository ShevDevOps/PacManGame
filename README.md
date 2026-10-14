# Pac-Man Arcade Engine

[![Python application](https://github.com/ShevDevOps/PacManGame/actions/workflows/python-app.yml/badge.svg)](https://github.com/ShevDevOps/PacManGame/actions/workflows/python-app.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modular desktop implementation of the classic 1980 arcade game built with **Python 3** and **Pygame**. Focused on clean object-oriented architecture, discrete tile-grid navigation, ghost state machines, and thorough test coverage.

---

## Features & Architecture

* **Ghost AI State Machine:** Each ghost operates across distinct states (`NORMAL`, `SCARED`, `EATEN`, `AFTER_EATEN`) with dynamic target re-routing and return-to-pen logic upon defeat.
* **Discrete Tile Map System:** ASCII-based level map parser (`#` walls, `D` dots, `P` power pills, `G` ghost gates) mapping continuous sprite velocities to a discrete collision grid.
* **Game Mechanics:**
  * Power pills trigger ghost vulnerability mode with reverse target behavior.
  * Score multipliers for consecutive ghost consumption and cherry bonus pickups.
  * Level progression upon clearing all dots and power pellets.
* **Menu & Persistence:** Interactive start/pause screens, settings configuration, and local leaderboard powered by `pygame-menu`.

---

## Controls

| Key | Action |
|:---:|:---|
| **W** | Move Up |
| **S** | Move Down |
| **A** | Move Left |
| **D** | Move Right |
| **ESC** | Pause / Back to Menu |

---

## Installation & Running

### Requirements
* Python 3.10 or higher
* `pip`

### Quick Start
```bash
# Clone the repository
git clone https://github.com/ShevDevOps/PacManGame.git
cd PacManGame

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

---

## Testing & Quality Assurance

The codebase includes an extensive suite of **164 unit tests** covering collision mechanics, state transitions, leaderboard operations, and resource loaders.

```bash
# Run test suite
pytest

# Run tests with coverage
pytest --cov=.
```

All pushes and pull requests are validated via **GitHub Actions** (`python-app.yml`), running static linting with `flake8` and executing the full `pytest` suite on Ubuntu runners.
