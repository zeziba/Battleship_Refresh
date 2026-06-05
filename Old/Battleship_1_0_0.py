__author__ = "Charles Engen"

"""
This is a full implementation of the Game Battleship!
There are still somethings I would like to work on but as of right now this is a full text game of Battleship.
TODO:
    Have preference file so you can change if the game data or not.
"""

from collections import OrderedDict
from random import randint
from functools import wraps
from os.path import join as join_
from os import getcwd
from os import makedirs
from os import path
import time
import cProfile

Display = True
Difficulty = 2
start = 0
Save_Stats = True
Save_Point_Maps = True
turns = 0
_game_number = None
path_ = getcwd()
path_gamedata_ = join_(path_, "GameData")
path_gamedata_pointmaps_ = join_(path_gamedata_, "point_maps")

board_size = 10

out_put_data = {
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
    23: "Horizontal or Vertical?",
    24: "A random entry has been done.",
    25: "{'Player': '%s', 'Shots': %s, 'Hits': %s, 'Accuracy': %s, 'Win ON': %s, 'Difficulty': %s}\n",
    26: "Would you like to save the game's point maps and game stats? Enter 1 for yes.",
}


def _create_master_game_number(override=False):
    global _game_number
    try:
        with open(join_(path_gamedata_, "GameNumber.txt"), "r+") as file:
            file.seek(0)
            game_number = file.readline()
            _game_number = int(game_number[12:]) + 1 + (override if not override else 0)
        with open(join_(path_gamedata_, "GameNumber.txt"), "w") as file:
            file.seek(0)
            file.write("Game Number: %s" % str(_game_number))
    except FileNotFoundError:
        with open(join_(path_gamedata_, "GameNumber.txt"), "w") as file:
            file.seek(0)
            _game_number = 1
            file.write("Game Number: %s" % str(_game_number))


def _create_dirs():
    if not path.exists(path_gamedata_):
        makedirs(join_(path_, "GameData"))
    if not path.exists(path_gamedata_pointmaps_):
        makedirs(join_(path_gamedata_, "point_maps"))


def handle_player_input(func):
    """
    This function wraps the two functions that deal with player input.
    If the player hit enter when asked for input it will give a random response.
    :param func: Pass the function you wish to test
    :return: Returns the function after working on it's data
    """

    @wraps(func)
    def _function_wrap(*args, **kwargs):
        """
        This function takes the arguments of the passed function and works on them.
        :param args: The arguments of the function
        :param kwargs: The key arguments of the function
        :return: Returns the data if a response is valid
        """

        def __change_bool_value(*args, **kwargs):
            """
            This function changes the bool value of player if no response was entered.
            :param args: The arguments of the function
            :param kwargs: The key arguments of the function
            :return: Returns converted data
            """
            arg_list = list(args)
            if True in args:
                arg_list = list(args)
                index = arg_list.index(True)
                arg_list[index] = False
            try:
                if True in kwargs["player"]:
                    kwargs["player"] = True
            except KeyError:
                pass
            return tuple(arg_list), kwargs

        valid = False
        while not valid:
            try:
                valid = True
                return func(*args, **kwargs)
            except ValueError:
                valid = True
                print(out_put_data[1], "\n", out_put_data[24])
                return func(*__change_bool_value()[0], **__change_bool_value()[1])
            except IndexError:
                valid = True
                print(out_put_data[1], "\n", out_put_data[24])
                return func(*__change_bool_value()[0], **__change_bool_value()[1])
            except TypeError:
                valid = False
                print(out_put_data[1])

    return _function_wrap


@handle_player_input
def ask_xy(player=False):
    """
    This function asks for player input regarding the position wanted.
    :param player: When True will ask for input, when False will return a random number
    :return: Returns position
    """
    if player:
        return int(input(out_put_data[3]))
    else:
        return randint(1, board_size)


@handle_player_input
def horizontal_or_vertical(player=False):
    """
    This function ask the orientation wanted.
    :param player: If True will ask for input if False will return random direction.
    :return: Returns direction
    """
    if player:
        h_v = str(input(out_put_data[23]))
        return (
            0 if h_v[0].lower() == "v" else 1 if h_v[0].lower() == "h" else ValueError
        )
    else:
        return randint(0, 1)


def ask_type(player):
    """
    This function asks for player type, when no type is entered returns False
    :param player: Pass the player Class to work on
    :return: Returns True/False based on Player/Not
    """
    p_type = str(input(out_put_data[0] % player))
    return p_type if "man" in p_type.lower() else False


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
            print(out_put_data[8] % ship.get_name())
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
        self.player = player1.playerType
        self.difficulty = player1.difficulty
        self.hits = player1.hits
        self.misses = player1.misses
        self.save_data()
        self.print_accuracy()

    def print_accuracy(self):
        if Display:
            total = self.hits + self.misses
            print(out_put_data[21])
            print(out_put_data[18] % (((self.hits / total) * 100), total))

    def save_data(self):
        """
        This function is used to save game data after a win.
        """
        global start
        global turns
        if Save_Stats:
            with open(join_(path_gamedata_, "battleship_stats.txt"), "a+") as file:
                file.write(
                    out_put_data[25]
                    % (
                        self.player,
                        (self.hits + self.misses),
                        self.hits,
                        (self.hits / (self.hits + self.misses)),
                        turns,
                        self.difficulty if self.difficulty else "Player",
                    )
                )
            with open(join_(path_gamedata_, "battleship_time.txt"), "a+") as file:
                file.write("%s\n" % (time.time() - start))
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
        return out_put_data[22] % (
            self.__dict__["shipName"],
            self.__dict__["shipLength"],
        )

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

    def _print_board(self):
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

    def _backup(self, revert=False):
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

    def _final_board(self):
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

    def __init__(self, type_player, p_number=0):
        """
        The __init__ sets the parameters for the player
        :param type_player: The passes argument tells the class what type the player is
        """
        Board.__init__(self)
        self.playerType = type_player
        self.p_number = p_number
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

        def __get_cords():
            """
            This function is used to call ask_xy twice. just because I can.
            :return: Returns the values of ask_xy
            """
            return ask_xy(player=True), ask_xy(player=True)

        while True:
            try:
                i_x, i_y = __get_cords()
                # The following line figure out if a ship was hit or not
                # and does the necessary operations to hit/sink/miss the ship
                if ("Damaged" or "Miss") in opposition_player.storedBoard[i_x, i_y]:
                    print(out_put_data[4] % (i_x, i_y))
                    raise ValueError

                elif "Water" in opposition_player.storedBoard[i_x, i_y]:
                    print(out_put_data[5] % (i_x, i_y))
                    opposition_player.storedBoard[i_x, i_y] = "Missed"
                    self.misses += 1
                    return False

                else:
                    for ship in range(len(opposition_player.fleet)):
                        if (
                            opposition_player.storedBoard[i_x, i_y]
                            in opposition_player.fleet[ship].get_name()
                        ):
                            print(out_put_data[6] % (i_x, i_y))
                            opposition_player.storedBoard[i_x, i_y] += "Damaged"
                            self.hits += 1
                            check_sink(opposition_player, self.fleet[ship])
                            check_win(self)
                            return False
            except ValueError:
                print(out_put_data[7])
            except IndexError:
                pass
            except KeyError:
                pass
            except TypeError:
                pass

    def _place_ship_section(self, ship, pos_x, pos_y):
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

    def _ship_gen(self, ship, pos_x, pos_y, h_v):
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
            self._backup()
            for tile in range(ship.get_length()):
                if h_v:
                    self._place_ship_section(ship, pos_x, (pos_y + tile))
                elif not h_v:
                    self._place_ship_section(ship, (pos_x + tile), pos_y)
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
                self._backup()
                for number, ship in enumerate(self.fleet):
                    if "Man" in self.playerType:
                        while True:
                            try:
                                if display:
                                    print(
                                        out_put_data[9] % self.fleet[number].get_name()
                                    )
                                pos_x, pos_y = ask_xy(player=True), ask_xy(player=True)
                                h_v = horizontal_or_vertical(player=True)
                                if display:
                                    print(
                                        out_put_data[10]
                                        % (
                                            self.fleet[number].get_name(),
                                            pos_x,
                                            pos_y,
                                            h_v,
                                        )
                                    )
                                self._ship_gen(self.fleet[number], pos_x, pos_y, h_v)
                            except ShipError:
                                self._backup(revert=True)
                                if display:
                                    print(
                                        out_put_data[11]
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
                                self._ship_gen(self.fleet[number], pos_x, pos_y, h_v)
                            except ShipError:
                                self._backup(revert=True)
                                continue
                            break
                else:
                    on = False
                    return on
            except TypeError as e:
                print(out_put_data[12] % (TypeError, e))
            finally:
                self.storedBoard = self._final_board()
                pass

    def __str__(self):
        """
        When a player object is called it prints out what that player's type is.
        """
        return out_put_data[13] % self.playerType


class AI(Player):
    """
    This Class inherits from the Player class and overwrites the attack method of the Player class.
    There are three difficultly Ais in this class.
    """

    def __init__(self, difficulty, type_player, point_map_state=False, p_number=0):
        """
        The __init__ sets up the AI parameters
        :param difficulty: Difficulty 0-2 *easy-hard*
        :param type_player: Player type to be passed to the Player.__init__
        """
        Player.__init__(self, type_player, p_number)
        self.difficulty = difficulty
        self.save_point_map = point_map_state
        self._hit_state = False
        self._pos_hit = []
        self._even_moves = [(x, y) for x, y in self.startBoard if (x or y) % 2 == 0]
        self._odd_moves = [(x, y) for x, y in self.startBoard if (x or y) % 2 != 0]
        self._moves_left = [(x, y) for x, y in self.startBoard]
        self._point_map = {
            (x, y): 0
            for x in range(1, self.sides + 1)
            for y in range(1, self.sides + 1)
        }
        self._hit_map = []
        self._last_hit = ()
        self.vs_ship_left = {
            "Aircraft Carrier": [False, 5],
            "Battleship": [False, 4],
            "Submarine": [False, 3],
            "Destroyer": [False, 3],
            "Patrol Boat": [False, 2],
        }
        self.__delta_move = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def __flatten(self, a_list):
        """
        Flattens the given list of an arbitrary amount of lists/items into a single list with all values
        :param a_list: Pass the list object you wish to flatten, no list will be left with in. Also maintains order.
        :return: Returns this function with the hold list as an argument if there
        are any list objects, else it returns the held list.
        """
        hold = []
        for item in a_list:
            if list == type(item):
                for it in item:
                    hold.append(it)
            else:
                hold.append(item)
        return (
            self.__flatten(hold) if any(type(part) == list for part in hold) else hold
        )

    def __easy_difficulty(self):
        """
        Easy AI: Gives a random cord from the moves left
        Generally Wins after 90 turns
        :return: returns x, y cords to attack
        """
        return self._moves_left[randint(0, len(self._moves_left))]

    def __med_difficulty(self):
        """
        Medium AI
        :return: Returns x, y cords to attack
        """
        # Target Mode
        if self._pos_hit:
            posx, posy = self._pos_hit[-1]
            pos_moves = [
                ((posx + move[0]), (posy + move[1]))
                for move in self.__delta_move
                if ((posx + move[0]), (posy + move[1])) in self._moves_left
            ]
            if not pos_moves:
                self._pos_hit.remove((posx, posy))
            else:
                pos = pos_moves[randint(0, len(pos_moves) - 1)]
                x, y = pos
                return x, y
        # Hunt(w/ parity) Mode
        else:
            pos_e = [
                (pos[0], pos[1]) for pos in self._even_moves if pos in self._moves_left
            ]
            if pos_e:
                pos_x, pos_y = pos_e[randint(0, len(pos_e) - 1)]
            else:
                pos_x, pos_y = self._moves_left[randint(0, len(self._moves_left) - 1)]
            return pos_x, pos_y

    # All Following Functions are part of Hard Difficulty
    def __check_delta_moves(self, coord, magnitude):
        """
        This function checks all the adjacent tiles around the given cords,
        it then checks to see if they are valid moves. If there is any invalid move
        in a set of cords it does not put them into the list.

        See Old_AI.txt if issues with AI: Hard.

        :param coord: Pass cords to be checked
        :param magnitude: Pass how far out from cords you want to check
        :return: Returns a list of all adjacent cords
        """

        def _gen_move(delta_start, mag):
            mag -= 1
            while True:
                yield (delta_start[0] * mag, delta_start[1]) if abs(
                    delta_start[0]
                ) else (delta_start[0], delta_start[1] * mag)
                mag -= 1
                if not mag:
                    break

        return self.__flatten(
            [
                moves
                for moves in [
                    [
                        (coord[0] + move[0], coord[1] + move[1])
                        for move in (
                            (delta[0] * mag, delta[1] * mag)
                            for mag in range(1, magnitude)
                        )
                        if (coord[0] + move[0], coord[1] + move[1]) in self._moves_left
                    ]
                    for delta in self.__delta_move
                ]
                if len(moves) == magnitude - 1
            ]
        )

    def __valid_attack_move(self, coord):
        """
        This function creates a list using the _check_delta_moves Method to create a list
        of cords that all player ships that can start at a give cord.
        :param coord: Cord to be checked
        """

        ships_left = [
            values[1] for ship, values in self.vs_ship_left.items() if not values[0]
        ]
        hold = []
        for i in ships_left:
            hold.append(self.__check_delta_moves(coord, i))
        hold2 = self.__flatten(hold)
        for cord in hold2:
            self._point_map[cord] += 1
        self._point_map[coord] += 1

    def __check_all_moves(self):
        """
        This Method calls the _valid_attack_move Method for all cords in the move_left list.
        :return:
        """
        for c_x, c_y in self._moves_left:
            self.__valid_attack_move((c_x, c_y))

    def __best_move(self):
        """
        This function determine all tiles with the most points and returns a random value from that list.
        :return: Returns the highest score tile
        """
        max_value = max(self._point_map.values())
        best_moves = [
            key for key in self._point_map.keys() if self._point_map[key] == max_value
        ]
        return best_moves[randint(0, len(best_moves)) - 1]

    def __remove_move(self, coord):
        """
        This function removes a coord from _moves_left.
        :param coord: Cord to be removed
        """
        self._moves_left.remove(coord)

    def __reset_point_map(self):
        """
        This Method resets all points on teh point map to 0
        """
        if self.save_point_map:
            self._save_ai_point_board()
        self._point_map = {
            (x, y): 0
            for x in range(1, self.sides + 1)
            for y in range(1, self.sides + 1)
        }

    def __check_adj_tiles(self, map_to_check):
        """
        This method returns all adjacent tiles that are still in moves left.
        :param map_to_check: The set of tiles to be checked.
        :return: Returns list of adjacent tiles that are valid
        """
        print(map_to_check, "Map to check")
        return [
            (x1 + d_x, y1 + d_y)
            for x1, y1 in map_to_check
            for d_x, d_y in self.__delta_move
            if (x1 + d_x, y1 + d_y) in self._moves_left
        ]

    def __adjust_for_hits(self):
        """
        This function adds points to the point map for all spaces adjacent to hit tiles if valid.
        """

        adj_pos_moves = self.__flatten(
            [
                cords
                for cords in [
                    self.__check_delta_moves(move, 2) for move in self._hit_map
                ]
            ]
        )
        for cord in adj_pos_moves:
            self._point_map[cord] += 2

    def __adjust_last_hit(self):
        """
        This function adds points to the point map around the spaces of the last hit.
        """
        moves = [
            cord
            for cord in [
                (c_x + self._last_hit[0], c_y + self._last_hit[1])
                for c_x, c_y in self.__delta_move
            ]
            if cord in self._moves_left
        ]
        for move in moves:
            self._point_map[move] += 5

    def __hard_difficulty(self):
        """
        Hard Difficulty AI: Currently wins at ~61.82 moves after 1000+ games of testing
        """
        self.__reset_point_map()
        self.__check_all_moves()
        self.__adjust_for_hits()
        # Hunt Mode
        if not self._hit_state:
            return self.__best_move()
        # Target mode
        elif self._hit_state:
            self.__adjust_last_hit()
            return self.__best_move()

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
            a_x, a_y = self.__easy_difficulty()
        elif self.difficulty == 1:
            a_x, a_y = self.__med_difficulty()
        elif self.difficulty == 2:
            a_x, a_y = self.__hard_difficulty()

        self._moves_left.remove((a_x, a_y))

        if (a_x, a_y) in self._moves_left:
            print("FAIL at %s,%s" % (a_x, a_y))

        if "Water" in opposition_player.storedBoard[a_x, a_y]:
            # print(out_put_data[5] % (a_x, a_y))
            opposition_player.storedBoard[a_x, a_y] = "Missed"
            self.misses += 1
            self._hit_state = False

        else:
            for ship in range(len(opposition_player.fleet)):
                if (
                    opposition_player.storedBoard[a_x, a_y]
                    in opposition_player.fleet[ship].get_name()
                ):
                    if Display:
                        print(out_put_data[6] % (a_x, a_y))
                    opposition_player.storedBoard[a_x, a_y] += "Damaged"
                    self.hits += 1
                    check_sink(opposition_player, opposition_player.fleet[ship])
                    check_win(self)
                    self._hit_map.append((a_x, a_y))
                    self._hit_state = True
                    self._last_hit = (a_x, a_y)

    def _save_ai_point_board(self):
        try:
            with open(
                join_(
                    path_gamedata_pointmaps_,
                    "%s_%s_%s.txt" % (self.p_number, _game_number, id(self.playerType)),
                ),
                "a+",
            ) as file:
                file.write("{'turn_%s': %s}\n" % (turns, str(self._point_map)))
        except FileNotFoundError:
            open(
                join_(
                    path_gamedata_pointmaps_,
                    "%s_%s_%s.txt" % (self.p_number, _game_number, id(self.playerType)),
                ),
                "w+",
            ).close()
            self._save_ai_point_board()


def _start_game(display=True, override=False, wait_x=1):
    """
    This function is used to control the game.
    :param wait_x: Inter-function Variable
    """
    global start
    start = time.time()
    global p1
    global p2
    global turns
    global Display
    global _game_number
    Display = display
    _create_dirs()
    _create_master_game_number(override=override)
    display__start = Display
    if not display__start:
        p1 = AI(
            difficulty=Difficulty,
            type_player="Machine_1",
            point_map_state=(True if Save_Point_Maps else False),
            p_number=1,
        )
        p1.fleet_gen()
        p2 = AI(
            difficulty=Difficulty,
            type_player="Machine_2",
            point_map_state=(True if Save_Point_Maps else False),
            p_number=2,
        )
        p2.fleet_gen()
    elif display__start:
        one = ask_type(1)
        if one:
            p1 = Player(type_player="Man", p_number=1)
        else:
            p1 = AI(
                difficulty=Difficulty,
                type_player="Machine_1",
                point_map_state=(True if Save_Point_Maps else False),
                p_number=1,
            )
            p1.playerType = "Machine"
        p1.fleet_gen()
        two = ask_type(2)
        if two:
            p2 = Player(type_player="Man", p_number=2)
        else:
            p2 = AI(
                difficulty=Difficulty,
                type_player="Machine_2",
                point_map_state=(True if Save_Point_Maps else False),
                p_number=2,
            )
        p2.fleet_gen()
        input(out_put_data[14])
    while wait_x:
        while True:
            try:
                if turns % 2 == 0:
                    if display__start:
                        print(out_put_data[15])
                    p1.attack_player(p2)
                    turns += 1
                    if display__start:
                        p2.print_masked_board()
                        print(out_put_data[16] % ("Two", turns))
                elif turns % 2 != 0:
                    if display__start:
                        print(out_put_data[17])
                    p2.attack_player(p1)
                    turns += 1
                    if display__start:
                        p1.print_masked_board()
                        print(out_put_data[16] % ("One", turns))
            except GameWin:
                wait_x -= 1
                if Display:
                    if turns % 2 == 0:
                        p2.print_masked_board()
                    if turns % 2 != 0:
                        p1.print_masked_board()
                return False


if __name__ == "__main__":
    Profile = input(out_put_data[19])
    Save = input(out_put_data[26])
    # Profile = 1
    if Save == 1:
        Save_Stats = False
        Save_Point_Maps = False
    if Profile == 1:
        Display = False

        def run_lot():
            for x in range(1):
                _start_game(display=False)
                if x % 10 == 0:
                    print(x)

        cProfile.run("run_lot()")
    else:
        _start_game()
