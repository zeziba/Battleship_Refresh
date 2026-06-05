import sys
import unittest


class TestMethodsMain(unittest.TestCase):
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
            from src import main
        finally:
            sys.stdout = std_out

        self.assertEqual(correct_out, str(out))

    def test_start(self):
        correct_out = ""

        std_out = sys.stdout
        out = self.MyOut()
        try:
            sys.stdout = out
            from src import main

            b = main.Battleship()
            b.start()
        finally:
            sys.stdout = std_out

        self.assertEqual(correct_out, str(out))
