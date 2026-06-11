from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from dataclasses import dataclass, field
from enum import Enum, auto, StrEnum
from typing import Any, Generator
from Logger import get_logger
from Ship import Direction
from GameRules import Output

logger = get_logger(__name__)

if TYPE_CHECKING:
    import Board
    import Fleet
    import Ship
    import Tile
    import UI
    from AI import BattleShipAI


class Difficulty(StrEnum):
    PLAYER = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


@dataclass()
class Player:
    _name: str
    _difficulty: Difficulty
    _board: Board.Board
    _fleet: Fleet.GeneralFleet
    _ai_brain: BattleShipAI | None = None

    @property
    def name(self):
        return self._name

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @property
    def fleet(self) -> Fleet.GeneralFleet:
        return self._fleet

    @property
    def board(self) -> Board.Board:
        return self._board
    
    @property
    def is_ai(self) -> bool:
        return self.difficulty != Difficulty.PLAYER

    @property
    def get_ships(self) -> Generator[Ship.Ship, Any, None]:
        for ship in self.fleet.ships:
            yield ship

    def take_at_self_shot(self, x: int, y: int) -> tuple[bool, Board.Tile.Tile]:
        fleet, tile = self.fleet.hit(x, y), self.board.get(x, y)
        tile.hit = True
        return fleet, tile
    
    def choose_target(self, UI: UI.UI) -> tuple[int, int]:
        if self._ai_brain and self.is_ai:
            x, y = self._ai_brain.get_shot()
            UI.output(Output.AI_SHOT_TAKEN.format(x, y))
        else:
            while True:
                raw_coords = UI.get_selection(Output.COORD_ENTER_GENERIC)
                parsed_coord = UI.parse_coord(raw_coords)
                if parsed_coord is None:
                    logger.debug(f"Failed to enter proper coords with {parsed_coord}")
                    UI.output(Output.WRONG_INPUT.format(Output.EXAMPLE_1))
                    continue
                else:
                    x, y = parsed_coord
        return x, y
    
    def is_alread_targeted(self, x, y) -> bool:
        return self.board.get(x, y).hit

    def process_shot(self, x: int, y: int, tile: Tile.Tile):
        if self._ai_brain and self.difficulty and self.is_ai and tile.has:
            if tile.has.is_sunk:
                self._ai_brain.ships_left.pop(tile.has.name, None)
            self._ai_brain.register_hit(x, y, tile.has.is_sunk)

    def auto_ship_placement(self, board_size: int):
        import random

        for ship in self.fleet.ships:
            logger.debug(f"\tAttemtpting to place {ship.name}")
            while True:
                h_v = random.choice(["h", "v"])
                if "h" == h_v:
                    x = random.randint(0, board_size - 1 - ship.length)
                    y = random.randint(0, board_size - 1)
                else:
                    x = random.randint(0, board_size - 1)
                    y = random.randint(0, board_size - 1 - ship.length)
                    ship.directionality = Direction.HORIZONTAL if h_v == "h" else Direction.VERTICAL
                    ship.place_ship(x, y, self.board)
                    logger.debug(f"\tSucceeded to place {ship.name} at ({x}, {y}, {h_v})")
                    break
                logger.debug(f"\tFailed to place {ship.name} at ({x}, {y}, {h_v})")
