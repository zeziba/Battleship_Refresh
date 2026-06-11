from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from Logger import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    import Tile

import os
import time

from GameRules import Colors, SIZE, HitTile, MissTile, EmptyTile, Output, check_xy


@dataclass()
class UI:
    delay = 0.5

    def get_coords(self, output: str) -> tuple[int, int]:
        x, y = input(f"{output}").split(" ")
        return int(x), int(y)

    def parse_coord(self, raw_input: str) -> Optional[tuple[int, int]]:
        clean_input = raw_input.strip().lower()
        if not clean_input:
            return None
        
        for seperator in [',', ';', ' ', ':']:
            if seperator in clean_input:
                parts = [p.strip() for p in clean_input.split(seperator) if p.strip()]
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    return int(parts[0]), int(parts[1])
        
        letter_part = ""
        digit_part = ""

        for char in clean_input:
            if char.isalpha():
                letter_part += char
            elif char.isdigit():
                digit_part += char
        
        if letter_part and digit_part and (len(letter_part) + len(digit_part) == len(clean_input)):
            if len(letter_part) == 1:
                x = ord(letter_part) - ord('a')
                y = int(digit_part) - 1

                return x, y
        
        return None
    
    def take_shot(self):
        logger.info("Getting player input for taking a shot")
        while True:
            try:
                x, y = self.get_coords(Output.COORD_ENTER)
            except ValueError as error:
                logger.warning(error)
                self.output(Output.INVALID_COORD)
            else:
                if check_xy(x, y):
                    break
                else:
                    self.output(Output.INVALID_COORD)
        return x, y

    def get_selection(self, selection: str) -> str:
        return input(f"{selection}")

    def output(self, selection: str) -> None:
        print(f"{selection}")

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def pause(seconds: float = 1.5):
        time.sleep(seconds)

    @staticmethod
    def prompt_to_continue():
        input("\nPress [Enter] to continue...")

    @staticmethod
    def print_board(board, hide_ships=False):
        print("   " + " ".join([str(i) for i in range(SIZE)]))

        for y in range(SIZE):
            row_str = f"{y} |"

            for x in range(SIZE):
                tile: Tile.Tile = board.get(x, y)
                if tile.hit and tile.has:
                    if tile.has.is_sunk:
                        row_str += f"{Colors.LIGHT_RED}{tile.has.name[0]} {Colors.END}"
                    else:
                        row_str += HitTile
                elif tile.hit:
                    row_str += MissTile
                elif not hide_ships and tile.has:
                    row_str += f"{Colors.GREEN}{tile.has.name[0]} {Colors.END}"
                else:
                    row_str += EmptyTile
            print(row_str)
