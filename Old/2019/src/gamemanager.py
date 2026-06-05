import random

import boardmanager
import playermanager
import shipmanager


class GameManager:
    def __init__(self, config):
        self.config = config
        self.__size = int(self.config["board size"])

        self.__state = False

    @property
    def state(self):
        return self.__state

    def reset(self):
        self.__state = False

    def check_win(self, board, override=False):
        if not override:
            if not isinstance(board, boardmanager.BoardManager):
                raise TypeError("Not a board object")

        ship_count = int(self.config["ship count"])
        if len(board.board["ships"]) > ship_count:
            raise Exception("Too many ships present on the board!")

        if not self.check_if_valid(board):
            raise Exception("Board is malformed")

        if all(boat.sunk() for boat in board.ships):
            self.__state = True
            return True
        return False

    @staticmethod
    def _m(ship1, ship2):
        if ship1[0] == ship2[0]:
            return float("inf")
        return (ship2[1] - ship1[1]) / (ship2[0] - ship1[0])

    def _check_if_in_bounds(self, ship):
        if (
            ship[0] < 0
            or ship[1] < 0
            or ship[0] > int(self.config["board size"])
            or ship[1]
        ):
            return False
        return True

    def _check_ship_is_valid(self, ship):
        m = self._m(ship.position[0], ship.position[1])

        x0, y0 = ship.position[0][0], ship.position[0][1]

        for pos in ship.position:
            if pos == ship.position[0]:
                continue
            self._check_if_in_bounds(pos)
            n_m = self._m(ship.position[0], pos)
            if m != n_m and n_m != float("inf") and n_m != 0:
                return False
            if pos[0] - x0 > ship.length or pos[1] - y0 > ship.length:
                return False
        if len(set([tuple(pos) for pos in ship.position])) != ship.length:
            return False
        return True

    def check_if_valid(self, board):
        # Check if the board is valid, display board is not checked.
        # Does this by checking if the correct number of ships is present then checks the position of each.
        # Checks if a player has won the game and returns a value based on that information
        ships_available = {
            i.split(":")[0].lower().replace('"', ""): int(i.split(":")[1])
            for i in self.config["ships"].split(",")
        }
        ship_data = {ship.name: 0 for ship in board.ships}

        # Check if ships are inside the board along with number of each type
        for ship in board.ships:
            ship_data[ship.name] += 1

        for ship in board.ships:
            if int(ship_data[ship.name]) != int(ships_available[ship.name]):
                return False

            if not self._check_ship_is_valid(ship):
                return False

        return True

    def allow_player_place_boats(self, **kwargs):
        """
        :param kwargs:
            :kwargs player: Required, playermanager.Player | playermanager.AI
            :kwargs board:  Required, boardmanager.Board
            :kwargs ux:     Required, allows this method to output to screen
            :kwargs dirs:   Required, playermanager.DIRS
        :return: True/False of success
        """
        player = kwargs["player"]
        ux = kwargs["ux"]
        boats = [ship for ship in player.ship_names]
        board = kwargs["board"]
        dirs = kwargs["dirs"]
        while boats:
            boat = boats[-1]
            # get Dir and (x, y) for boat, NO checking is done right now
            # TODO: Check if boat is valid here and make player retry
            if isinstance(player, playermanager.AI):
                _dir = random.choice(dirs)
                x, y = random.randint(
                    0, int(self.config["board size"])
                ), random.randint(0, int(self.config["board size"]))
            else:
                # TODO: Add GUI to place boats, would be easier and make more sense here.
                try:
                    ux.display(ux.out["placement"].format(boat))
                    _dir = dirs[int(ux.get_input(ux.out["get dir"]))]
                    _out = ux.out["get input num"].format(
                        0, int(self.config["board size"]) - 1
                    )
                    x, y = int(ux.get_input(_out)), int(ux.get_input(_out))
                except ValueError:
                    ux.display(ux.out["failed input"])
                    continue
            if (
                x + int(self.config[boat]) > self.__size
                or y + int(self.config[boat]) > self.__size
            ):
                continue
            if any(b.special_check(x, y) for b in board.ships) or any(
                [x < 0, x > int(self.__size), y < 0, y > int(self.__size)]
            ):
                ux.display(ux.out["failed input"])
                continue
            s = shipmanager.ShipManager(self.config, boat, boat[0])
            s.create_ship(_dir=_dir, x0=x, y0=y)
            board.add_ship(s)
            boats.pop(-1)

    def game(self, **kwargs):
        """
        :param kwargs:
            :kwargs player1: playermanager.Player | playermanger.AI
            :kwargs player2: playermanager.AI
            :kwargs player1_board: boardmanager.BoardManager
            :kwargs player2_board: boardmanager.BoardManager
            :kwargs ux: uxhandler.UXHandler
        :return: None
        """
        ux = kwargs["ux"]

        p1 = kwargs["player1"]
        p2 = kwargs["player2"]

        p1_b = kwargs["player1_board"]
        p2_b = kwargs["player2_board"]

        # Start placing boats.
        ux.display(ux.out["game start"])

        self.allow_player_place_boats(
            player=p1, board=p1_b, ux=ux, dirs=list(playermanager.DIRS.values())
        )
        while not p1_b.validate_board():
            p1_b.reset()
            self.allow_player_place_boats(
                player=p1, board=p1_b, ux=ux, dirs=list(playermanager.DIRS.values())
            )
        self.allow_player_place_boats(
            player=p2, board=p2_b, ux=ux, dirs=list(playermanager.DIRS.values())
        )
        while not p2_b.validate_board():
            p2_b.reset()
            self.allow_player_place_boats(
                player=p2, board=p2_b, ux=ux, dirs=list(playermanager.DIRS.values())
            )

        while not self.check_win(p1_b) and not self.check_win(p2_b):
            p, _p = (
                ((p1, p1_b), (p2, p2_b))
                if p1.turn < p2.turn
                else ((p2, p2_b), (p1, p1_b))
            )
            ux.display(ux.out["turn"].format(p[0].name, p[0].turn + 1))

            if not isinstance(p[0], playermanager.AI):
                x, y = ux.get_input(), ux.get_input()
                if 0 > x > self.__size and 0 > y > self.__size:
                    continue
                try:
                    if p[0].fire_shot(board=_p[1], x=int(x), y=int(y)):
                        ux.display(ux.out["attack success"].format(x, y))
                    else:
                        ux.display(ux.out["attack failed"].format(x, y))
                except shipmanager.ShipException:
                    ux.display(ux.out["attack repeat"].format(x, y))
                except playermanager.PlayerAlreadyShotError:
                    ux.display(ux.out["attack repeat"].format(x, y))
                except shipmanager.ShipSunkError as error:
                    ux.display(ux.out["attack sunk"].format(error.args, x, y))
            else:
                try:
                    if p[0].fire_shot(board=p[1]):
                        ux.display(
                            ux.out["attack success"].format(
                                p[0].fired[-1][0], p[0].fired[-1][1]
                            )
                        )
                    else:
                        ux.display(
                            ux.out["attack failed"].format(
                                p[0].fired[-1][0], p[0].fired[-1][1]
                            )
                        )
                except shipmanager.ShipSunkError as error:
                    ux.display(
                        ux.out["attack sunk"].format(
                            error.args, p[0].fired[-1][0], p[0].fired[-1][1]
                        )
                    )

            p[1].update_display()
            ux.display("\n".join("{:<2}".format(d) for d in p[1].display))
            if p[0].turn == 500:
                break
        ux.display(ux.out["win"] if self.check_win(p1_b) else ux.out["loss"])
