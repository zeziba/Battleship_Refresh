__author__ = "Charles Engen"

# All the imports that are needed
from collections import OrderedDict
from random import randint

# This is used to profile the script's AI and other functions
import cProfile

# These are the globals
# The p1, p2 variables will be set to contain the Player or AI class
p1 = None
p2 = None
# If Display is changed to False all print outs will be stopped
Display = True
turns = 0
# When Save Accuracy is true it will print out a file to store accuracy.
# For testing purpose of the AI only
Save_Accuracy = False

# I have put all the print out text here so I can change it if needed
responses = {
    0: "Player %s Are you 'Man' or 'Machine'?",
    1: "You failed to enter a valid entry.",
    2: "What is your name?",
    3: "Pick a number 1-10",
    4: "You have already fired here at [%s, %s]",
    5: "At [%s, %s] was nothing!",
    6: "You have hit the something at [%s, %s]",
    7: "You tried and failed to attack, try again.",
    8: "You sunk %s!",
    9: "You are placing the %s",
    10: "You are placing %s at (%s, %s) %s",
    11: "Failed to place %s at (%s, %s)",
    12: "%s at %s",
    13: "You are a %s!!!",
    14: "Hit a key to continue.",
    15: "Place your shot Player 1",
    16: "Player %s's known Board, on turn %s",
    17: "Place your shot Player 2",
    18: "Your accuracy was %s, you fired %s times!",
    19: "Enter 1 to profile.",
    21: "\n******************************\n"
    "*********CONGRATS*************\n"
    "******************************\n",
    22: "'%s is %s tiles long.'",
}


def ask_xy(player=False):
    """
    This function simply asks for or returns a number
    :param player: If set to True will ask otherwise will return a number
    :return: Gives back a int
    """
    if player:
        return int(input(responses[3]))
    else:
        return randint(1, 10)


def horizontal_or_vertical(player=False):
    """
    This function asks for or returns 0/False or 1/True based on input
    :param player: When True will give a random True/False
    :return: Returns 0/1
    """
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
        pass
    else:
        return randint(0, 1)


def ask_type(player, valid=False):
    """
    This function returns True/False to determine if the player is a machine
    :param player: Pass the Class Object Here
    :param valid: Used to loop through till a valid response is had
    :return: Returns True/False to tell if Man or Machine
    """
    while not valid:
        try:
            p_type = str(input(responses[0] % player))
            if ("man" or 1) == p_type.lower():
                return True
            else:
                return False
        except TypeError:
            print(responses[1])


def check_sink(opponent, ship):
    """
    This function checks to see if a ship has been sunk,
    also sets the ship's bool value to True if sunk.
    :param opponent: Pass the Opponents Class Object here
    :param ship: Pass the Ship you would like to check here
    :return: Returns True if the ship is sunk
    """
    ship_hp = 0
    for i in range(1, opponent.sides):
        for j in range(1, opponent.sides):
            if (
                ship.get_name() in opponent.storedBoard[i, j]
                and "Damaged" in opponent.storedBoard[i, j]
            ):
                ship_hp += 1

    if ship.get_length() == ship_hp:
        if Display:
            print(responses[8] % ship.get_name())
        for boat in opponent.fleet:
            if ship.get_name() == boat.__dict__["shipName"]:
                for number, nship in enumerate(opponent.fleet):
                    if nship.__dict__["shipName"] == ship.get_name():
                        opponent.sink_ship(number)
                return True


def check_win(player):
    """
    This function checks to see if a player has sunk all ships by
    checking if they have hit 17 positions
    :param player: Pass the player to be checked for all sunk ships
    :raise: When invoked it will cause an exception that is caught by the _start_game Mainloop
    """
    if player.hits == 17:
        raise GameWin(player)


# These Two Classes are Custom Errors to catch specific events
class ShipError(BaseException):
    """
    This Class Exception is used for Flow control only.
    """

    pass


class GameWin(BaseException):
    """
    This Class Exception is used for flow control and to display data when called.
    """

    def __init__(self, player1):
        """
        The __init__ computes a players accuracy and displays it.
        :param player1:
        """
        self.player = player1
        self.hits = player1.hits
        self.misses = player1.misses
        self.print_accuracy()

    def print_accuracy(self):
        """
        This function is used to computer and display player accuracy.
        """
        total = self.hits + self.misses
        print(responses[21])
        print(responses[18] % (((self.hits / total) * 100), total))
        if Save_Accuracy:
            with open("score_data.txt", "a") as file:
                file.write("\n%s" % str((self.hits / total) * 100))
        global turns
        turns = 0


class ShipBlueprint(object):
    """
    This function is the framework for all player ships.
    """

    def __init__(self, ship_length, ship_name, sunk):
        """
        The __init__ takes the length and name of the ship and assigns it a bool value
        to tell if it has been sunk or not.
        :param ship_length: Length of ship to be generated
        :param ship_name: Name of ship to be generated
        :param sunk: True/False if the ship is sunk
        """
        self.shipLength = ship_length
        self.shipName = ship_name
        self.sunk = sunk

    def get_name(self):
        """
        This function gets the name of the ship
        :return: Returns the name of the called ship
        """
        return self.__dict__["shipName"]

    def get_length(self):
        """
        This function returns the length of the ship
        :return: Returns the length of the ship
        """
        return self.__dict__["shipLength"]

    def __str__(self):
        """
        When a ship is printed it will print the str of out_put_data[22] which takes two
        string inputs of ship name and ship length
        :return: Returns the string to be displayed
        """
        return responses[22] % (self.__dict__["shipName"], self.__dict__["shipLength"])

    def __call__(self):
        """
        When a ship blueprint object is called it will return if the ship is sunk or not
        :return: Returns True/False based on the Ship's state
        """
        return self.sunk


class Board(object):
    """
    This is the board class that contains the board and all the functions
    to work on the board.
    """

    def __init__(self, size=10):
        """
        The __init__ has a standard size of 10 but can be larger/smaller if the user wants to edit it.
        :param size: Changes the size of the board
        """
        self.sides = size
        self.startBoard = {
            (x, y): "~Water"
            for y in range(1, self.sides + 1)
            for x in range(1, self.sides + 1)
        }
        self.backedup_board = self.startBoard
        self.storedBoard = dict()

    def print_board(self):
        """
        This function prints out a man-readable board with no masking.
        """
        printable_board = OrderedDict(sorted(self.startBoard.items()))
        for y in range(1, self.sides):
            print(" ".join(str(printable_board[x, y])[0] for x in range(1, self.sides)))

    def print_masked_board(self, nonprint=False):
        """
        This function prinks out a masked human readable board.
        :param nonprint: If set to False will print out the dictionary of the board
        :return: Returns the masked_ships for printing.
        """
        masked_ships = OrderedDict(sorted(self.storedBoard.items()))
        for x in range(1, self.sides):
            for y in range(1, self.sides):
                if "Damage" in masked_ships[x, y]:
                    masked_ships[x, y] = "X"
                elif "Miss" in masked_ships[x, y]:
                    masked_ships[x, y] = "^"
                else:
                    masked_ships[x, y] = "~"
        if not nonprint:
            for y in range(1, self.sides):
                print(
                    " ".join(str(masked_ships[x, y])[0] for x in range(1, self.sides))
                )
        elif nonprint:
            return masked_ships

    def backup(self, revert=False):
        """
        This function saves the state of the bard and reverts it when told to do so.
        :param revert: When True will revert the board to a previous state
        :return: Returns the board
        """

        def revert_board():
            """
            This nested function only reverts the board to a previous state
            :return: Returns the Start board state
            """
            self.startBoard = dict(self.backedup_board)
            return self.startBoard

        if revert:
            revert_board()
        else:
            self.backedup_board = dict(self.startBoard)
            return self.backedup_board

    def final_board(self):
        """
        This function finalizes the board for play.
        :return: Returns the final board
        """
        self.storedBoard = self.startBoard
        return self.storedBoard


class Player(Board):
    """
    This class has all the player functions and methods
    """

    def __init__(self, type_player):
        """
        The __init__ sets the parameters for the player
        :param type_player: The passes argument tells the class what type the player is
        """
        Board.__init__(self)
        self.playerType = type_player
        self.misses = 0
        self.hits = 0
        # This list fills it's self with ships using the arguments inside
        self.fleet = [
            ShipBlueprint(5, "Aircraft Carrier", False),
            ShipBlueprint(4, "Battleship", False),
            ShipBlueprint(3, "Submarine", False),
            ShipBlueprint(3, "Destroyer", False),
            ShipBlueprint(2, "Patrol Boat", False),
        ]

    def sink_ship(self, ship):
        """
        This function changes the state of a ship to True when sunk
        :param ship: Pass the ship to be sunk.
        """
        self.fleet[ship].__dict__["sunk"] = True

    def attack_player(self, opposition_player):
        """
        This function allows the player to attack the other player.

        It also uses a while loop in conjunction with a try to keep the player
        from missing a turn for a bad entry.
        :param opposition_player: Pass the player to be attack
        """

        def get_cords():
            """
            This function is used to call ask_xy twice. just because I can.
            :return: Returns the values of ask_xy
            """
            return ask_xy(player=True), ask_xy(player=True)

        while True:
            try:
                i_x, i_y = get_cords()
                # The following line figure out if a ship was hit or not
                # and does the necessary operations to hit/sink/miss the ship
                if ("Damaged" or "Miss") in opposition_player.storedBoard[i_x, i_y]:
                    print(responses[4] % (i_x, i_y))
                    raise ValueError

                elif "Water" in opposition_player.storedBoard[i_x, i_y]:
                    print(responses[5] % (i_x, i_y))
                    opposition_player.storedBoard[i_x, i_y] = "Missed"
                    self.misses += 1
                    return False

                else:
                    for ship in range(len(opposition_player.fleet)):
                        if (
                            opposition_player.storedBoard[i_x, i_y]
                            in opposition_player.fleet[ship].get_name()
                        ):
                            print(responses[6] % (i_x, i_y))
                            opposition_player.storedBoard[i_x, i_y] += "Damaged"
                            self.hits += 1
                            check_sink(opposition_player, self.fleet[ship])
                            check_win(self)
                            return False
            except ValueError:
                print(responses[7])
            except IndexError:
                pass
            except KeyError:
                pass
            except TypeError:
                pass

    def place_ship_section(self, ship, pos_x, pos_y):
        """
        This function places one section of the ship
        :param ship: Ship to be placed
        :param pos_x: Location of the placed ship in x
        :param pos_y: Location of the ship in y
        """
        if "Water" not in self.startBoard[pos_x, pos_y]:
            raise StopIteration()
        else:
            self.startBoard[pos_x, pos_y] = ship.get_name()

    def ship_gen(self, ship, pos_x, pos_y, h_v):
        """
        This function is used to place ship sections based on the length
        and horizontal or vertical orientation of said ship. It uses the
        place_ship_section method to place each section of a ship
        :param ship: Ship to be placed
        :param pos_x: Top leftmost x value of Ship
        :param pos_y: Top leftmost y value of Ship
        :param h_v: Horizontal or Vertical Orientation of Ship
        """
        try:
            self.backup()
            for tile in range(ship.get_length()):
                if h_v:
                    self.place_ship_section(ship, pos_x, (pos_y + tile))
                elif not h_v:
                    self.place_ship_section(ship, (pos_x + tile), pos_y)
        except StopIteration:
            raise ShipError()
        except KeyError:
            raise ShipError()
        except IndexError:
            raise ShipError()

    def fleet_gen(self, on=True):
        """
        This function generates all ships in the player's fleet.
        Everything needed to place the ship is called and used in this function.
        Also has error checking to ensure that a ship is placed in bounds.
        :param on: Inter-function State
        """
        global Display
        display = Display
        while on:
            try:
                self.backup()
                for number, ship in enumerate(self.fleet):
                    if "Man" in self.playerType:
                        while True:
                            try:
                                if display:
                                    print(responses[9] % self.fleet[number].get_name())
                                pos_x, pos_y = ask_xy(player=True), ask_xy(player=True)
                                h_v = horizontal_or_vertical(player=True)
                                if display:
                                    print(
                                        responses[10]
                                        % (
                                            self.fleet[number].get_name(),
                                            pos_x,
                                            pos_y,
                                            h_v,
                                        )
                                    )
                                self.ship_gen(self.fleet[number], pos_x, pos_y, h_v)
                            except ShipError:
                                self.backup(revert=True)
                                if display:
                                    print(
                                        responses[11]
                                        % (self.fleet[number], pos_x, pos_y)
                                    )
                                continue
                            break
                        else:
                            on = False
                            return on
                    elif "Machine" in self.playerType:
                        while True:
                            try:
                                pos_x, pos_y, h_v = (
                                    ask_xy(),
                                    ask_xy(),
                                    horizontal_or_vertical(),
                                )
                                self.ship_gen(self.fleet[number], pos_x, pos_y, h_v)
                            except ShipError:
                                self.backup(revert=True)
                                continue
                            break
                else:
                    on = False
                    return on
            except TypeError as e:
                print(responses[12] % (TypeError, e))
            finally:
                self.storedBoard = self.final_board()
                pass

    def __str__(self):
        """
        When a player object is called it prints out what that player's type is.
        """
        return responses[13] % self.playerType


class AI(Player):
    """
    This Class inherits from the Player class and overwrites the attack method of the Player class.
    There are three difficultly Ais in this class.
    """

    def __init__(self, difficulty, type_player):
        """
        The __init__ sets up the AI parameters
        :param difficulty: Difficulty 0-2 *easy-hard*
        :param type_player: Player type to be passed to the Player.__init__
        """
        Player.__init__(self, type_player)
        self.difficulty = difficulty
        self.hit_state = False
        self.pos_hit = []
        self.even_moves = [(x, y) for x, y in self.startBoard if (x or y) % 2 == 0]
        self.odd_moves = [(x, y) for x, y in self.startBoard if (x or y) % 2 != 0]
        self.moves_left = [(x, y) for x, y in self.startBoard]
        self.point_map = {
            (x, y): 0
            for x in range(1, self.sides + 1)
            for y in range(1, self.sides + 1)
        }
        self.hit_map = []
        self.last_hit = ()
        self.delta_move = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def easy_difficulty(self):
        """
        Easy AI
        :return: returns x, y cords to attack
        """
        pos_x, pos_y = self.moves_left[randint(0, len(self.moves_left))]
        return pos_x, pos_y

    def med_difficulty(self):
        """
        Medium AI
        :return: Returns x, y cords to attack
        """
        # Target Mode
        if self.pos_hit:
            posx, posy = self.pos_hit[-1]
            pos_moves = [
                ((posx + move[0]), (posy + move[1]))
                for move in self.delta_move
                if ((posx + move[0]), (posy + move[1])) in self.moves_left
            ]
            if not pos_moves:
                self.pos_hit.remove((posx, posy))
            else:
                pos = pos_moves[randint(0, len(pos_moves) - 1)]
                x, y = pos
                return x, y
        # Hunt(w/ parity) Mode
        else:
            pos_e = [
                (pos[0], pos[1]) for pos in self.even_moves if pos in self.moves_left
            ]
            if pos_e:
                pos_x, pos_y = pos_e[randint(0, len(pos_e) - 1)]
            else:
                pos_x, pos_y = self.moves_left[randint(0, len(self.moves_left) - 1)]
            return pos_x, pos_y

    # All Following Functions are part of Hard Difficulty
    def check_delta_moves(self, coord, magnitude):
        """
        This function checks all the adjacent tiles around the given cords,
        it then checks to see if they are valid moves. If there is any invalid move
        in a set of cords it does not put them into the list.
        :param coord: Pass cords to be checked
        :param magnitude: Pass how far out from cords you want to check
        :return: Returns a list of all adjacent cords
        """

        to_move = [
            possible_move
            for possible_move in [
                move
                for move in [
                    [
                        (coord[0] + (c_x * mag), coord[1] + (c_y * mag))
                        for mag in range(1, magnitude)
                    ]
                    for c_x, c_y in self.delta_move
                ]
                if coord in self.moves_left
            ]
            if magnitude == possible_move
        ]
        return to_move

    def valid_attack_move(self, coord):
        """
        This function creates a list using the check_delta_moves Method to create a list
        of cords that all player ships that can start at a give cord.
        :param coord: Cord to be checked
        """
        test = [
            item
            for sublist in [
                self.check_delta_moves(coord, ship_length)
                for ship_length in [
                    self.fleet[ship].get_length()
                    for ship in range(len(self.fleet))
                    if not self.fleet[ship]()
                ]
            ]
            for item in sublist
        ]

        for item in test:
            self.point_map[item] += 1
        self.point_map[coord] += 1

    def check_all_moves(self):
        """
        This Method calls the valid_attack_move Method for all cords in the move_left list.
        :return:
        """
        for c_x, c_y in self.moves_left:
            self.valid_attack_move((c_x, c_y))

    def best_move(self):
        """
        This function determins all tiles with the most points and returns a random value from that list.
        :return: Returns the highest score tile
        """
        max_value = max(self.point_map.values())
        best_moves = [
            key for key in self.point_map.keys() if self.point_map[key] == max_value
        ]
        return best_moves[randint(0, len(best_moves)) - 1]

    def remove_move(self, coord):
        """
        This function removes a coord from _moves_left.
        :param coord: Cord to be removed
        """
        self.moves_left.remove(coord)

    def reset_point_map(self):
        """
        This Method resets all points on teh point map to 0
        """
        self.point_map = {
            (x, y): 0
            for x in range(1, self.sides + 1)
            for y in range(1, self.sides + 1)
        }

    def check_adj_tiles(self, map_to_check):
        """
        This method returns all adjacent tiles that are still in moves left.
        :param map_to_check: The set of tiles to be checked.
        :return: Returns list of adjacent tiles that are valid
        """
        return [
            (x1 + d_x, y1 + d_y)
            for x1, y1 in map_to_check
            for d_x, d_y in self.delta_move
            if (x1 + d_x, y1 + d_y) in self.moves_left
        ]

    def adjust_for_hits(self):
        """
        This function adds points to the point map for all spaces adjacent to hit tiles if valid.
        """
        all_moves = [
            sublist_5
            for sublist_5 in self.check_adj_tiles(
                [
                    sublist_4
                    for sublist_4 in self.check_adj_tiles(
                        [
                            sublist_3
                            for sublist_3 in self.check_adj_tiles(
                                [
                                    sublist_2
                                    for sublist_2 in self.check_adj_tiles(
                                        [
                                            sublist
                                            for sublist in self.check_adj_tiles(
                                                self.hit_map
                                            )
                                            if sublist
                                        ]
                                    )
                                    if sublist_2
                                ]
                            )
                            if sublist_3
                        ]
                    )
                    if sublist_4
                ]
            )
            if sublist_5
        ]
        for cord in all_moves:
            self.point_map[cord] += 1

    def adjust_last_hit(self):
        """
        This function adds points to the point map around the spaces of the last hit.
        """
        moves = [
            cord
            for cord in [
                (c_x + self.last_hit[0], c_y + self.last_hit[1])
                for c_x, c_y in self.delta_move
            ]
            if cord in self.moves_left
        ]
        for move in moves:
            self.point_map[move] += 5

    def hard_difficulty(self):
        """
        Hard Difficulty AI
        """
        self.reset_point_map()
        self.check_all_moves()
        self.adjust_for_hits()
        # Hunt Mode
        if not self.hit_state:
            return self.best_move()
        # Target mode
        elif self.hit_state:
            self.adjust_last_hit()
            return self.best_move()

    # This overrides the Player class attack_player
    # That way it does a computer attack instead
    def attack_player(self, opposition_player, a_x=0, a_y=0):
        """
        This Method is used to attack the other player and is an override of the
        Player attack_player method
        :param opposition_player: Pass the player to be attacked
        :param a_x: x cord to be attacked
        :param a_y: y cord to be attacked
        """
        if self.difficulty == 0:
            a_x, a_y = self.easy_difficulty()
        elif self.difficulty == 1:
            a_x, a_y = self.med_difficulty()
        elif self.difficulty == 2:
            a_x, a_y = self.hard_difficulty()

        self.moves_left.remove((a_x, a_y))

        if (a_x, a_y) in self.moves_left:
            print("FAIL at %s,%s" % (a_x, a_y))

        if "Water" in opposition_player.storedBoard[a_x, a_y]:
            # print(out_put_data[5] % (a_x, a_y))
            opposition_player.storedBoard[a_x, a_y] = "Missed"
            self.misses += 1
            self.hit_state = False

        else:
            for ship in range(len(opposition_player.fleet)):
                if (
                    opposition_player.storedBoard[a_x, a_y]
                    in opposition_player.fleet[ship].get_name()
                ):
                    if Display:
                        print(responses[6] % (a_x, a_y))
                    opposition_player.storedBoard[a_x, a_y] += "Damaged"
                    self.hits += 1
                    check_sink(opposition_player, opposition_player.fleet[ship])
                    check_win(self)
                    self.hit_map.append((a_x, a_y))
                    self.hit_state = True
                    self.last_hit = (a_x, a_y)


def _start_game(wait_x=1):
    """
    This function is used to control the game.
    :param wait_x: Inter-function Variable
    """
    global p1
    global p2
    global turns
    global Display
    display__start = Display
    if not display__start:
        p1 = AI(difficulty=2, type_player="Machine_1")
        p1.fleet_gen()
        p2 = AI(difficulty=2, type_player="Machine_2")
        p2.fleet_gen()
    elif display__start:
        one = ask_type(1)
        if one:
            p1 = Player(type_player="Man")
        else:
            p1 = AI(difficulty=2, type_player="Machine_1")
            p1.playerType = "Machine"
        p1.fleet_gen()
        two = ask_type(2)
        if two:
            p2 = Player(type_player="Man")
        else:
            p2 = AI(difficulty=2, type_player="Machine_2")
        p2.fleet_gen()
        input(responses[14])
    while wait_x:
        while True:
            try:
                if turns % 2 == 0:
                    if display__start:
                        print(responses[15])
                    p1.attack_player(p2)
                    turns += 1
                    if display__start:
                        p2.print_masked_board()
                        print(responses[16] % ("Two", turns))
                elif turns % 2 != 0:
                    if display__start:
                        print(responses[17])
                    p2.attack_player(p1)
                    turns += 1
                    if display__start:
                        p1.print_masked_board()
                        print(responses[16] % ("One", turns))
            except GameWin:
                wait_x -= 1
                if turns % 2 == 0:
                    p2.print_masked_board()
                if turns % 2 != 0:
                    p1.print_masked_board()
                return False


if __name__ == "__main__":
    Profile = input(responses[19])
    if Profile:
        global Display
        Display = False
        for x in range(1):
            if x % 10 == 0:
                print(x)
            cProfile.run("_start_game()")
    _start_game()
