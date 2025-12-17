# Project: Ping Pong Game
A classic two-player ping pong game built with PyGame featuring smooth paddle controls, ball physics, and scoring system.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Documentation](#documentation)

## Features
- **Two-Player Gameplay**: Play against a friend using different controls
- **Smooth Controls**: Responsive paddle movement with W/S and Up/Down arrow keys
- **Realistic Physics**: Ball bouncing and collision detection with paddles and walls
- **Scoring System**: Track points for both players
- **Visual Elements**:
  - Dotted center line
  - Color-coded paddles (blue for Player 1, red for Player 2)
  - Real-time score display
  - Attractive midnight blue background
- **Error Handling**: Comprehensive error handling for robust gameplay
- **Frame Rate Control**: Consistent 60 FPS for smooth gameplay

## Requirements
- Python 3.6 or higher
- PyGame 2.5.0 or higher
- pytest 7.0.0 or higher (for testing)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/<your-username>/ping-pong-game.git
cd ping-pong-game
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the main game file:
```bash
python ping_pong.py
```

**Game Controls:**
- **Player 1 (Left Paddle - Blue):**
  - W key: Move paddle up
  - S key: Move paddle down
- **Player 2 (Right Paddle - Red):**
  - Up Arrow: Move paddle up
  - Down Arrow: Move paddle down

**Game Rules:**
- Each player controls a paddle to hit the ball
- Score points when the opponent misses the ball
- Ball bounces off top and bottom walls
- First to reach a predetermined score wins (no limit in current version)

## Testing
The project includes comprehensive unit tests for paddle movement logic. Run tests using:
```bash
pytest test_ping_pong.py
```

**Tests verify:**
- Paddle movement within screen boundaries
- Boundary collision handling
- Direction-based movement
- Synchronization between paddle data and rectangle object
- Edge case scenarios

## Documentation
Generate HTML documentation using PyDoctor:

1. Install PyDoctor:
```bash
pip install -U pydoctor
```

2. Generate documentation:
```bash
pydoctor --make-html --html-output=docs --project-base-dir="." --docformat=restructuredtext ping_pong.py paddle_logic.py
```

3. View documentation:
Open `docs/index.html` in your web browser

**Documentation includes:**
- Detailed descriptions of all game constants
- Function documentation with parameters and return values
- Class and object descriptions
- Game loop explanation
- Error handling mechanisms

## Project Structure
```
ping-pong-game/
├── ping_pong.py          # Main game file
├── paddle_logic.py       # Paddle movement logic
├── test_ping_pong.py     # Unit tests
├── requirements.txt      # Dependencies
└── README.md            # This file
```

