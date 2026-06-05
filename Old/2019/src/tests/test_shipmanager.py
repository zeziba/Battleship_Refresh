import sys
import unittest

defaultconfig = {
    "base location": "",
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
size = int(defaultconfig["board size"])


class testboat:
    def __init__(self, tp):
        self.tp = tp
        self.__hits = []
        self._sunk = False

    def hit(self, x, y):
        if x == self.tp[0] and y == self.tp[1]:
            self.__hits.append([x, y])
            return True
        return False

    @property
    def sunk(self):
        return self._sunk

    def flip(self):
        self._sunk = not self.sunk

    @property
    def hits(self):
        return self.__hits

    def update_hits(self):
        self.hit(test_point[0], test_point[1])

    @property
    def name(self):
        return "patrol boat"

    @property
    def positions(self):
        return [[0, 0], [0, 1]]

    @property
    def length(self):
        return 2


class malformedboat(testboat):
    @property
    def length(self):
        return 100


class testboard:
    def __init__(self, tb):
        self.__board = {
            "display": list(),
            "ships": list(),
            "point map": [[0 for _ in range(10)] for _ in range(10)],
        }
        self.__board["ships"].append(tb)

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

    def add_ship(self, ship):
        self.__board["ships"].append(ship)


class TestMethodsShipManager(unittest.TestCase):
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
            from src import shipmanager
        finally:
            sys.stdout = std_out

        self.assertEqual(correct_out, str(out))

    def test_name(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        self.assertEqual(s.name, name)

    def test_symbol(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        self.assertEqual(s.symbol, symbol)

    def test_hits(self):

        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        self.assertEqual(s.hits, list())

    def test_position(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        self.assertEqual(s.position, list())

    def test_length(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        self.assertEqual(s.length, defaultconfig[name])

    def test_reset(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        s.reset()

        self.assertEqual(s.position, list())
        self.assertEqual(s.hits, list())

    def test_create_ship(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        s.create_ship((0, 1), 0, 0)

        self.assertEqual(s.position, [[0, x * 1] for x in range(defaultconfig[name])])

    def test_hit(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        s.create_ship((0, 1), 0, 0)

        pos1 = (0, 1)
        pos2 = (5, 5)

        self.assertTrue(s.hit(*pos1))
        self.assertFalse(s.hit(*pos2))

    def test_sunk(self):
        from src import shipmanager

        name = "battleship"
        symbol = "B"
        s = shipmanager.ShipManager(defaultconfig, name, symbol)

        s.create_ship((0, 1), 0, 0)

        for i in range(defaultconfig[name]):
            self.assertTrue(s.hit(0, i))

        self.assertTrue(s.sunk())
