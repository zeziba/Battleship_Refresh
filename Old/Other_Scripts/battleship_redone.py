__author__ = "Charles Engen"
__version__ = "1.0.0"
__date__ = "Friday, September 11, 2015"

"""
This will be a full implantation of the game Battleship

TODO:
    Board
    Players
    Statistics
    AI
    Attack Abilities
    Check Game State win/loss
    Check ship sink
    A GUI
"""

import tkinter as tk
from collections import OrderedDict
from random import randint


class GameException(BaseException):
    pass


def askXY(direction="", player=False):
    if player:
        return int(input("Pick a %snumber 1-10") % direction)


class Board(object):
    def __init__(self, sides=10):
        self.board = {
            (x, y): "water" for x in range(1, sides + 1) for y in range(1, sides + 1)
        }

    def return_board(self):
        return OrderedDict(sorted(self.board.items()))


class MainFrame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.ship_list = [{"Battleship": 3}, {"Patrol Boat": 2}]

        self.board_data = Board()

        self.current_ship_state = tk.StringVar()

        self.board_text = tk.StringVar()
        self.board = tk.Label(self, textvariable=self.board_text)

        self.frame = tk.Frame(self)
        self.frame.pack()
        self.title("Battleship")

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.sub_file_item = tk.Menu(self.file_menu)
        self.menu.add_cascade(label="File", menu=self.sub_file_item)

        self.sub_file_item.add_command(label="Quit", command=self.destroy)

        self.a = self.board_data.return_board()
        for x, y in self.a:
            self.aButton = tk.Button(
                self.frame,
                text=self.a[x, y][0],
                command=lambda: self.set_board(self.current_ship_state.get()),
            )
            self.aButton.grid(row=x, column=y)
            print(self.aButton)

        self.board.pack()
        self.board_text.set("Nothing yet")

        self.frame_side = tk.Frame()
        self.frame_side.pack(side="right")

        for boat in self.ship_list:
            for boat_name in boat:
                self.bButton = tk.Button(
                    self.frame_side,
                    text=boat_name,
                    command=lambda: self.set_current_ship_select(boat_name),
                )
                self.bButton.pack()

    def set_board(self, ship):
        self.board_text.set(ship)
        self.aButton["text"] = ship[0]

    def set_current_ship_select(self, ship):
        self.current_ship_state.set(ship)


if __name__ == "__main__":
    root = MainFrame()
    root.mainloop()
