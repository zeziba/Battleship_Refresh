from dataclasses import dataclass, field

import GameRules
import Tile

EMPTYTILE = GameRules.EmptyTile
HITTILE = GameRules.HitTile


@dataclass()
class Board:
    _tiles: list[Tile.Tile] = field(init=False, default_factory=list[Tile.Tile])
    height: int = GameRules.SIZE
    width: int = GameRules.SIZE
    size: int = height * width

    @property
    def tiles(self) -> tuple[Tile.Tile, ...]:
        return tuple(self._tiles)

    def get(self, px, py) -> Tile.Tile:
        return self.tiles[px + py * self.size]

    def tiles_set(self, x: int, y: int, tile: Tile.Tile) -> Tile.Tile:
        size = self.size - 1
        if (size >= x >= 0) and (size >= y >= 0):
            self._tiles[x + y * self.size] = tile
            return self._tiles[x + y * self.size]
        raise IndexError(
            f"{tile.contains}: Cannot be placed at ({x},{y}) as it is out of bounds"
        )

    def generate_board(self) -> None:
        self._tiles = [Tile.Tile(None, False) for _ in range(self.size**2)]

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

    def output_array(self) -> tuple[int, ...]:
        score = lambda hit, contains: (
            1
            if hit is True and contains is not None
            else 1 if hit is True and contains is None else 0
        )
        return tuple(score(tile.hit, tile.contains) for tile in self.tiles)
