from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from Logger import get_logger

import GameRules

if TYPE_CHECKING:
    import Tile

logger = get_logger(__name__)

EMPTYTILE = GameRules.EmptyTile
HITTILE = GameRules.HitTile


@dataclass()
class Board:
    height: int = GameRules.SIZE
    width: int = GameRules.SIZE
    _tiles: list[Tile.Tile] = field(init=False, default_factory=list)

    def __post_init__(self):
        logger.debug("Post Init of board")
        self._generate_board()
        logger.debug(f"\tGenerated board has {len(self._tiles)} Tile.Tile(s)")

    @property
    def size(self):
        logger.debug("Getting size property")
        return self.height * self.width

    @property
    def tiles(self) -> tuple[Tile.Tile, ...]:
        logger.debug("Getting Board.tiles")
        return tuple(self._tiles)

    def _convert_to_1d_index(self, x: int, y: int):
        logger.debug("Converting 2d coords to 1d index")
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            raise IndexError(f"Coordinates ({x}, {y}) track outside of board")
        return x + (y * self.width)

    def get(self, px, py) -> Tile.Tile:
        logger.debug(f"Getting Board.get({px}, {py}) Tile")
        index = self._convert_to_1d_index(px, py)
        return self.tiles[index]

    def tiles_set(self, x: int, y: int, tile: Tile.Tile) -> Tile.Tile:
        logger.debug(f"Setting Tile at ({x}, {y})")
        index = self._convert_to_1d_index(x, y)
        self._tiles[index] = tile
        return tile

    def _generate_board(self) -> None:
        logger.debug("Generating Board Tile(s)")
        import Tile

        self._tiles = [Tile.Tile(None, False) for _ in range(self.size)]

    @property
    def all_ships_sunk(self):
        logger.debug("Checking if all ships are sunk")
        occupied = [tile for tile in self._tiles if tile.has is not None]
        if not occupied:
            return False

        return all(tile.has.is_sunk if tile.has else False for tile in occupied)

    def output_array(self) -> tuple[int, ...]:
        logger.debug("Generating output array")
        score = lambda hit, contains: 1 if (not hit and contains) else 0
        return tuple(score(tile.hit, tile.contains) for tile in self.tiles)

    def output_readable(self, hidden: bool = True) -> str:
        logger.debug("Geneerating output that is readable")
        nl = "\n"
        if hidden:
            return "".join(
                [
                    f"{HITTILE if tile.hit else EMPTYTILE}{nl if (index + 1) % self.size == 0 else ''}"
                    for index, tile in enumerate(self.tiles)
                ]
            )
        else:
            return "".join(
                [
                    f"{HITTILE if tile.contains else EMPTYTILE}{nl if (index + 1) % self.size == 0 else ''}"
                    for index, tile in enumerate(self.tiles)
                ]
            )
