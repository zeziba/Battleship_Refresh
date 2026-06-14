### Battle Ship - Revisited

###### This is a recreation of a program which I originally made when i first started to program. I have updated it to display the new ideas and techniques that I have learned.

1. Update unittest to better reflect usage of the program
4. Integrate automated unittest and integration
5. Add additional AI algorithms for increased difficulties

This is the standard setup for the game Battleship. It has a board of size 10 with
its 5 ships. With the game config it is possible to make the board larger and
use custom fleets but that is not planned to be included into the main game
currently.


### Example Game Output


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

# To Setup

> pip install -r requirements.txt

#### Run the tests

> pip install -r requirements_dev.txt
> python -m pytest --cov=src --cov-config=.coveragerc --cov-report html tests/


# To run without installation

> python -m src.main
