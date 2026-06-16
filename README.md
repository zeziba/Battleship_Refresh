# Battleship Refresh (GUI)

Welcome to Battleship Refresh, a modernized desktop implementation of the classic naval combat game. Built with Python 3 and a slick, modern graphical user interface powered by CustomTkinter, this version features robust AI opponents, fully tracked gameplay statistics, customizable rules, and an automated flavor-text name generator for an immersive experience.
## Features

- Modern UI/UX: Built using CustomTkinter for a clean, responsive, dark-mode-native desktop interface.
- Intelligent AI: Play against a dedicated automated opponent with optimized target-seeking logic.
- Dynamic Component System: Fully modular board tracking, ship damage states, and fleet allocations.
- Procedural Flavor: Integrated identity generation utilizing custom localized text files for first names, middle names, and geographic deployment origins.
- Extensive Configuration & Validation: Rigid rule handling and a comprehensive logging ecosystem to audit turns, hits, and misses.

## Repository Architecture

The project maintains a clean separation of concerns between core game loop data, UI renderers, and resource storage:


### Example Game Output

```Plaintext

Battleship_Refresh-GUI/
├── .github/workflows/    # CI/CD automated test pipelines
├── resources/            # Data assets for name/place generation
│   ├── first-names.txt
│   ├── middle-names.txt
│   └── places.txt
├── src/                  # Application source code
│   ├── main.py           # Application entry point
│   ├── UI.py             # Base UI definitions
│   ├── CtkUI.py          # CustomTkinter GUI wrapper & implementation
│   ├── Game.py           # Core gameplay loop and session coordinator
│   ├── GameRules.py      # Validation mechanics for moves and ship placement
│   ├── Board.py          # Coordinate grid array mechanics
│   ├── Tile.py           # Individual coordinate square state trackers
│   ├── Fleet.py          # Group collection management for active ships
│   ├── Ship.py           # Single vessel dimensional and structural states
│   ├── Player.py         # Human vs AI profile management
│   ├── AI.py             # Target hunting and firing algorithms
│   ├── Stats.py          # Session tracking (accuracy, hit/miss ratios)
│   ├── Logger.py         # Formatted debugging and event logs
│   └── name_generator.py # Procedural text constructor for entities
└── tests/                # Complete Pytest test suite matching src modules
```

## Installation & Setup
### Prerequisites

    Python 3.10 or higher

    pip (Python package installer)

### 1. Clone the Repository

```Bash
Bash

git clone https://github.com/yourusername/Battleship_Refresh-GUI.git
cd Battleship_Refresh-GUI
```

### 2. Set Up a Virtual Environment (Recommended)

```Bash
Bash

python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```Bash
Bash

pip install -r requirements.txt
```

Note: Core interface operations rely heavily on customtkinter. Ensure your display drivers are properly updated for hardware-accelerated UI rendering.

## Running the Game

To launch the primary application graphical window, execute the main module directly from the root directories:

```Bash
Bash

python -m src.main
```

## Development & Testing

This repository is built for continuous integration, incorporating complete validation configurations via pytest.ini and .coveragerc.
### Install Development Dependencies

```Bash
Bash

pip install -r requirements_dev.txt
```

### Run the Test Suite

Execute the testing framework to evaluate suite health across all core state objects (Board, Fleet, GameRules, etc.):

```Bash
Bash

pytest
```

### Check Test Coverage
```Bash
Bash

coverage run -m pytest
coverage report -m
```

## License

This project is licensed under the MIT License - see the LICENSE file for comprehensive permissions details.


# Play the game in the terminal

```Bash
Bash

python -m src.main -terminal
```


```text
Currently turn: 113 with player (1) Admiral Pierette Ezequiel of Foxcroft being targeted
Shot at (6,8) was a hit
CARRIER has been sunk!
Player - (2) Admiral Cybill Massimo of Ouray Board     Player - (1) Admiral Pierette Ezequiel of Foxcroft Board
   0 1 2 3 4 5 6 7 8 9                                    0 1 2 3 4 5 6 7 8 9
0 |+ . + + D D D . . +                                 0 |+ . . + . + . S S S 
1 |. + + . + + . . + B                                 1 |+ . . + . + . . + + 
2 |+ P . . + . . + + B                                 2 |. + + . . . . + . . 
3 |+ P + + . + + . + B                                 3 |+ . . . P P . + . + 
4 |. + + . . + . . + B                                 4 |. + . . + + + + + . 
5 |. + . . + . . + . +                                 5 |+ + + . + D D D . + 
6 |+ . . + . . + . . +                                 6 |+ B + . . . + . + . 
7 |. . + . . + . . . .                                 7 |+ B + + + . + . . + 
8 |+ . + . + + + + . .                                 8 |. B C C C C C + . . 
9 |+ . . C C C C C + +                                 9 |. B + + + + . . . . 

(2) Admiral Cybill Massimo of Ouray has won the game!
   0 1 2 3 4 5 6 7 8 9
0 |+ . . + . + . S S S 
1 |+ . . + . + . . + + 
2 |. + + . . . . + . . 
3 |+ . . . P P . + . + 
4 |. + . . + + + + + . 
5 |+ + + . + D D D . + 
6 |+ B + . . . + . + . 
7 |+ B + + + . + . . + 
8 |. B C C C C C + . . 
9 |. B + + + + . . . . 
```
