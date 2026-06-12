from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .Ship import Ship


@dataclass
class Tile:
    _contains: Ship | None = field(default=None)
    _hit: bool = field(default=False)

    @property
    def hit(self) -> bool:
        return self._hit

    @hit.setter
    def hit(self, value: bool) -> None:
        if self._hit and not value:
            raise ValueError("State progression Error - Cannot revert to an un-attacked state")
        self._hit = value

    @property
    def contains(self) -> bool:
        return self._contains is not None

    @property
    def has(self) -> Optional[Ship]:
        return self._contains

    @has.setter
    def has(self, ship: Optional[Ship]):
        if self._contains is not None and ship is not None:
            raise IndexError(
                f"Collision Violation: Cannot allocate {ship.name} here. "
                f"Space is already claimed by {self._contains.name}"
            )
        self._contains = ship

    @contains.setter
    def contains(self, value) -> None:
        if self.contains:
            raise IndexError(f"Location already has {self.contains}")
        self._contains = value

    def get_rendered_logo(self, hidden: bool = True) -> str:
        from .GameRules import Colors, HitTile, MissTile, EmptyTile

        if self._hit and self._contains:
            if self._contains.is_sunk:
                return f"{Colors.LIGHT_RED}{self._contains.name[0]} {Colors.END}"
            return HitTile
        if self._hit:
            return MissTile
        if not hidden and self._contains:
            return f"{Colors.GREEN}{self._contains.name[0]} {Colors.END}"
        return EmptyTile
