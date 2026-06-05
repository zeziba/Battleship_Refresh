from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

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
        if not self.hit:
            self._hit = value

    @property
    def contains(self) -> bool:
        return self._contains is not None

    @contains.setter
    def contains(self, value) -> None:
        if self.contains is True:
            raise IndexError(f"Location already has {self.contains}")
        self._contains = value

    @property
    def has(self) -> object:
        return self._contains

    @property
    def title_logo(self, hidden: bool = True) -> str:
        # TODO: Finish implementation
        raise NotImplemented
        if hidden:
            if self.contains:
                if self.hit:
                    pass
                else:
                    pass
        else:
            if self.contains:
                if self.hit:
                    pass
                else:
                    pass
        return GameRules.EmptyTile
