__author__ = "Charles Engen"

from os import getcwd
from os.path import join as join_

_path = getcwd()
_path_gamedata = join_(_path, "GameData")

scores = []

with open(join_(_path_gamedata, "battleship_time.txt"), "r") as file:
    for line in file:
        scores.append(eval(line))


def get_average_accuracy(score_obj):
    return sum(score_obj) / len(score_obj)


print(get_average_accuracy(scores))
