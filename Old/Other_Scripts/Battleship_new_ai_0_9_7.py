__author__ = "Charles Engen"

# All the imports that are needed
from collections import OrderedDict
from random import randint
import cProfile

# These are the globals
p1 = None
p2 = None
Display = False
turns = 0
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
    18: "Your accuracy was %s",
}


def ask_xy(player=False):
    if player:
        return int(input(responses[3]))
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
        pass
    else:
        return randint(0, 1)


def ask_type(player, valid=False):
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
                boat.__dict__["sunk"] = True
                return True


def check_win(player1):
    if player1.hits == 17:
        raise GameWin(player1)


# These Two Classes are Custom Errors to catch specific events
class ShipError(BaseException):
    pass


class GameWin(BaseException):
    def __init__(self, player1):
        self.hits = player1.hits
        self.misses = player1.misses
        self.print_accuracy()

    def print_accuracy(self):
        total = self.hits + self.misses
        print(responses[18] % (self.hits / total))
        if Save_Accuracy:
            with open("score_data.txt", "a") as file:
                file.write("\n%s" % str(self.hits / total))
        global turns
        turns = 0


class ShipBlueprint(object):
    def __init__(self, ship_length, ship_name, sunk):
        self.shipLength = ship_length
        self.shipName = ship_name
        self.sunk = sunk

    def get_name(self):
        return self.__dict__["shipName"]

    def get_length(self):
        return self.__dict__["shipLength"]

    def __str__(self):
        return "%s is %s tiles long." % (
            self.__dict__["shipName"],
            self.__dict__["shipLength"],
        )

    def __call__(self):
        return self.sunk


class Board(object):
    def __init__(self, size=10):
        self.sides = size
        self.startBoard = {
            (x, y): "~Water"
            for y in range(1, self.sides + 1)
            for x in range(1, self.sides + 1)
        }
        self.backedup_board = self.startBoard
        self.storedBoard = dict()

    def print_board(self):
        printable_board = OrderedDict(sorted(self.startBoard.items()))
        for y in range(1, self.sides):
            print(" ".join(str(printable_board[x, y])[0] for x in range(1, self.sides)))

    def print_masked_board(self, nonprint=False):
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
        def revert_board():
            self.startBoard = dict(self.backedup_board)
            return self.startBoard

        if revert:
            revert_board()
        else:
            self.backedup_board = dict(self.startBoard)
            return self.backedup_board

    def final_board(self):
        self.storedBoard = self.startBoard
        return self.storedBoard


class Player(Board):
    def __init__(self, type_player):
        Board.__init__(self)
        self.playerType = type_player
        self.misses = 0
        self.hits = 0
        self.fleet = [
            ShipBlueprint(5, "Aircraft Carrier", False),
            ShipBlueprint(4, "Battleship", False),
            ShipBlueprint(3, "Submarine", False),
            ShipBlueprint(3, "Destroyer", False),
            ShipBlueprint(2, "Patrol Boat", False),
        ]

    def attack_player(self, opposition_player):
        def get_cords():
            return ask_xy(player=True), ask_xy(player=True)

        while True:
            try:
                i_x, i_y = get_cords()
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
        if "Water" not in self.startBoard[pos_x, pos_y]:
            raise StopIteration()
        else:
            self.startBoard[pos_x, pos_y] = ship.get_name()

    def ship_gen(self, ship, pos_x, pos_y, h_v):
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

    def __str__(self, *args, **kargs):
        return responses[13] % self.playerType


class AI(Player):
    def __init__(self, difficulty, type_player):
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
        pos_x, pos_y = self.moves_left[randint(0, len(self.moves_left))]
        return pos_x, pos_y

    def med_difficulty(self):
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
        for c_x, c_y in self.moves_left:
            self.valid_attack_move((c_x, c_y))

    def best_move(self):
        max_value = max(self.point_map.values())
        best_moves = [
            key for key in self.point_map.keys() if self.point_map[key] == max_value
        ]
        return best_moves[randint(0, len(best_moves)) - 1]

    def remove_move(self, coord):
        self.moves_left.remove(coord)

    def reset_point_map(self):
        self.point_map = {
            (x, y): 0
            for x in range(1, self.sides + 1)
            for y in range(1, self.sides + 1)
        }

    def check_adj_tiles(self, map_to_check):
        return [
            (x1 + d_x, y1 + d_y)
            for x1, y1 in map_to_check
            for d_x, d_y in self.delta_move
            if (x1 + d_x, y1 + d_y) in self.moves_left
        ]

    def adjust_for_hits(self):
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
                    # print(out_put_data[6] % (opposition_player.fleet[ship].get_name(), a_x, a_y))
                    opposition_player.storedBoard[a_x, a_y] += "Damaged"
                    self.hits += 1
                    check_sink(opposition_player, opposition_player.fleet[ship])
                    check_win(self)
                    self.hit_map.append((a_x, a_y))
                    self.hit_state = True
                    self.last_hit = (a_x, a_y)


def _start_game(x=1):
    global p1
    global p2
    global turns
    global Display
    display__start = Display
    if not display__start:
        p1 = AI(difficulty=2, type_player="Machine")
        p1.fleet_gen()
        p2 = AI(difficulty=2, type_player="Machine")
        p2.fleet_gen()
    elif display__start:
        one = ask_type(1)
        if one:
            p1 = Player(type_player="Man")
        else:
            p1 = AI(difficulty=2, type_player="Machine")
            p1.playerType = "Machine"
        p1.fleet_gen()
        two = ask_type(2)
        if two:
            p2 = Player(type_player="Man")
        else:
            p2 = AI(difficulty=2, type_player="Machine")
        p2.fleet_gen()
        input(responses[14])
    while x:
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
                x -= 1
                return False


if __name__ == "__main__":
    for x in range(10):
        if x % 10 == 0:
            print(x)
        # cProfile.run('_start_game()')
        _start_game()
