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
Currently turn: 73 with player (1) Admiral Rozelle Regan of Proberta being targeted
Shot at (6,6) was a hit
DESTROYER has been sunk!
Player - (2) Admiral Antonina Egor of Flovilla Board     Player - (1) Admiral Rozelle Regan of Proberta Board
   0 1 2 3 4 5 6 7 8 9                                      0 1 2 3 4 5 6 7 8 9
                                                         
0 |. . + . . . . . . .                                   0 |. . . . + . . . + . 
1 |. + . + . . . + . .                                   1 |+ . + . . + . + . + 
2 |+ . . . . . . . . .                                   2 |B B B B . . . . . . 
3 |. . . . . . . . . +                                   3 |+ . . + . . . . . + 
4 |. . + . . . . . . +                                   4 |. + . . . . . . . . 
5 |. . . . . D . . + B                                   5 |. . + . P C . . . . 
6 |+ . + . + D + . + B                                   6 |. . . + P C D . . . 
7 |. . . + + D + . + B                                   7 |. . . . + C D + . . 
8 |. . + + + + . . + B                                   8 |. . . . + C D S S S 
9 |. + C C C C C . . .                                   9 |. . . . + C + + . + 
```

# To Setup

> pip install -r requirements.txt

#### Run the tests

> pip install -r requirements_dev.txt
> python -m pytest --cov=src --cov-config=.coveragerc --cov-report html tests/


# To run without installation

> python -m src.main
