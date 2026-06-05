"""
Created on Aug 9, 2014
Last worked on Jan 11, 2015

@author: Charles Engen

We are creating a basic battleship game, not only with full
sized ships but with it's full size board as well. You can have two computers duke it out
or you can play manually.

This little project was a means to an end. While building this program I learned a lot about Python and programming
    in general. That is why a lot of the code in not as neat as it could be but I do believe that I did the best
    could at the time.

"""


# Imports

# We import this because we are going to use it to order our board later.
from collections import OrderedDict
from random import randint


class GameWin(BaseException):
    """This class is raised as an error if the win conditions are ever met by a player."""

    pass


class ShipError(BaseException):
    pass


###########
# This function takes a variable and asks the user what number they would like to pick
###########
def askXY(player=False):
    if player:
        return int(input("Pick a number 1-10"))
    else:
        return randint(1, 10)


def horizontal_or_vertical(player=False):
    try:
        if player:
            h_v = str(input("Horizontal or Vertical?"))[0]
            if h_v[0].lower() == "v":
                return 0
            elif h_v[0].lower() == "h":
                return 1
            else:
                print("You failed to make a good choice!")
                raise ValueError
        elif not player:
            return randint(0, 1)
    except ValueError:
        raise StopIteration()
    else:
        return randint(0, 1)


############
# Creates a class object for future ships to inherit.
############
class shipBlueprint(object):
    """Creates object for ships."""

    # Creates variables so they can be passed to other functions later.
    def __init__(self, shipLength, shipName):
        self.shipLength = shipLength
        self.shipName = shipName

    # Returns the ship name when called
    def getName(self):
        return self.shipName

    # Returns the ship length when called
    def getLength(self):
        return self.shipLength

    # Returns the Ship's name and it's length when the object is called
    def __str__(self, *args, **kargs):
        return "%s is %s tiles long." % (self.shipName, self.shipLength)

    def __call__(self):
        return self.shipName

    def __getitem__(self):
        return


###########
# The data structure that I am generating now is will look like
#    data = {
#    (1,1):'`Water',
#    (1,2):'ship',
#    (1,3): 'shipDamagedP2'
#    ...
#    }
#
#    Uses the OrderedDict method from collections on the board to ordered the dict.
#   Creates a class Object for the board and assigns a method to print the board.
###########
class Board(object):
    """Creates a board object with a print board method and other methods specific to actions on the board."""

    # Creates a board based on the length that is provided.
    def __init__(self, sides=11):
        self.sides = sides
        self.storedBoard = {
            (x, y): "~Water" for y in range(1, self.sides) for x in range(1, self.sides)
        }
        self.backedupBoard = self.storedBoard

    # This is the board's print method
    def print_board(self):
        printableBoard = OrderedDict(sorted(self.storedBoard.items()))
        for y in range(1, self.sides):
            print(" ".join(str(printableBoard[x, y])[0] for x in range(1, self.sides)))

    def printBoardOpposition(self):
        """This function creates a masked board so you can print it out after you fire a shot."""
        self.getMap()
        maskedShips = dict(self.storedBoard)
        for y in range(1, self.sides):
            for x in range(1, self.sides):
                for xFleet in range(len(self.fleet)):
                    if self.fleet[xFleet].getName() in maskedShips[x, y]:
                        if self.fleet[xFleet].getName() in maskedShips[x, y]:
                            maskedShips[x, y] = "~"
                        if "damage" in str(maskedShips[x, y]).lower():
                            maskedShips[x, y] = "X"
                        if "miss" in str(maskedShips[x, y]).lower():
                            maskedShips[x, y] = "^"
        for y in range(1, self.sides):
            print(" ".join(str(maskedShips[x, y])[0] for x in range(1, self.sides)))

    def getMap(self):
        return self.storedBoard

    def backupBoard(self):
        self.backupedBoard = dict(self.storedBoard)
        return self.backedupBoard

    def getBackUp(self):
        self.storedBoard = dict(self.backupedBoard)
        return self.storedBoard

    def realBackUp(self):
        self.getBackUp()
        self.getMap()


#############
# Create a class system to generate boards and apply ships to the board.
#############
class Player(Board):
    def __init__(self):
        Board.__init__(self)
        self.playerType = self.askPlayerType()
        self.hitEnemyShips = 0
        self.fleet = [
            shipBlueprint(5, "Aircraft Carrier"),
            shipBlueprint(4, "Battleship"),
            shipBlueprint(3, "Submarine"),
            shipBlueprint(3, "Destroyer"),
            shipBlueprint(2, "Patrol Boat"),
        ]

    # Asks Player Type
    def askPlayerType(self):
        """This is to build the boards for different players. I will soon incorporate more functionality into it."""
        playerType = input("Are you man or machine?").lower()
        if "man" in str(playerType):
            return playerType
        else:
            playerType = str("Machine")
            return playerType

    def placeShipSection(self, ship, posx, posy):
        if "water" not in self.storedBoard[posx, posy].lower():
            print("No Water")
            raise StopIteration()
        else:
            if 0 > posx > 10:
                if 0 > posy > 10:
                    raise StopIteration()
            else:
                self.storedBoard[posx, posy] = ship.getName()
                return self.storedBoard

    def shipGen(self, ship, posx, posy, hv):
        try:
            self.realBackUp()
            for tile in range(ship.getLength()):
                if hv:
                    self.placeShipSection(ship, posx, (posy + tile))
                elif not hv:
                    self.placeShipSection(ship, posx + tile, posy)
        except StopIteration:
            raise ShipError()
        except KeyError:
            raise ShipError()
        except IndexError:
            raise ShipError()

    def fleetGen(self, x=0):
        while x < 1:
            try:
                self.backupBoard()
                for ship in range(len(self.fleet)):
                    if "man" in self.playerType:
                        while True:
                            try:
                                print(
                                    "You are placing the %s"
                                    % (self.fleet[ship].getName())
                                )
                                posx, posy, hv = (
                                    askXY(player=True),
                                    askXY(player=True),
                                    horizontal_or_vertical(player=True),
                                )
                                print(
                                    "You are placing %s at (%s, %s) %s"
                                    % (self.fleet[ship].getName(), posx, posy, hv)
                                )
                                self.shipGen(self.fleet[ship], posx, posy, hv)
                            except ShipError:
                                self.realBackUp()
                                print(
                                    "Failed to place %s at (%s, %s)"
                                    % (self.fleet[ship].getName(), posx, posy)
                                )
                                continue
                            break
                        else:
                            x += 1
                            return
                    elif "Machine" in self.playerType:
                        while True:
                            try:
                                print(
                                    "You are placing the %s"
                                    % (self.fleet[ship].getName())
                                )
                                posx, posy, hv = (
                                    askXY(),
                                    askXY(),
                                    horizontal_or_vertical(),
                                )
                                self.shipGen(self.fleet[ship], posx, posy, hv)
                            except ShipError:
                                self.realBackUp()
                                continue
                            break
                else:
                    x += 1
                    return
            finally:
                print("")
                self.print_board()
                pass

    def __type__(self):
        return self.playerType

    def __str__(self, *args, **kargs):
        return "You are a %s!!!" % (self.playerType)


###########
# Damages the ship
###########
def fireShot(player1, player2, t=0):
    """This function takes 2 arguments(x, y) from a player and places a shot on the other player's board,
    if there is a hit it updates the board same as with a miss. There is also checking to see
    if a shot was placed there previously.
    """
    while True:
        try:
            if t == 0:
                x, y = 0, 0
                if "man" in player1.__type__():
                    x, y = askXY(player=True), askXY(player=True)
                elif "Machine" in player1.__type__():
                    x, y = askXY(), askXY()
                if (
                    "damaged" in player2.storedBoard[x, y].lower()
                    or "miss" in player2.storedBoard[x, y].lower()
                ):
                    print("You already shot here at [%s, %s]" % (x, y))
                    input("Pause")
                elif "water" in player2.storedBoard[x, y].lower():
                    player2.storedBoard[x, y] = "Missed"
                    print("You missed")
                    t += 1
                    return False
                else:
                    for amount in range(len(player2.fleet)):
                        if player2.storedBoard[x, y] in player2.fleet[amount].getName():
                            print("You hit the %s" % player2.fleet[amount])
                            player2.storedBoard[x, y] = (
                                "Damaged" + player2.fleet[amount].getName()
                            )
                            t += 1
                            player1.hitEnemyShips += 1
                            checkSink(p2, p1, player2.fleet[amount])
                            checkIfWin(player1, player2)
                            return False
        except KeyError:
            print(KeyError)
            break
        except IndexError:
            print(IndexError)
            break

    checkIfWin(player1, player2)


def checkSink(player1, player2, ship):
    """This function scans the board and sets a var to how many hits a boat has, if it is equal
    to the ship length then it tells us that it was sunk.
    """
    shipHp = 0
    for i in range(1, player1.sides):
        for j in range(1, player1.sides):
            if (
                ship.getName() in player2.storedBoard[i, j]
                and "Damaged" in player2.storedBoard[i, j]
            ):
                shipHp += 1
                print(shipHp)

    if ship.getLength() == shipHp:
        print("You sunk %s 's %s" % (player2.playerType, ship.getName()))


def checkIfWin(player1, player2):
    """This function will check if you have won the game."""
    if player1.hitEnemyShips == 17:
        print("%s has won the game over %s" % (player1.playerType, player2.playerType))
        input("Press Enter to Continue")
        raise GameWin


###########
# Instantiates the mechanics of the game.
###########
def startGame(x=0):
    """This function is all the functionality that will be need to run the game autonomously."""
    print("This is BattleShip the Game!")
    print("There are two players present. Assign player one now.")
    # Here we assign a global var for player one and assign the class player to it.
    global p1
    p1 = Player()
    # We then check if the player want it to be a computer or a human player.
    # I have it automatically place the ships if it's a computer
    # Down the line it will also play with the person or against the computer.
    p1.fleetGen()
    print("Now assign player 2")
    # Here we assign a global var for player two and assign the class player to it.
    global p2
    p2 = Player()
    p2.fleetGen()
    print("Now we will start the game, ")
    global turns
    turns = 0
    while x == 0:
        while True:
            try:
                # This is when we start to actually fire shots at the other players board
                if turns % 2 == 0:
                    print("Place your shot Player 1")
                    fireShot(p1, p2)
                    turns += 1
                    print(p2.printBoardOpposition())
                    print("Player Two's known Board, on turn %s" % (turns))
                elif turns % 2 != 0:
                    print("Place your shot Player 2")
                    fireShot(p2, p1)
                    turns += 1
                    print(p1.printBoardOpposition())
                    print("Player One's Known Board, on turn %s" % (turns))
            except KeyError:
                print("KeyError")
                return
            # This special error is raised if the Win condition is met.
            except GameWin:
                x += 1
                return False


#############
# initialize Script
#############
if __name__ == "__main__":
    # do something
    startGame()
