[![Build Status](https://travis-ci.com/zeziba/Battleship_revisited.svg?branch=master)](https://travis-ci.com/zeziba/Battleship_revisited)
[![Coverage Status](https://coveralls.io/repos/github/zeziba/Battleship_revisited/badge.svg)](https://coveralls.io/github/zeziba/Battleship_revisited)

### Battle Ship - Revisited

###### This is a recreation of a program which I originally made when i first started to program. I have updated it to display the new ideas and techniques that I have learned.

As of January 9, 2019 this program is in a working condition. Below are some things I still wish to work on and
complete.

1. Update unittest to better reflect usage of the program
2. Update output to read better
3. Create an installer for pip
4. Integrate automated unittest and integration
5. Add additional AI algorithms for increased difficulties

The current form of the program basically uses a greedy algorithm to decide where to fire a shot. This has the benefit
of winning a game in roughly 60-80 moves which gives a human player many opportunities to win.

# To Setup

> pip install -r requirements.txt

#### Run the tests

> python -m pytest --cov=src --cov-config=.coveragerc --cov-report html tests/
