from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from GameRules import Colors, HitTile, MissTile, EmptyTile

if TYPE_CHECKING:
    import GameRules
    from Ship import Ship


@dataclass
class Tile:
    _contains: Ship | None
    _hit: bool = False

    @property
    def hit(self) -> bool:
        return self._hit

    @hit.setter
    def hit(self, value: bool) -> None:
        self._hit = value

    @property
    def contains(self) -> bool:
        return self._contains is not None

    @contains.setter
    def contains(self, value) -> None:
        if self.contains:
            raise IndexError(f"Location already has {self.contains}")
        self._contains = value

    @property
    def has(self) -> Ship | None:
        return self._contains

    def get_rendered_logo(self, hidden: bool = True) -> str:
        if self._hit and self._contains:
            if self._contains.is_sunk:
                return f"{Colors.LIGHT_RED}{self._contains.name[0]} {Colors.END}"
            else:
                return HitTile
        elif self._hit:
            return MissTile
        elif not hidden and self._contains:
            return f"{Colors.GREEN}{self} {Colors.END}"
        else:
            return EmptyTile
