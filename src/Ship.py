from dataclasses import dataclass, field
from enum import Enum, auto, unique

import Board


@unique
class Direction(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


@dataclass()
class Ship:
    name: field(default_factory=str)
    length: field(default_factory=int)

    def contains(self, px: int, py: int) -> bool:
        return self.set_pos(px, py) in self.positions

    def hit(self, px: int, py: int) -> bool:
        if self.contains(px, py) and not self.positions[self.set_pos(px, py)].hit:
            self.positions[self.set_pos(px, py)].hit = True
            self.hit_points -= 1
            return True
        return False

    @staticmethod
    def possible_places(
        start_x: int, start_y: int, length: int, directionality: Direction
    ):
        h = 1 if directionality is Direction.HORIZONTAL else 0
        v = 0 if directionality is Direction.HORIZONTAL else 1
        for i in range(length):
            x = start_x + i * h
            y = start_y + i * v
            yield x, y

    def place_ship(self, start_x: int, start_y: int, board: Board.Board) -> bool:
        if len(self.positions) == 0:
            for x, y in self.possible_places(
                start_x, start_y, self.length, self.directionality
            ):
                if Board.GameRules.check_xy(x, y):
                    self.positions[self.set_pos(x, y)] = board.tiles_set(
                        x, y, Board.Tile.Tile(self, False)
                    )
                else:
                    raise IndexError(f"({x},{y}) is not a valid move")
            return True
        return False

    @property
    def is_sunk(self) -> bool:
        return self.hit_points == 0

    @property
    def is_placed(self) -> bool:
        return len(self.positions) == self.length

    @staticmethod
    def set_pos(px, py) -> str:
        return f"{px},{py}"

    @staticmethod
    def get_xy_pos(pos: str) -> tuple[int, int]:
        x, y = pos.split(",")
        return int(x), int(y)

    @property
    def directionality(self):
        return self.__directionality

    @directionality.setter
    def directionality(self, value: Direction):
        self.__directionality = value

    def __post_init__(self):
        self.__directionality: Direction.VERTICAL = field(default=Direction)
        self.hit_points = self.length
        self.positions = dict()
