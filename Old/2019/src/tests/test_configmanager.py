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


class TestMethodsConfigManager(unittest.TestCase):
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
        from src import configmanager
        import configparser

        c = configmanager.ConfigManager()

        self.assertIsInstance(c.configfile, str)
        self.assertIsInstance(c.config, configparser.ConfigParser)

    def test_create(self):
        from src import configmanager

        c = configmanager.ConfigManager()

        c.create()

        import os

        file = os.path.join(
            configmanager.defaultconfig["settings"]["base location"],
            configmanager.defaultconfig["settings"]["config file"],
        )
        self.assertTrue(os.path.exists(file))

        os.remove(file)

        self.assertFalse(os.path.exists(file))

    def test_open(self):
        import os
        from src import configmanager

        file = os.path.join(
            configmanager.defaultconfig["settings"]["base location"],
            configmanager.defaultconfig["settings"]["config file"],
        )

        if os.path.exists(file):
            os.remove(file)

        c = configmanager.ConfigManager()

        correct_out = "File not found, creation of file is required!\n"

        std_out = sys.stdout
        out = self.MyOut()
        try:
            sys.stdout = out
            c.open()
        finally:
            sys.stdout = std_out

        self.assertEqual(correct_out, str(out))

        c.create()
        self.assertTrue(c.open())
        self.assertTrue(os.path.exists(file))

        if os.path.exists(file):
            os.remove(file)

        self.assertFalse(os.path.exists(file))
        self.assertFalse(c.open())

    def test_get_config(self):
        import os
        from src import configmanager

        file = os.path.join(
            configmanager.defaultconfig["settings"]["base location"],
            configmanager.defaultconfig["settings"]["config file"],
        )

        if os.path.exists(file):
            os.remove(file)

        c = configmanager.ConfigManager()
        c.create()
        c.open()

        self.assertEqual(c.get_config().keys(), configmanager.defaultconfig.keys())

        self.assertIsInstance(c.get_config("settings"), dict)

        if os.path.exists(file):
            os.remove(file)

    def test_str(self):
        import os
        from src import configmanager

        file = os.path.join(
            configmanager.defaultconfig["settings"]["base location"],
            configmanager.defaultconfig["settings"]["config file"],
        )

        if os.path.exists(file):
            os.remove(file)

        c = configmanager.ConfigManager()
        c.create()
        c.open()

        correct_out = configmanager.defaultconfig

        std_out = sys.stdout
        out = self.MyOut()
        try:
            sys.stdout = out
            print(c)
        finally:
            sys.stdout = std_out

        # Calculate number of ints in default config and then multiply by 2 add 1 for the \n char
        offset = (
            sum(
                [
                    1
                    for key in configmanager.defaultconfig["settings"].keys()
                    if isinstance(configmanager.defaultconfig["settings"][key], int)
                ]
            )
            * 2
            + 1
        )
        self.assertEqual(len(str(correct_out)) + offset, len(str(out)))

        if os.path.exists(file):
            os.remove(file)
