from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import Tile

import os
import time

from GameRules import Colors, SIZE, HitTile, MissTile, EmptyTile


@dataclass()
class UI:
    delay = 0.5 
    
    def get_coords(self, output: str) -> tuple[int, int]:
        x, y = input(f"{output}").split(" ")
        return int(x), int(y)

    def get_selection(self, selection: str) -> str:
        return input(f"{selection}")

    def output(self, selection: str) -> None:
        print(f"{selection}")

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

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
