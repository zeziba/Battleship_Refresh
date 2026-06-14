from dataclasses import dataclass
from enum import Enum, auto, unique

from .Logger import get_logger

logger = get_logger(__name__)

from . import check_xy
from .Board import Board, GameRules
from .Tile import Tile


@unique
class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


@dataclass()
class Ship:
    name: str = ""
    length: int = 0

    def __post_init__(self):
        logger.debug("Post Init")
        self._directionality: Direction = Direction.VERTICAL
        self._positions: dict[tuple[int, int], Tile] = dict()

    def contains(self, px: int, py: int) -> bool:
        logger.debug(f"Getting ({px}, {py}) of Ship<{self.name}>")
        return (px, py) in self._positions

    def hit(self, px: int, py: int) -> bool:
        logger.debug(f"Checking if ({px}, {py}) hits {self.name}")
        if self.contains(px, py) and not self._positions[(px, py)].hit:
            self._positions[(px, py)].hit = True
            self._hit_points -= 1
            return True
        return False

    @staticmethod
    def possible_places(start_x: int, start_y: int, length: int, directionality: Direction):
        logger.debug(f"Getting possible places for Length: {length} with {directionality}")
        h = 1 if directionality is Direction.HORIZONTAL else 0
        v = 0 if directionality is Direction.HORIZONTAL else 1
        for i in range(length):
            x = start_x + i * h
            y = start_y + i * v
            yield x, y

    def place_ship(self, start_x: int, start_y: int, board: Board) -> bool:
        logger.debug(f"Attempting to place ship {self.name}")
        if len(self._positions) == 0:
            for x, y in self.possible_places(start_x, start_y, self.length, self.directionality):
                if check_xy(x, y):
                    self._positions[(x, y)] = board.tiles_set(x, y, Tile(self, False))
                else:
                    raise IndexError(f"({x},{y}) is not a valid move")
            return True
        return False

    @property
    def is_sunk(self) -> bool:
        logger.debug(f"Checking if {self.name} is sunk")
        return all(tile.hit for tile in self._positions.values())

    @property
    def is_placed(self) -> bool:
        logger.debug(f"Checking if {self.name} is placed")
        return len(self._positions) == self.length

    @property
    def directionality(self):
        logger.debug(f"Getting {self.name}'s directionality")
        return self._directionality

    @directionality.setter
    def directionality(self, value: Direction):
        logger.debug(f"Setting {self.name}'s directionality")
        self._directionality = value
