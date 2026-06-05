from dataclasses import dataclass, field

import GameRules
import Tile

SIZE: int = GameRules.SIZE
EMPTYTILE = GameRules.EmptyTile
HITTILE = GameRules.HitTile


@dataclass()
class Board:
    __tiles: list[Tile.Tile] = field(init=False, default_factory=list[Tile.Tile])

    @property
    def tiles(self) -> tuple[Tile.Tile]:
        return tuple(self.__tiles)

    def get(self, px, py) -> Tile.Tile:
        return self.tiles[px + py * SIZE]

    def tiles_set(self, x: int, y: int, tile: Tile) -> Tile.Tile:
        size = SIZE - 1
        if (size >= x >= 0) and (size >= y >= 0):
            self.__tiles[x + y * SIZE] = tile
            return self.__tiles[x + y * SIZE]
        raise IndexError(
            f"{tile.contains}: Cannot be placed at ({x},{y}) as it is out of bounds"
        )

    def generate_board(self) -> None:
        self.__tiles = [Tile.Tile(None, False) for _ in range(SIZE * SIZE)]

    def output_readable(self, hidden: bool = True) -> str:
        nl = "\n"
        if hidden:
            return "".join(
                [
                    f"{HITTILE if tile.hit else EMPTYTILE}{nl if (index + 1) % SIZE == 0 else ''}"
                    for index, tile in enumerate(self.tiles)
                ]
            )
        else:
            return "".join(
                [
                    f"{HITTILE if tile.contains else EMPTYTILE}{nl if (index + 1) % SIZE == 0 else ''}"
                    for index, tile in enumerate(self.tiles)
                ]
            )

    def output_array(self) -> tuple[int]:
        score = (
            lambda hit, contains: 1
            if hit is True and contains is not None
            else 1
            if hit is True and contains is None
            else 0
        )
        return tuple(score(tile.hit, tile.contains) for tile in self.tiles)
