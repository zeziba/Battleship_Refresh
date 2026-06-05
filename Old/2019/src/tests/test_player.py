import sys
import unittest

defaultconfig = {
    "base location": "",
    "config file": "config.ini",
    "board size": 10,
    "ship count": 5,
    "ships": """"Battleship":1,"Carrier":1,"Patrol Boat":1,"Submarine":1,"Destroyer":1""",
    "Battleship": 4,
    "Carrier": 5,
    "Patrol Boat": 2,
    "Submarine": 3,
    "Destroyer": 3,
}

test_point = [1, 1]
WATERSYMBOL = "~"
size = int(defaultconfig["board size"])


class testboat:
    def __init__(self, tp):
        self.tp = tp
        self.__hits = []

    def hit(self, x, y):
        if x == self.tp[0] and y == self.tp[1]:
            self.__hits.append([x, y])
            return True
        return False

    @property
    def sunk(self):
        return False

    @property
    def hits(self):
        return self.__hits

    @property
    def symbol(self):
        return "B"


class testboard:
    def __init__(self, tb):
        self.__board = {
            "display": list(),
            "ships": list(),
            "point map": [[0 for _ in range(10)] for _ in range(10)],
        }
        self.__board["ships"].append(tb)
        self.config = defaultconfig

    @property
    def board(self):
        return self.__board

    @property
    def ships(self):
        return self.board["ships"]

    @property
    def size(self):
        return defaultconfig["board size"]

    @property
    def point_map(self):
        return self.__board["point map"]

    @property
    def display(self):
        return self.board["display"]

    @property
    def size(self):
        return size

    def update_display(self):
        self.__board["display"] = [
            WATERSYMBOL * self.config["board size"]
            for _ in range(self.config["board size"])
        ]
        for ship in self.board["ships"]:
            symbol = "X" if not ship.sunk else ship.symbol if ship.sunk else WATERSYMBOL
            for hit in ship.hits:
                t = list(self.__board["display"][hit[0]])
                t[1] = symbol
                self.__board["display"][hit[0]] = "".join(t)

    def update_point_map(self):
        self.update_display()
        self.__board["point map"] = list()
        for row in self.board["display"]:
            self.__board["point map"].append(
                [0 if x is not WATERSYMBOL else 1 for x in row]
            )
            # TODO: Add ships that are sunk to the board


class TestMethodsPlayer(unittest.TestCase):
    class MyOut(object):
        def __init__(self):
            self.data = []

        def write(self, s):
            self.data.append(s)

        def flush(self):
            self.data = []

        def getvalue(self):
            return self.data

        def __str__(self):
            return "".join(self.data)

    def test_import(self):
        correct_out = ""

        std_out = sys.stdout
        out = self.MyOut()
        try:
            sys.stdout = out
            from src import playermanager
        finally:
            sys.stdout = std_out

        self.assertEqual(correct_out, str(out))

    def test_player(self):
        from src import playermanager

        p = playermanager.Player(None, None, defaultconfig)

        correct_out = "True\n"
        false_out = "False\n"

        for pos in range(size ** 2):
            std_out = sys.stdout
            out = self.MyOut()
            sys.stdout = out
            print(
                p.fire_shot(
                    board=testboard(testboat(test_point)),
                    x=(pos % size),
                    y=(pos // size),
                )
            )
            sys.stdout = std_out
            self.assertEqual(
                correct_out
                if (pos % size) == test_point[0] and (pos // size) == test_point[1]
                else false_out,
                str(out),
            )

    def test_place_boats(self):
        # TODO: Have to finalize how ships are placed in ship manager before this test can be conducted.
        pass

    def test_AI(self):
        from src import playermanager

        b = testboard(testboat(test_point))
        ai = playermanager.AI(b, defaultconfig, "easy")

    def test_AI_adjacent_cells(self):
        from src import playermanager

        b = testboard(testboat(test_point))
        ai = playermanager.AI(b, defaultconfig, "easy")

        correct_out = "0\n"

        for pos in range(size ** 2):
            std_out = sys.stdout
            out = self.MyOut()
            sys.stdout = out
            print(ai._get_adjacent_cells((pos % size), (pos // size), b))
            sys.stdout = std_out
            self.assertEqual(correct_out, str(out))

    def test_AI_fire_shot(self):
        from src import playermanager

        b = testboard(testboat(test_point))
        ai = playermanager.AI(b, defaultconfig, "easy")

        self.assertIsInstance(ai.fire_shot(board=b), bool)
