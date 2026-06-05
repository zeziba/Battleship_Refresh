__author__ = "Charles Engen"
__version__ = "1.0.0"
__date__ = "Monday, September 14, 2015"

"""
This is a redo of the Battleship game
"""

from collections import OrderedDict
from random import randint


class CustomeException(BaseException):
    pass


def ask_xy(col_row=" ", player=False):
    if player:
        return int(input("Pick %sn, 1-10" % col_row))
    else:
        return randint(1, 10)


def delta_dir(player=False):
    try:
        if player:
            delta = str(input("Horizontal or Vertical?"))[0]
            if delta.lower() == "h":
                return 1
            elif delta.lower() == "v":
                return 0
        else:
            return randint(0, 1)
    except ValueError:
        raise CustomeException


class ShipBluePrint(object):
    def __init__(self, **shipdata):
        self.length = shipdata["length"]
        self.name = shipdata["name"]

    def get_name(self):
        return self.name

    def get_length(self):
        return self.length

    def __str__(self):
        return "%s is %s tiles long" % (self.name, self.length)


class Board(object):
    def __init__(self, sides=11):
        self.sides = sides
        self.startBoard = {
            (x, y): "~Water" for y in range(1, self.sides) for x in range(1, self.sides)
        }
        self.backedupBoard = self.startBoard
        self.storedBoard = dict()

    def readable_board(self):
        return OrderedDict(sorted(self.startBoard.items()))

    def print_board(self, safe=False):
        board = self.readable_board()
        if not safe:
            for x in range(1, self.sides):
                for y in range(1, self.sides):
                    if "Damage" in board[x, y]:
                        board[x, y] = "X"
                    elif "Miss" in board[x, y]:
                        board[x, y] = "^"
                    else:
                        board[x, y] = "~"
        for y in range(1, self.sides):
            print(" ".join(str(board[x, y])[0] for x in range(1, self.sides)))

    def backup(self, revert=False):
        if revert:
            self.startBoard = dict(self.backedupBoard)
            return self.startBoard
        else:
            self.backedupBoard = dict(self.startBoard)
            return self.backedupBoard

    def finalize_board(self):
        self.storedBoard = dict(self.startBoard)
        return self.storedBoard


class Player(Board):
    def __init__(self, playernumber):
        Board.__init__(self)
        self.player_Type = self.ask_type() + " " + str(playernumber)
        self.hit_miss = False
        self.hit_enemy_ships = 0
