from __future__ import annotations
import os
import re
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from .Logger import get_logger
from . import check_xy
from .GameRules import Output

logger = get_logger(__name__)

if TYPE_CHECKING:
    from . import Board
    from .Game import TurnResult


@dataclass
class ScreenBuffer:
    frames: list[str] = field(default_factory=list)

    def capture_frame(self, frame: str):
        self.frames.append(frame)
        logger.debug(f"Frame {len(self.frames) - 1} captured in screen buffer")

    def get_frame(self, frame_index: int) -> Optional[str]:
        if 0 <= frame_index < len(self.frames):
            return self.frames[frame_index]
        return None

    def clear_buffer(self):
        self.frames.clear()

    @property
    def last_frame(self) -> str:
        if not self.frames:
            return ""
        return self.frames[-1]


class GameUI:
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.buffer = ScreenBuffer()
        self._ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    @staticmethod
    def strip_ansi(text: str):
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", text)

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

    def output(self, selection: str, capture: bool = False) -> None:
        print(f"{selection}")
        if capture:
            self.buffer.capture_frame(selection)

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

    @staticmethod
    def parse_coord(raw_input: str) -> Optional[tuple[int, int]]:
        logger.debug(f"Parsing coords = {r'{}'.format(bytes(raw_input, 'utf-8'))}")
        clean_input = raw_input.strip().lower()
        if not clean_input:
            return None

        for seperator in [",", ";", " ", ":"]:
            if seperator in clean_input:
                parts = [p.strip() for p in clean_input.split(seperator) if p.strip()]
                if len(parts) == 2 and all(p.isdigit() for p in parts):
                    return int(parts[0]), int(parts[1])

        letter_part = "".join(c for c in clean_input if c.isalpha())
        digit_part = "".join(c for c in clean_input if c.isdigit())

        if letter_part and digit_part and (len(letter_part) + len(digit_part) == len(clean_input)):
            if len(letter_part) == 1:
                x = ord(letter_part) - ord("a")
                y = int(digit_part) - 1

                return x, y

        return None

    @staticmethod
    def get_selection(selection: str) -> str:
        logger.debug("Getting input from user")
        return input(f"{selection}")

    @staticmethod
    def _generate_board_output(board: Board.Board, hide_ships: bool = False):
        header_row = "   " + " ".join([str(i) for i in range(board.width)])
        rows = []

        for y in range(board.height):
            tiles_str = "".join(board.get(x, y).get_rendered_logo(hide_ships) for x in range(board.width))
            rows.append(f"{y} |{tiles_str}")

        return f"{header_row}\n" + "\n".join(rows)

    def print_board(self, board: Board.Board, hide_ships=False):
        logger.debug("Starting Board print")
        self.output(self._generate_board_output(board, hide_ships), True)

    def print_turn_result(self, results: TurnResult):
        logger.debug("Starting print_turn_results")
        self.clear_screen()

        frmae_content = [
            Output.CURRENT_TURN.format(results.turnNumber, results.defender.name),
            Output.SHOT_AT.format(results.shot_x, results.shot_y, "hit" if results.hit else "miss"),
        ]

        if results.sunk_ship:
            frmae_content.append(Output.SUNK_SHIP.format(results.sunk_ship))

        self.output("\n".join(frmae_content), capture=True)

    def print_boards(
        self,
        p1_name: str,
        player1: Board.Board,
        p2_name: str,
        player2: Board.Board,
        _pass: bool = False,
        hidden: bool = True,
    ):
        logger.debug("Starting print_boards")

        p1_out = f"{Output.BOARD_PRINTPUT_HEADER_1.format(p1_name)}"
        p2_out = f"{Output.BOARD_PRINTPUT_HEADER_2.format(p2_name)}"

        p1_body = self._generate_board_output(player1, hidden).split("\n")
        p2_body = self._generate_board_output(player2, hidden).split("\n")

        max_board_width = max((len(self.strip_ansi(line)) for line in p1_body), default=0)
        col_width = max(len(self.strip_ansi(p1_out)), max_board_width) + 5

        def pad_line(line: str, width: int):
            visible_len = len(self.strip_ansi(line))
            padding_needed = max(0, width - visible_len)
            return line + (" " * padding_needed)

        out = f"{p1_out:<{col_width}}     {p2_out}\n"

        for i in range(len(p1_body)):
            left_line = pad_line(p1_body[i], col_width)
            out += f"{left_line}{p2_body[i]}\n"

        self.output(out)

        if _pass:
            self.prompt_to_continue()

    def print_game_over(self, p1_name: str, defender: Board.Board, clear: bool = False):
        logger.debug("Starting Game Over print")
        if clear:
            self.clear_screen()
        self.output(Output.WON_GAME.format(p1_name))
        last_frame = self.buffer.last_frame
        if last_frame:
            self.output(last_frame)
        else:
            self.print_board(defender)
