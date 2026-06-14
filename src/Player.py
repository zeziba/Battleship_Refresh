from __future__ import annotations
from dataclasses import dataclass, field
from enum import auto, StrEnum
import random
from typing import TYPE_CHECKING, Callable, Optional, Any, Generator

from .Ship import Direction
from .Logger import get_logger
from .GameRules import Output, check_xy
from . import AI
from . import Board
from . import Fleet
from . import UI

if TYPE_CHECKING:
    from . import Ship
    from . import Tile
    from .AI import BattleShipAI


class Difficulty(StrEnum):
    HUMAN = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


logger = get_logger(__name__)


def create_player(name: str, difficulty: Difficulty, board: Board.Board, fleet_comp: dict[str, int]):
    ai_brain = None
    if difficulty == Difficulty.EASY:
        ai_brain = AI.Random(board.width, board.height)
    elif difficulty == Difficulty.MEDIUM:
        ai_brain = AI.HuntAndTargetAIAdv(board.width, board.height)
    # elif p.difficulty == Difficulty.HARD:
    #     p._ai_brain = AI.ProbabilityAI()

    return Player(
        name, difficulty, board, Fleet.GeneralFleet(fleet_comp=fleet_comp), ai_brain
    )


def has_overlap(board: Board.Board, positions: list[tuple[int, int]]) -> bool:
    for px, py in positions:
        if board.get(px, py).contains:
            return True
    return False


def is_valid_placement(board: Board.Board, x: int, y: int, size: int, orinentation: Direction) -> bool:
    logger.debug(f"Begining check for ship of length {size} at ({x}, {y}, {orinentation})")
    if orinentation == Direction.HORIZONTAL:
        if x < 0 or (x + size) > board.width or y < 0 or (y + size) > board.height:
            return False
        coordinates = [(x + i, y) for i in range(size)]
    else:
        coordinates = [(x, y + i) for i in range(size)]

    for cx, cy in coordinates:
        tile = board.get(cx, cy)
        if tile.has:
            return False

    return True


def _validate_human_ship_input(
    coords: tuple[int, int], h_v: str, p: Player, ship: Ship.Ship, display: Callable[[str], None]
) -> bool:
    x, y = coords
    h_v = h_v.strip().lower()
    logger.debug(f"Checking {p.name} at ({x}, {y}) with {h_v}")
    if h_v not in ("h", "v") or len(h_v) != 1:
        display(Output.DIR_INVALID)
        return False
    directionality = Ship.Direction.HORIZONTAL if h_v == "h" else Ship.Direction.VERTICAL
    if not check_xy(x, y):
        return False

    try:
        projected_coords = list(Ship.Ship.possible_places(x, y, ship.length, directionality))
    except Exception as ex:
        display(Output.FAILED_PLACE.format(ship.name, x, y, directionality))
        logger.warning(ex)
        return False

    for px, py in projected_coords:
        for existing_ship in p.get_ships:
            if existing_ship.is_placed and existing_ship.contains(px, py):
                display(Output.OVERLAP.format(x, y, existing_ship.name))
                return False

    return True


validate_human_ship_input = None


def set_validate_human_ship_input(display: Callable[[str], None]):
    def wrapper(coords: tuple[int, int], h_v: str, p: Player, ship: Ship.Ship):
        _validate_human_ship_input(coords, h_v, p, ship, display)

    global validate_human_ship_input
    validate_human_ship_input = wrapper


def get_user_coord_input(prompt: str) -> tuple[int, int] | None:
    raw_coords = UI.get_selection(prompt)
    parsed_coord = UI.parse_coord(raw_coords)
    if parsed_coord is None:
        logger.debug(f"Failed to enter proper coords with {parsed_coord}")
        UI.output(Output.WRONG_INPUT.format(Output.EXAMPLE_1))
    return parsed_coord


@dataclass()
class Player:
    _name: str
    _difficulty: Difficulty
    _board: Board.Board
    _fleet: Optional[Fleet.GeneralFleet] = field(default=None)
    _ai_brain: Optional[BattleShipAI] = field(default=None)

    _get_input_hook: Optional[Callable[[str], Optional[tuple[int, int]]]] = field(default=None)

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
        if self._fleet is None:
            raise ValueError(f"{self.name}'s Fleet not generated")
        return self._fleet

    @property
    def board(self) -> Board.Board:
        logger.debug(f"Gettings {self.name}'s board")
        return self._board

    @property
    def is_ai(self) -> bool:
        logger.debug(f"Getting if {self.name} is an ai")
        return self.difficulty != Difficulty.HUMAN

    @property
    def get_ships(self) -> Generator[Ship.Ship, Any, None]:
        logger.debug(f"Getting Generator for {self.name}'s fleet")
        if self._fleet is None:
            raise ValueError(f"{self.name}'s Fleet not generated")
        yield from self._fleet.ships

    def set_input_hook(self, func: Callable[[str], Optional[tuple[int, int]]]):
        self._get_input_hook = func

    def take_at_self_shot(self, x: int, y: int) -> Board.Tile.Tile:
        logger.debug(f"{self.name} is taking a shot at self")
        tile = self._board.get(x, y)
        tile.hit = True

        if self._fleet is None:
            raise ValueError(f"{self.name}'s Fleet not generated")

        self._fleet.hit(x, y)
        return tile

    def is_already_targeted(self, x: int, y: int) -> bool:
        logger.debug(f"Checking if ({x},{y}) in {self.name}'s board has been targeted")
        return self.board.get(x, y).hit

    def process_shot_result(self, x: int, y: int, tile: Tile.Tile):
        if self._ai_brain is not None and self.is_ai:
            logger.debug(f"Processing shot at ({x}, {y}) on {self.name}'s tile")
            is_hit = False
            _ship = None
            if tile.has:
                is_hit = tile.has.contains(x, y)
                if tile.has.is_sunk:
                    _ship = tile.has
            self._ai_brain.register_result((x, y), is_hit, _ship)

    def choose_target(self) -> tuple[int, int]:
        logger.debug(f"Starting target acquisition for {self.name}")
        if self.is_ai and self._ai_brain:
            ai_target = self._ai_brain.get_shot()
            if ai_target:
                return ai_target

            return random.randint(0, self._board.width - 1), random.randint(0, self._board.height - 1)

        if not self._get_input_hook:
            raise RuntimeError(f"Polymorphism Error: Human Player '{self.name}' UI input hook")

        while True:
            prompt = Output.COORD_ENTER_GENERIC
            coords = self._get_input_hook(prompt)
            if coords is not None:
                return coords

    def generate_fleet(self, fleet_manifest: dict[str, int]):
        if self.difficulty == Difficulty.HUMAN:
            self._place_human_fleet(fleet_manifest)
        else:
            self._place_ai_fleet(fleet_manifest)

    def _place_human_fleet(self, fleet_manifest: dict[str, int]):
        if validate_human_ship_input is None:
            raise ValueError("Did not initialize validate_human_ship_input with a display function")
        self._fleet = Fleet.GeneralFleet(fleet_comp=fleet_manifest)
        logger.debug(f"Starting auto ship placement for (Human) {self.name}")

        if self._fleet is None:
            raise ValueError(f"{self.name}'s Fleet not generated")

        for ship in self.fleet.ships:
            logger.debug(f"\tAttempting to place Ship: {ship.name}")
            placed = False
            while not placed:
                UI.output(Output.PLACE.format(ship.name))
                raw_coords = UI.get_selection(Output.COORD_ENTER_GENERIC)
                parsed_coord = UI.parse_coord(raw_coords)
                if parsed_coord is None:
                    UI.output(Output.MANGLED_PLACE.format(ship.name))
                    UI.output(Output.WRONG_INPUT.format(Output.EXAMPLE_1))
                    continue
                x, y = parsed_coord
                if not check_xy(x, y):
                    UI.output(Output.OUTSIDE_BOARD.format(x, y))
                    continue
                h_v = UI.get_selection(Output.DIR_ENTER)
                orientation = Direction.HORIZONTAL if h_v.strip().lower() == "h" else Direction.VERTICAL
                if not is_valid_placement(self.board, x, y, ship.length, orientation):
                    continue
                projected_position = list(ship.possible_places(x, y, ship.length, orientation))
                if has_overlap(self._board, projected_position):
                    _ship = self._board.get(x, y).has
                    if _ship:
                        UI.output(Output.OVERLAP.format(x, y, _ship.name))
                    continue

                ship.directionality = orientation
                ship.place_ship(x, y, self._board)
                placed = True
                logger.debug(f"\tSuccessfully placed {ship.name} at ({x}, {y})")

    def _place_ai_fleet(self, fleet_manifest: dict[str, int]):
        self._fleet = Fleet.GeneralFleet(fleet_comp=fleet_manifest)
        logger.debug(f"Starting auto ship placement for (AI) {self.name}")
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

                if has_overlap(self._board, projected_position):
                    continue

                ship.directionality = orientation
                ship.place_ship(x, y, self._board)
                placed = True
                logger.debug(f"\tSuccessfully placed {ship.name} at ({x}, {y})")

    def take_turn(self, opp: Player) -> tuple[int, int, bool, str]:
        x, y = self.choose_target()
        tile: Tile.Tile = opp.take_at_self_shot(x, y)
        
        self.process_shot_result(x, y, tile)

        if tile.has and tile.hit:
            return x, y, tile.hit, tile.has.name
        elif tile.hit:
            return x, y, tile.hit, ""
        return x, y, False, ""
