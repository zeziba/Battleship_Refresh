from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from Logger import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    import Tile
    import Board

import os
import time

from GameRules import Output, check_xy


@dataclass()
class UI:
    delay: float = 0.5

    def get_valid_coordinates(self, prompt_message: str) -> tuple[int, int]:
        logger.debug("Attempting to get valid coords")
        while True:
            raw_input = input(f"{prompt_message}")
            parsed_xy = self.parse_coord(raw_input)

            if parsed_xy is None:
                self.output(Output.INVALID_COORD)
                continue

            x, y = parsed_xy

            if not check_xy(x, y):
                self.output(Output.INVALID_COORD)
                continue
            return x, y

    def parse_coord(self, raw_input: str) -> Optional[tuple[int, int]]:
        logger.debug(f"Parsing coords = {r'{}'.format(bytes(raw_input, 'utf-8'))}")
        clean_input = raw_input.strip().lower()
        if not clean_input:
            return None

        for seperator in [",", ";", " ", ":"]:
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
                x = ord(letter_part) - ord("a")
                y = int(digit_part) - 1

                return x, y - 1

        return None

    def get_selection(self, selection: str) -> str:
        logger.debug("Getting input from user")
        return input(f"{selection}")

    def output(self, selection: str) -> None:
        print(f"{selection}")

    @staticmethod
    def clear_screen():
        logger.debug("Clearing Screen")
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self, seconds: Optional[float] = None):
        logger.debug("Initating Pause")
        time.sleep(seconds if seconds is not None else self.delay)

    @staticmethod
    def prompt_to_continue():
        logger.debug("Waiting for key press to continue")
        input("\nPress [Enter] to continue...")

    @staticmethod
    def print_board(board: Board.Board, hide_ships=False):
        logger.debug("Starting Board print")
        header_row = "   " + " ".join([str(i) for i in range(board.width)])
        print(header_row)

        for y in range(board.height):
            row_str = f"{y} |"

            for x in range(board.width):
                tile: Tile.Tile = board.get(x, y)
                row_str += tile.get_rendered_logo(hide_ships)
            print(row_str)


if __name__ == "__main__":
    # Test parse of raw coords
    ui = UI(0.5)
    ui.parse_coord("A5")
    ui.parse_coord("spam\\neggs")
