### Battle Ship - Revisited

###### This is a recreation of a program which I originally made when i first started to program. I have updated it to display the new ideas and techniques that I have learned.

1. Update unittest to better reflect usage of the program
4. Integrate automated unittest and integration
5. Add additional AI algorithms for increased difficulties

The current form of the program basically uses a greedy algorithm to decide where to fire a shot. This has the benefit
of winning a game in roughly 60-80 moves which gives a human player many opportunities to win.

# To Setup

> pip install -r requirements.txt

#### Run the tests

> python -m pytest --cov=src --cov-config=.coveragerc --cov-report html tests/
