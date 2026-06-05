__author__ = "Charles Engen"

from os import getcwd
from os.path import join as join_

_path = getcwd()
_path_gamedata = join_(_path, "GameData")

scores = []

with open(join_(_path_gamedata, "battleship_stats.txt"), "r") as file:
    for line in file:
        scores.append(eval(line))


def get_average_accuracy(score_obj):
    total = 0
    shots_win = 0
    min_shot = 100
    for score in score_obj:
        total += score["Accuracy"]
        shots_win += score["Shots"]
        if score["Shots"] < min_shot:
            min_shot = score["Shots"]
    return "Average Accuracy: %0.2f \nShots to Win: %0.2f \nTotal Games: %s\n Best Game: %s" % (
        (total / len(score_obj) * 100),
        (shots_win / len(score_obj)),
        len(score_obj),
        min_shot,
    )


print(get_average_accuracy(scores))
