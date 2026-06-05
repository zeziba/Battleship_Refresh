import sys
import os
import unittest

defaultconfig = {
    "base location": os.path.dirname(os.path.dirname(__file__)),
    "config file": "config.ini",
    "board size": 10,
    "ship count": 5,
    "ships": """"Battleship":1,"Carrier":1,"Patrol Boat":1,"Submarine":1,"Destroyer":1""",
    "battleship": 4,
    "carrier": 5,
    "patrol boat": 2,
    "submarine": 3,
    "destroyer": 3,
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

    def __iter__(self):
        for row in self.display:
            yield row

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


class TestMethodsUXHandler(unittest.TestCase):
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
            from src import uxhandler
        finally:
            sys.stdout = std_out

        self.assertEqual(correct_out, str(out))

    def test_load(self):
        from src import uxhandler

        ux = uxhandler.UXHandle(defaultconfig)

        ux.load()

        self.assertIsInstance(ux.out, dict)

    def test_get(self):
        from src import uxhandler

        ux = uxhandler.UXHandle(defaultconfig)

        for key in defaultconfig.keys():
            self.assertEqual(ux.get(key), defaultconfig[key])

    def test_print_board(self):
        from src import uxhandler

        ux = uxhandler.UXHandle(defaultconfig)

        b = testboard(testboat(test_point))
        b.update_display()

        n = [
            "{:<2}".format("~") * defaultconfig["board size"]
            for _ in range(defaultconfig["board size"])
        ]
        n = "\n".join(n) + "\n"

        std_out = sys.stdout
        out = self.MyOut()
        try:
            sys.stdout = out
            ux.print_board(b, True)
        finally:
            sys.stdout = std_out

        self.assertEqual(str(out), n)
