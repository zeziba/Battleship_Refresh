from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import GameRules

if TYPE_CHECKING:
    import Tile

EMPTYTILE = GameRules.EmptyTile
HITTILE = GameRules.HitTile


@dataclass()
class Board:
    height: int = GameRules.SIZE
    width: int = GameRules.SIZE
    _tiles: list[Tile.Tile] = field(init=False, default_factory=list)

    def __post_init__(self):
        self._generate_board()

    @property
    def size(self):
        return self.height * self.width

    @property
    def tiles(self) -> tuple[Tile.Tile, ...]:
        return tuple(self._tiles)
    
    def _convert_to_1d_index(self, x: int, y: int):
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            raise IndexError(f"Coordinates ({x}, {y}) track outside of board")
        return x + (y * self.width)

    def get(self, px, py) -> Tile.Tile:
        index = self._convert_to_1d_index(px, py)
        return self.tiles[index]

    def tiles_set(self, x: int, y: int, tile: Tile.Tile) -> Tile.Tile:
        index = self._convert_to_1d_index(x, y)
        self._tiles[index] = tile
        return tile

    def _generate_board(self) -> None:
        import Tile
        self._tiles = [Tile.Tile(None, False) for _ in range(self.size)]

    @property
    def all_ships_sunk(self):
        occupied = [tile for tile in self._tiles if tile.has is not None]
        if not occupied:
            return False
        
        return all(tile.has.is_sunk if tile.has else False for tile in occupied)
    
    def output_array(self) -> tuple[int, ...]:
        score = lambda hit, contains: 1 if (not hit and contains) else 0
        return tuple(score(tile.hit, tile.contains) for tile in self.tiles)

    def output_readable(self, hidden: bool = True) -> str:
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
