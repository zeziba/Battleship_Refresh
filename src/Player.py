from __future__ import annotations
from dataclasses import dataclass, field
from enum import auto, StrEnum
import random
from typing import TYPE_CHECKING, Iterator, Optional, Any, Generator

from Ship import Direction
from Logger import get_logger
from GameRules import Output, Colors

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


logger = get_logger(__name__)


@dataclass()
class Player:
    _name: str
    _difficulty: Difficulty
    _board: Board.Board
    _fleet: Fleet.GeneralFleet
    _ai_brain: Optional[BattleShipAI] = field(default=None)

    @property
    def name(self):
        logger.debug("Getting name")
        return self._name

    @property
    def difficulty(self) -> Difficulty:
        logger.debug(f"Getting {self.name}'s difficulty")
        return self._difficulty

    @property
    def fleet(self) -> Fleet.GeneralFleet:
        logger.debug(f"Gettings {self.name}'s fleet")
        return self._fleet

    @property
    def board(self) -> Board.Board:
        logger.debug(f"Gettings {self.name}'s board")
        return self._board

    @property
    def is_ai(self) -> bool:
        logger.debug(f"Getting if {self.name} is an ai")
        return self.difficulty != Difficulty.PLAYER

    @property
    def get_ships(self) -> Generator[Ship.Ship, Any, None]:
        logger.debug(f"Getting Generator for {self.name}'s fleet")
        yield from self._fleet.ships

    def take_at_self_shot(self, x: int, y: int) -> Board.Tile.Tile:
        logger.debug(f"{self.name} is taking a shot at self")
        tile = self._board.get(x, y)
        tile.hit = True

        self._fleet.hit(x, y)
        return tile

    def is_already_targeted(self, x, y) -> bool:
        logger.debug(f"Checking if ({x},{y}) in {self.name}'s board has been targeted")
        return self.board.get(x, y).hit

    def process_shot_result(self, x: int, y: int, tile: Tile.Tile):
        if self._ai_brain and self.is_ai and tile.has:
            logger.debug(f"Processing shot at ({x}, {y}) on {self.name}'s tile")
            if tile.has.is_sunk:
                self._ai_brain.ships_left.pop(tile.has.name, None)
            self._ai_brain.register_hit(x, y, tile.has.is_sunk)

    def choose_target(self, UI: UI.UI) -> tuple[int, int]:
        logger.debug(f"Starting target acquisition for {self.name}")
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

    def auto_ship_placement(self):
        logger.debug(f"Starting auto ship placement for {self.name}")
        for ship in self._fleet.ships:
            logger.debug(f"\tAttemtpting to place {ship.name}")
            placed = False

            while not placed:
                orientation = random.choice([Direction.HORIZONTAL, Direction.VERTICAL])

                if orientation == Direction.HORIZONTAL:
                    x = random.randint(0, self._board.width - ship.length)
                    y = random.randint(0, self._board.height - 1)
                else:
                    x = random.randint(0, self._board.width - 1)
                    y = random.randint(0, self._board.height - ship.length)

                projected_position = list(ship.possible_places(x, y, ship.length, orientation))

                overlap_detection = False
                for px, py in projected_position:
                    target_tile = self._board.get(px, py)
                    if target_tile.contains:
                        overlap_detection = True
                        break
                
                if overlap_detection:
                    continue

                ship.directionality = orientation
                ship.place_ship(x, y, self._board)
                placed = True
                logger.debug(f"\tSuccessfully placed {ship.name} at ({x}, {y})")
