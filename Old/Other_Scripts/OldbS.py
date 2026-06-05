__author__ = "Charles Engen"
__version__ = "1.0.0"
__date__ = "Monday, August 17, 2015"

"""
This is a full battleship game.
"""


from collections import OrderedDict
from random import randint


class GameWin(BaseException):
    pass


class ShipError(BaseException):
    pass


class TryAgain(BaseException):
    pass


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


class shipBlueprint(object):
    def __init__(self, shipLength, shipName):
        self.shipLength = shipLength
        self.shipName = shipName

    def getName(self):
        return self.shipName

    def getLength(self):
        return self.shipLength

    def __str__(self, *args, **kargs):
        return "%s is %s tiles long." % (self.shipName, self.shipLength)

    def __call__(self):
        return self.shipName

    def __getitem__(self):
        return


class Board(object):
    def __init__(self, sides=11):
        self.sides = sides
        self.startBoard = {
            (x, y): "~Water" for y in range(1, self.sides) for x in range(1, self.sides)
        }
        self.backedupBoard = self.startBoard
        self.storedBoard = dict()

    def print_board(self):
        printableBoard = OrderedDict(sorted(self.startBoard.items()))
        for y in range(1, self.sides):
            print(" ".join(str(printableBoard[x, y])[0] for x in range(1, self.sides)))

    def printBoardOpposition(self, nonprint=False):
        maskedShips = OrderedDict(sorted(self.storedBoard.items()))
        for x in range(1, self.sides):
            for y in range(1, self.sides):
                if "Damage" in maskedShips[x, y]:
                    maskedShips[x, y] = "X"
                elif "Miss" in maskedShips[x, y]:
                    maskedShips[x, y] = "^"
                else:
                    maskedShips[x, y] = "~"
        if not nonprint:
            for y in range(1, self.sides):
                print(" ".join(str(maskedShips[x, y])[0] for x in range(1, self.sides)))
        elif nonprint:
            return maskedShips

    def Backup(self, revert=False):
        def revertBoard():
            self.startBoard = dict(self.backedupBoard)
            return self.startBoard

        if revert:
            revertBoard()
        else:
            self.backedupBoard = dict(self.startBoard)
            return self.backedupBoard

    def finalBoard(self):
        self.storedBoard = self.startBoard
        return self.storedBoard


class Player(Board):
    def __init__(self, playernumber):
        Board.__init__(self)
        self.playerType = self.askPlayerType() + " " + str(playernumber)
        # self.hit_miss = False
        self.hitEnemyShips = 0
        self.misses = 0
        self.poshit = []
        self.even_moves = [(x, y) for x, y in self.startBoard if (x or y) % 2 == 0]
        self.odd_moves = [(x, y) for x, y in self.startBoard if (x or y) % 2 != 0]
        self.moves_left = [(x, y) for x, y in self.startBoard]
        self.fleet = [
            shipBlueprint(5, "Aircraft Carrier"),
            shipBlueprint(4, "Battleship"),
            shipBlueprint(3, "Submarine"),
            shipBlueprint(3, "Destroyer"),
            shipBlueprint(2, "Patrol Boat"),
        ]

    def askPlayerType(self):
        playerType = input("Are you man or machine?").lower()
        if "man" in str(playerType):
            return playerType
        else:
            return "Machine"

    def placeShipSection(self, ship, posx, posy):
        if "Water" not in self.startBoard[posx, posy]:
            print("No Water")
            raise StopIteration()
        else:
            self.startBoard[posx, posy] = ship.getName()
            return self.startBoard

    def shipGen(self, ship, posx, posy, hv):
        try:
            self.Backup()
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
                self.Backup()
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
                                self.Backup(revert=True)
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
                                self.Backup(revert=True)
                                continue
                            break
                else:
                    x += 1
                    return
            except TypeError as e:
                print(e)
            finally:
                print("")
                self.storedBoard = self.finalBoard()
                self.print_board()
                pass

    def __type__(self):
        return self.playerType

    def __str__(self, *args, **kargs):
        return "You are a %s!!!" % self.playerType


def ai(player1):

    delta_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    try:
        if player1.poshit:
            posx, posy = player1.poshit[-1]
            pos_moves = [
                ((posx + move[0]), (posy + move[1]))
                for move in delta_moves
                if ((posx + move[0]), (posy + move[1])) in player1.moves_left
            ]
            print(pos_moves)
            if not pos_moves:
                player1.poshit.remove((posx, posy))
            else:
                pos = pos_moves[randint(0, len(pos_moves))]
                x, y = pos
                print(x, y)
                return x, y
        elif not player1.poshit:
            pos_e = [
                (pos[0], pos[1])
                for pos in player1.even_moves
                if pos in player1.moves_left
            ]
            if pos_e:
                posx, posy = pos_e[randint(0, len(pos_e))]
            else:
                pos_o = [
                    (pos[0], pos[1])
                    for pos in player1.odd_moves
                    if pos in player1.moves_left
                ]
                posx, posy = pos_o[randint(0, len(pos_o))]
            return posx, posy

    finally:
        # pos = [(pos[0], pos[1]) for pos in player1._moves_left]
        # return pos[0], pos[1]
        pass

    # try:
    #     if player1.poshit:
    #         posx, posy = player1.poshit[-1]
    #     lopm = [(posx+x, posy+y) for x, y in moves]
    #     for ax, ay in lopm:
    #         if (ax, ay) not in player1.poshit:
    #             pcms.append((ax, ay))
    #     cx, cy = pcms[randint(0, len(pcms))]
    #     return cx, cy
    # except IndexError:
    #     listpm = [(x, y) for x in range(1, 11) for y in range(1, 11)]
    #     moves = []
    #     offmoves = []
    #     try:
    #         for (ax, ay) in listpm:
    #             if (ax, ay) not in player1.poshit:
    #                 moves.append((ax, ay))
    #                 if ax % 2:
    #                     if ay % 2:
    #                         offmoves.append((ax, ay))
    #         return offmoves[randint(0, len(moves))]
    #     except IndexError:
    #         return moves[randint(0, len(moves))]
    # except KeyError:
    #     pass


def fireShot(player1, player2):
    def getCords(player):
        if "man" in player.__type__():
            return askXY(player=True), askXY(player=True)
        elif "Machine" in player1.__type__():
            cx, cy = ai(player1)
            return cx, cy

    def remove_pos(x, y):
        player1.moves_left.remove((x, y))

    while True:
        try:
            x, y = getCords(player1)
            if ("Damaged" or "Miss") in player2.storedBoard[x, y]:
                print("You have already fired here at [%s, %s]" % (x, y))
                raise TryAgain

            elif "Water" in player2.storedBoard[x, y]:
                print("At [%s, %s] was nothing!" % (x, y))
                player2.storedBoard[x, y] = "Missed"
                player1.poshit.append((x, y))
                player1.misses += 1
                # player1.hit_miss = False
                remove_pos(x, y)
                return False

            else:
                for ship in range(len(player2.fleet)):
                    if player2.storedBoard[x, y] in player2.fleet[ship].getName():
                        print(
                            "You have hit the %s at [%s, %s]"
                            % (player2.fleet[ship].getName(), x, y)
                        )
                        # player1.hit_miss = True
                        player1.poshit.append((x, y))
                        player2.storedBoard[x, y] += "Damaged"
                        player1.hitEnemyShips += 1
                        checkSink(player2, player1, player2.fleet[ship])
                        checkIfWin(player1, player2)
                        remove_pos(x, y)
                        return False
        except IndexError:
            pass
        except KeyError:
            pass
        except TypeError:
            pass
        except TryAgain:
            continue

    checkIfWin(player1, player2)


def checkSink(player1, player2, ship):
    shipHp = 0
    for i in range(1, player1.sides):
        for j in range(1, player1.sides):
            if (
                ship.getName() in player1.storedBoard[i, j]
                and "Damaged" in player1.storedBoard[i, j]
            ):
                shipHp += 1
                player2.lasthit = (0, 0)
                print(shipHp)

    if ship.getLength() == shipHp:
        print("You sunk %s 's %s" % (player1.playerType, ship.getName()))


def checkIfWin(player1, player2):
    if player1.hitEnemyShips == 17:
        print("%s has won the game over %s" % (player1.playerType, player2.playerType))
        print(
            (
                "%s had an accuracy of %.4f%%"
                % (
                    player1.playerType,
                    (
                        (
                            player1.hitEnemyShips
                            / (player1.hitEnemyShips + player1.misses)
                        )
                        * 100
                    ),
                )
            )
        )
        player2.print_masked_board()
        input("Press Enter to Continue")
        raise GameWin


def startGame(x=0):
    print("This is BattleShip the Game!")
    print("There are two players present. Assign player one now.")
    global p1
    p1 = Player(1)
    p1.fleetGen()
    print("Now assign player 2")
    global p2
    p2 = Player(2)
    p2.fleetGen()
    input("Stop")
    print("Now we will start the game, ")
    global turns
    turns = 0
    while x == 0:
        while True:
            try:
                if turns % 2 == 0:
                    print("Place your shot Player 1")
                    fireShot(p1, p2)
                    turns += 1
                    p2.printBoardOpposition()
                    # p2.print_board()
                    print("Player Two's known Board, on turn %s" % turns)
                elif turns % 2 != 0:
                    print("Place your shot Player 2")
                    fireShot(p2, p1)
                    turns += 1
                    p1.printBoardOpposition()
                    # p1.print_board()
                    print("Player One's Known Board, on turn %s" % turns)

            except GameWin:
                x += 1
                return False


if __name__ == "__main__":
    startGame()
    # p1 = Player(1)
    # p1.fleetGen()
    # p2 = Player(2)
    # p2.fleetGen()
