__author__ = "Charles Engen"

import tkinter
from os.path import join as join_
from os import getcwd
from os import listdir
import re

_path = getcwd()
_path_gamedata = join_(_path, "GameData")
_path_gamedata_pointmaps = join_(_path_gamedata, "point_maps")

point_map = {(x, y): None for x in range(1, 11) for y in range(1, 11)}


class PointMaps(object):
    def __init__(self):
        self.point_map_files = listdir(_path_gamedata_pointmaps)
        self.load_base_number = 1
        self.point_maps = dict()

    def load_point_map(self, file):
        with open(join_(_path_gamedata_pointmaps, file)) as file:
            temp = []
            for line in file:
                temp.append(eval(line))
            return temp

    def lowest_game_number(self):
        min_val = 0
        for file in self.point_map_files:
            match = re.search(r"_(.*)_", file)
            if int(match.group()[1:-1]) < min_val or min_val == 0:
                min_val = int(match.group()[1:-1])
        return min_val


class Table(tkinter.Frame):
    def __init__(self, parent):
        global point_map
        tkinter.Frame.__init__(self, parent)
        self._widgets = []
        for x in range(1, 11):
            current_row = []
            for y in range(1, 11):
                string_var = tkinter.StringVar()
                string_var.set(point_map[(x, y)])
                text = tkinter.Label(self, height=2, width=2, textvariable=string_var)
                text.grid(column=x, row=y)
                current_row.append(string_var)
            self._widgets.append(current_row)

    def set(self, row, column, value):
        widget = self._widgets[row - 1][column - 1]
        widget.set(value)


class MainFrame(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.data = PointMaps()
        self.file_data = None
        self.lowest_game = self.data.lowest_game_number()

        self.player_number = 0
        self.player_1_turn = 1
        self.player_2_turn = 2
        self.game_number = 0

        if self.game_number < self.lowest_game:
            self.game_number = self.lowest_game

        self._widgets = []

        self.menu_item = tkinter.Menu(self)
        self.config(menu=self.menu_item)

        self.file_menu = tkinter.Menu(self.menu_item, tearoff=0)
        self.sub_file_item_01 = tkinter.Menu(self.file_menu)
        self.menu_item.add_cascade(label="Load map", menu=self.sub_file_item_01)

        self.sub_file_item_01.add_separator()

        self.sub_file_item_01.add_command(
            label="Load Player One", command=self.load_player_1
        )
        self.sub_file_item_01.add_command(
            label="Load Player Two", command=self.load_player_2
        )

        self.sub_file_item_01.add_separator()

        self.sub_file_item_01.add_command(
            label="Next map", command=self.cycle_point_map_up
        )

        self.level_var = tkinter.StringVar()
        self.player_var = tkinter.StringVar()

        self.level_label = tkinter.Label(self, textvariable=self.level_var)
        self.player_label = tkinter.Label(self, textvariable=self.player_var)

        self.level_label.pack(side="bottom")
        self.player_label.pack(side="bottom")

        self.button_up = tkinter.Button(
            text="Point Up", command=self.cycle_point_map_up
        )
        self.button_down = tkinter.Button(
            text="Point Down", command=self.cycle_point_map_down
        )

        self.button_up.pack()
        self.button_down.pack()

        self.game_var = tkinter.StringVar()

        self.game_number_up_button = tkinter.Button(
            text="Game Up", command=self.game_up
        )
        self.game_number_dn_button = tkinter.Button(
            text="Game Down", command=self.game_down
        )

        self.game_number_up_button.pack(side="left")
        self.game_number_dn_button.pack(side="left")

        self.point_map = Table(self)
        self.point_map.pack()

    def _set_point_map(self, turn):
        global point_map
        try:
            for data in self.file_data:
                try:
                    point_map = data["turn_%s" % turn]
                    raise StopIteration
                except KeyError:
                    continue
        except StopIteration:
            try:
                for x, y in point_map:
                    self.point_map.set(x, y, point_map[(x, y)])
            except KeyError:
                print("Fail")

    def _load_point_map(self, p_number):
        print(p_number, "P")
        try:
            for file_name in self.data.point_map_files:
                print(file_name, "First")
                p_match = re.search(r"._", file_name)
                print(p_match.string)
                if p_match.string[0] == str(self.player_number):
                    print(file_name, "Second")
                    match = re.search(r"_(.*)_", file_name)
                    if match.group()[1:-1] == str(self.game_number):
                        print(file_name, "Third")
                        self.file_data = self.data.load_point_map(match.string)
                        break
        except KeyError:
            self.level_var.set("No more turns to look at")

    def cycle_point_map_up(self):
        self.player_1_turn += 2
        self.player_2_turn += 2
        self._set_point_map(
            self.player_2_turn if self.player_number == 1 else self.player_1_turn
        )

    def cycle_point_map_down(self):
        self.player_1_turn -= 2
        self.player_2_turn -= 2
        self._set_point_map(
            self.player_2_turn if self.player_number == 1 else self.player_1_turn
        )

    def load_player_1(self):
        self.player_number = 1
        self.player_var.set("Player: %s" % self.player_number)
        self._load_point_map(self.game_number)

    def load_player_2(self):
        self.player_number = 2
        self.player_var.set("Player: %s" % self.player_number)
        self._load_point_map(self.game_number)

    def game_up(self):
        pass

    def game_down(self):
        pass


if __name__ == "__main__":
    root = MainFrame()
    root.mainloop()
