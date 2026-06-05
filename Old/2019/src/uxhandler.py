import os

import boardmanager

FILENAME = "output.txt"


class UXHandle:
    def __init__(self, config):
        self.config = config
        self.out = dict()
        self.load()

    def load(self):
        filename = os.path.join(self.config["base location"], FILENAME)
        with open(filename, "r") as file:
            for line in file:
                data = line.split(":")
                self.out[data[0]] = data[1]

    def get(self, option):
        return self.config[option]

    def get_input(self, out="get input num"):
        return str(input(out if out != "get input name" else self.out[out]))

    def display(self, data):
        print(data)

    @staticmethod
    def print_board(board, override=False):
        if not isinstance(board, boardmanager.BoardManager) and not override:
            raise TypeError()

        for row in board:
            print("".join("{:<2}" * int(board.size)).format(*row), sep="", end="\n")
