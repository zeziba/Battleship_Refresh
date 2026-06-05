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


size = int(defaultconfig["board size"])


class TestMethodsGameManager(unittest.TestCase):
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
            from src import gamemanager
        finally:
            sys.stdout = std_out

        self.assertEqual(correct_out, str(out))

    def test_state(self):
        from src import gamemanager

        g = gamemanager.GameManager(defaultconfig)

        self.assertFalse(g.state)

    def test_reset(self):
        from src import gamemanager

        g = gamemanager.GameManager(defaultconfig)

        self.assertFalse(g.state)
        g.reset()
        self.assertFalse(g.state)

    def test_check_win(self):
        from src import gamemanager

        g = gamemanager.GameManager(defaultconfig)

        b = testboard(testboat(test_point))

        self.assertFalse(g.check_win(b, True))

        b.ships[0].flip()

        self.assertTrue(g.check_win(b, True))

        # Test malformed board
        with self.assertRaises(TypeError) as context:
            g.check_win(b)

        self.assertTrue("Not a board object" == str(context.exception))

        with self.assertRaises(Exception) as context:
            b.add_ship(malformedboat(test_point))
            g.check_win(b, True)

        self.assertTrue("Board is malformed" == str(context.exception))

        with self.assertRaises(Exception) as context:
            b = testboard(testboat(test_point))
            for _ in range(10):
                b.add_ship(testboat(test_point))

            g.check_win(b, True)

        self.assertTrue(
            "Too many ships present on the board!" == str(context.exception)
        )

    def test_check_if_valid(self):
        pass
