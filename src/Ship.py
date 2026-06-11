from dataclasses import dataclass
from enum import Enum, auto, unique

from Logger import get_logger

logger = get_logger(__name__)

from Board import Board, GameRules
from Tile import Tile


@unique
class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


@dataclass()
class Ship:
    name: str = ""
    length: int = 0
    hit_points: int = length

    def contains(self, px: int, py: int) -> bool:
        logger.debug(f"Getting ({px}, {py}) of Ship<{self.name}>")
        return self.convert_xy_to_str_coords(px, py) in self.positions

    def hit(self, px: int, py: int) -> bool:
        logger.debug(f"Checking if ({px}, {py}) hits {self.name}")
        if self.contains(px, py) and not self.positions[self.convert_xy_to_str_coords(px, py)].hit:
            self.positions[self.convert_xy_to_str_coords(px, py)].hit = True
            self.hit_points -= 1
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
        if len(self.positions) == 0:
            for x, y in self.possible_places(start_x, start_y, self.length, self.directionality):
                if GameRules.check_xy(x, y):
                    self.positions[self.convert_xy_to_str_coords(x, y)] = board.tiles_set(x, y, Tile(self, False))
                else:
                    raise IndexError(f"({x},{y}) is not a valid move")
            return True
        return False

    @property
    def is_sunk(self) -> bool:
        logger.debug(f"Checking if {self.name} is sunk")
        return self.hit_points == 0

    @property
    def is_placed(self) -> bool:
        logger.debug(f"Checking if {self.name} is placed")
        return len(self.positions) == self.length

    @staticmethod
    def convert_xy_to_str_coords(px: int, py: int) -> str:
        logger.debug(f"Converting ({px}, {py}) to '{px}, {py}'")
        return f"{px},{py}"

    @staticmethod
    def get_xy_pos(pos: str) -> tuple[int, int]:
        logger.debug("Getting int tuple for coord from str coord")
        x, y = pos.split(",")
        return int(x), int(y)

    @property
    def directionality(self):
        logger.debug(f"Getting {self.name}'s directionality")
        return self.__directionality

    @directionality.setter
    def directionality(self, value: Direction):
        logger.debug(f"Setting {self.name}'s directionality")
        self.__directionality = value

    def __post_init__(self):
        logger.debug("Post Init")
        self.__directionality: Direction = Direction.VERTICAL
        self.hit_points = self.length
        self.positions = dict()
