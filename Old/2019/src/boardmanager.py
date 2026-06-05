import shipmanager

WATERSYMBOL = "~"


class BoardManager:
    def __init__(self, config, player):
        self.config = config
        self.player = player
        # TODO: Check if player or other is asking for information and morph output based on it

        self.__board = {"display": list(), "ships": list(), "point map": dict()}

    @property
    def board(self):
        return self.__board

    @property
    def point_map(self):
        return self.board["point map"]

    @property
    def point_map_iter(self):
        for key in self.point_map.keys():
            yield self.point_map[key]

    @property
    def ships(self):
        return self.board["ships"]

    @property
    def display(self):
        return self.board["display"]

    @property
    def size(self):
        return int(self.config["board size"])

    @property
    def hits(self):
        return [pos for pos in [ship.hits for ship in self.ships if not ship.sunk()]]

    def add_ship(self, ship: type(shipmanager.ShipManager)):
        self.__board["ships"].append(ship)

    def validate_board(self):
        """
        Method looks to ensure that no ship overlaps.
        :return: True/False is ships overlap
        """
        if not self.ships:
            return True
        total = sum(ship.length for ship in self.ships)
        positions = []
        for ship in self.ships:
            for pos in ship.position:
                if pos not in positions:
                    positions.append(pos)
        if total != len(positions):
            return False
        return True

    def __iter__(self):
        # The below should output the display board
        for row in self.board["display"]:
            yield row

    def reset(self):
        self.__board = {"display": list(), "ships": list(), "point map": dict()}

    def update_display(self):
        self.__board["display"] = [
            [WATERSYMBOL for _ in range(self.size)] for _ in range(self.size)
        ]
        for x, y in self.player.fired:
            self.__board["display"][x][y] = "*"
        for ship in self.board["ships"]:
            symbol = (
                "X" if not ship.sunk() else ship.symbol if ship.sunk else WATERSYMBOL
            )
            for x, y in ship.hits:
                self.__board["display"][x][y] = symbol

        self.__board["display"] = ["".join(row) for row in self.display]

    def update_point_map(self):
        self.update_display()
        self.__board["point map"] = dict()
        for index, x in enumerate(self.board["display"]):
            self.__board["point map"][index] = dict()
            for _index, y in enumerate(x):
                self.__board["point map"][index][_index] = 1 if y is WATERSYMBOL else 0
