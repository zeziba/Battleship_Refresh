from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from dataclasses import dataclass, field
from enum import Enum, auto, StrEnum
from typing import Any, Generator
from Logger import get_logger
from Ship import Direction

logger = get_logger(__name__)

if TYPE_CHECKING:
    import Board
    import Fleet
    import Ship
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

    def generate_fleet(self) -> None:
        if self.difficulty is not Difficulty.PLAYER:
            self.fleet.generate()
        else:
            self.fleet.generate()

    @property
    def get_ships(self) -> Generator[Ship.Ship, Any, None]:
        for ship in self.fleet.fleet:
            yield self.fleet.fleet[ship]

    @property
    def destroyed(self) -> bool:
        if len(self.fleet.fleet) == 0:
            return True
        return all(self.fleet.fleet[ship].is_sunk for ship in self.fleet.fleet)

    def take_at_self_shot(self, x: int, y: int) -> tuple[bool, Board.Tile.Tile]:
        fleet, tile = self.fleet.hit(x, y), self.board.get(x, y)
        tile.hit = True
        return fleet, tile

    def auto_ship_placement(self, checker: Callable, board_size: int):
        import random

        for ship in self.get_ships:
            logger.debug(f"\tAttemtpting to place {ship.name}")
            while True:
                h_v = random.choice(["h", "v"])
                if "h" == h_v:
                    x = random.randint(0, board_size - 1 - ship.length)
                    y = random.randint(0, board_size - 1)
                else:
                    x = random.randint(0, board_size - 1)
                    y = random.randint(0, board_size - 1 - ship.length)
                    # if checker((x, y), h_v, self, ship):
                    ship.directionality = Direction.HORIZONTAL if h_v == "h" else Direction.VERTICAL
                    ship.place_ship(x, y, self.board)
                    logger.debug(f"\tSucceeded to place {ship.name} at ({x}, {y}, {h_v})")
                    break
                logger.debug(f"\tFailed to place {ship.name} at ({x}, {y}, {h_v})")
