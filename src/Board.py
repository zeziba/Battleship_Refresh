from __future__ import annotations
from dataclasses import dataclass, field

from .Logger import get_logger

from . import config
from . import GameRules
from . import Tile

logger = get_logger(__name__)

EMPTYTILE = GameRules.EmptyTile
HITTILE = GameRules.HitTile


@dataclass()
class Board:
    height: int = field(default=config.board_height)
    width: int = field(default=config.board_width)
    _tiles: list[Tile.Tile] = field(init=False, default_factory=list)

    def __post_init__(self):
        logger.debug("Post Init of board")
        self._generate_board()
        logger.debug(f"\tGenerated board has {len(self._tiles)} Tile.Tile(s)")

    @property
    def size(self):
        logger.debug("Getting size property")
        if self.height and self.width:
            return self.height * self.width
        return 0

    @property
    def tiles(self) -> tuple[Tile.Tile, ...]:
        logger.debug("Getting Board.tiles")
        return tuple(self._tiles)

    def _convert_to_1d_index(self, x: int, y: int):
        logger.debug("Converting 2d coords to 1d index")
        if self.width is not None and self.height is not None:
            if not (0 <= x < self.width) or not (0 <= y < self.height):
                raise IndexError(f"Coordinates ({x}, {y}) track outside of board")
            return x + (y * self.width)
        raise ValueError("Width or Height not set")

    def get(self, px, py) -> Tile.Tile:
        logger.debug(f"Getting Board.get({px}, {py}) Tile")
        index = self._convert_to_1d_index(px, py)
        return self._tiles[index]

    def tiles_set(self, x: int, y: int, tile: Tile.Tile) -> Tile.Tile:
        logger.debug(f"Setting Tile at ({x}, {y})")
        index = self._convert_to_1d_index(x, y)
        self._tiles[index] = tile
        return tile

    def _generate_board(self) -> None:
        logger.debug("Generating Board Tile(s)")
        self._tiles = [Tile.Tile(None, False) for _ in range(self.width * self.height)]

    @property
    def all_ships_sunk(self):
        logger.debug("Checking if all ships are sunk")
        occupied = [tile for tile in self._tiles if tile.has is not None]
        if not occupied:
            return False

        return all(tile.has.is_sunk if tile.has else False for tile in occupied)
