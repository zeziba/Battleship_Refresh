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

    def update_hits(self):
        self.hit(test_point[0], test_point[1])


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


size = int(defaultconfig["board size"])


class testplayer:
    pass


class TestMethodsBoardManager(unittest.TestCase):
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
        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        self.assertIs(type(b), boardmanager.BoardManager)

    def test_board(self):
        __board = {"display": list(), "ships": list(), "point map": list()}

        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        self.assertEqual(b.board, __board)

    def test_add_boat(self):
        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        self.assertIsNone(b.add_ship(testboat(test_point)))

    def test_display(self):
        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        b.add_ship(testboat(test_point))

        b.update_display()

        tmap = ["~" * 10 for _ in range(10)]
        self.assertEqual(b.display, tmap)

        # Tests the hit markers
        b.board["ships"][0].update_hits()

        b.update_display()

        t = list(tmap[test_point[0]])
        t[test_point[1]] = "X"
        tmap[test_point[0]] = "".join(t)

        self.assertEqual(tmap, b.display)

    def test_point_map(self):
        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        self.assertEqual(b.point_map, list())

        b.add_ship(testboat(defaultconfig))

        b.update_display()
        b.update_point_map()

        tmap = [[1 for _ in range(10)] for _ in range(10)]

        self.assertEqual(b.point_map, tmap)

    def test_size(self):
        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        self.assertEqual(b.size, defaultconfig["board size"])

    def test_reset(self):
        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        b.add_ship(testboat(test_point))

        b.update_display()
        b.update_point_map()

        self.assertEqual(b.point_map, [[1 for _ in range(10)] for _ in range(10)])

        b.reset()

        self.assertEqual(b.point_map, list())

    def test_iter(self):
        from src import boardmanager

        b = boardmanager.BoardManager(defaultconfig, testplayer())

        b.add_ship(testboat(test_point))
        b.update_display()

        for row in b:
            self.assertEqual("~" * b.size, row)
