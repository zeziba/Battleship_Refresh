__author__ = "Charles Engen"

"""
This is a revisit of the Battleship game
TODO:
    Ships:
        5 Ships
            Aircraft Carrier
                Size: 5
            Battleship
                Size: 4
            Submarine
                Size: 3
            Destroyer
                Size: 3
            Patrol Boat
                Size: 2
            No overlapping
    Board:
        10 X 10 Board
            Attack
            Defense
    AI:
        1st: Random Guess
        2nd: More articulate shot positioning
    GUI:
        1st: Text
        2nd: Tkinter gui
"""

import collections
from random import randint
from functools import wraps


def validMove(import_func):
    @wraps(import_func)
    def checker(*args, **kwargs):
        for arg in args:
            print(arg)
        for kwarg in kwargs:
            print(kwarg)
        function = import_func(*args, **kwargs)
        return function

    return checker


class Board(object):
    """Creates the board as an object with the methods to get data from it and apply changes to the data"""

    def __init__(self):
        self.sides = 11
        self.storedboard = {
            (x, y): "empty" for y in range(1, self.sides) for x in range(1, self.sides)
        }
        self.backedupboard = self.storedboard

    def getorderedmap(self):
        """This function will return the data needed to display the board while in game"""
        orderedboarddata = collections.OrderedDict(sorted(self.storedboard.items()))
        return orderedboarddata

    def returncovertboarddata(self):
        """This function will return the board in a covered state"""
        self.getboarddata()
        hiddenship = dict(self.storedboard)
        for y in range(1, self.sides):
            for x in range(1, self.sides):
                if not "empty":
                    if not "shell":
                        if not "damage":
                            hiddenship[x, y] += "hidden"
        return hiddenship

    def backupboard(self):
        """This stores the current board and returns it"""
        self.backedupboard = dict(self.storedboard)
        return self.backedupboard

    def getbackup(self):
        """This overwrites the storedboard with backupboard"""
        self.storedboard = dict(self.backedupboard)
        return self.storedboard

    def getboarddata(self):
        """Updates the storedboard data"""
        return self.storedboard

    def actualbackup(self):
        self.getbackup()
        self.getboarddata()


class Ship(object):
    """
    This Class is the backbone of all the ships, it will have methods that assign the ship to our stored board.
    """

    def __init__(self, shipname, shiplength):
        self.shipName = shipname
        self.shipLength = shiplength

    def getName(self):
        return self.shipName

    def getLength(self):
        return self.shipLength

    def __str__(self, shipName, shipLength):
        return ("%s is %s tiles long.") % (self.shipName, self.shipLength)


shipList = {
    "Aircraft Carrier": 5,
    "BattleShip": 4,
    "Submarine": 3,
    "Destroyer": 3,
    "Patrol Boat": 2,
}


def getCord(player=False):
    """
    Asks for a cord position if player is equal to False, gives a position if True.
    :param player: If set to True will ask for a number
    """
    if player == True:
        return int(input("Pick a number one to ten"))
    else:
        return randint(1, 10)


@validMove
def shipPlacement(posx, posy, shiplength, shipname, user, player=False):
    """
    This function places the ship on the board
    :param posx: X position
    :param posy: Y position
    :param ship: Ship name
    """

    vORh = ""

    if player == True:
        vORh = input("Would you like to place the ship Vertical or Horizontal?")[0]
    else:
        chance = randint(0, 1)
        if chance:
            vOrH = "v"
        else:
            vORh = "h"
    if str(vORh).lower() == "h":
        for length in range(0, shiplength):
            user.storedBoard[posx, posy + length] = shipname[0] + "%s" % shipname
    elif str(vORh).lower() == "v":
        for length in range(0, shiplength):
            user.storedBoard[posx + length, posy] = shipname[0] + "%s" % shipname


PBoard = Board()
PBoard.print_board()
for ship in shipList:
    shipPlacement(getCord(), getCord(), shipList[ship], ship, PBoard)
PBoard.print_board()
