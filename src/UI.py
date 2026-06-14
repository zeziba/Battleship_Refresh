from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
import os
import time
import re

from .Logger import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from . import Tile
    from . import Board
    from .Game import TurnResult

from . import check_xy
from .GameRules import Output

DELAY: float = 0.5


def get_valid_coordinates(prompt_message: str) -> tuple[int, int]:
    logger.debug("Attempting to get valid coords")
    while True:
        raw_input = input(f"{prompt_message}")
        parsed_xy = parse_coord(raw_input)

        if parsed_xy is None:
            output(Output.INVALID_COORD)
            continue

        x, y = parsed_xy

        if not check_xy(x, y):
            output(Output.INVALID_COORD)
            continue
        return x, y


def parse_coord(raw_input: str) -> Optional[tuple[int, int]]:
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

            return x, y

    return None


def get_selection(selection: str) -> str:
    logger.debug("Getting input from user")
    return input(f"{selection}")


def output(selection: str) -> None:
    print(f"{selection}")


def clear_screen():
    logger.debug("Clearing Screen")
    os.system("cls" if os.name == "nt" else "clear")


def pause(self, seconds: Optional[float] = None):
    logger.debug("Initating Pause")
    time.sleep(seconds if seconds is not None else self.delay)


def prompt_to_continue():
    logger.debug("Waiting for key press to continue")
    input("\nPress [Enter] to continue...")


def _generate_board_output(board: Board.Board, hide_ships: bool = False):
    header_row = "   " + " ".join([str(i) for i in range(board.width)])
    body = ""

    for y in range(board.height):
        row_str = f"{y} |"

        for x in range(board.width):
            tile: Tile.Tile = board.get(x, y)
            row_str += tile.get_rendered_logo(hide_ships)
        body += f"\n{row_str}"

    return f"{header_row}{body}"


def print_board(board: Board.Board, hide_ships=False):
    logger.debug("Starting Board print")
    print(_generate_board_output(board, hide_ships))


def print_turn_result(results: TurnResult):
    logger.debug("Starting print_turn_results")
    clear_screen()
    output(Output.CURRENT_TURN.format(results.turnNumber, results.defender.name))
    output(Output.SHOT_AT.format(results.shot_x, results.shot_y, "hit" if results.hit else "miss"))
    if results.sunk_ship:
        output(Output.SUNK_SHIP.format(results.sunk_ship))


def strip_ansi(text: str):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def print_boards(
    p1_name: str, player1: Board.Board, p2_name: str, player2: Board.Board, _pass: bool = False, hidden: bool = True
):
    logger.debug("Starting print_boards")

    p1_out = f"{Output.BOARD_PRINTPUT_HEADER_1.format(p1_name)}"
    p2_out = f"{Output.BOARD_PRINTPUT_HEADER_2.format(p2_name)}"

    p1_body = _generate_board_output(player1, hidden).split("\n")
    p2_body = _generate_board_output(player2, hidden).split("\n")

    max_board_width = max((len(strip_ansi(line)) for line in p1_body), default=0)
    col_width = max(len(strip_ansi(p1_out)), max_board_width) + 5

    def pad_line(line: str, width: int):
        visible_len = len(strip_ansi(line))
        padding_needed = max(0, width - visible_len)
        return line + (" " * padding_needed)

    out = f"{p1_out:<{col_width}}     {p2_out}\n"

    for i in range(len(p1_body)):
        left_line = pad_line(p1_body[i], col_width)
        out += f"{left_line}{p2_body[i]}\n"

    output(out)

    if _pass:
        prompt_to_continue()


def print_game_over(p1_name: str, defender: Board.Board, clear: bool = False):
    logger.debug("Starting Game Over print")
    if clear:
        clear_screen()
    output(Output.WON_GAME.format(p1_name))
    print_board(defender)
