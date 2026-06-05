from dataclasses import dataclass, field
from enum import Enum, auto

import GameRules
from Ship import Ship, Direction

Fleet: Enum = Enum("Fleet", {name: auto() for name in GameRules.FLEET})
FLEET = {ship: GameRules.FLEET[ship.name] for ship in list(Fleet)} # pyright: ignore[reportArgumentType]


@dataclass
class GeneralFleet:
    _fleet: dict[Fleet, Ship] = field(default_factory=dict) # pyright: ignore[reportInvalidTypeForm]

    @property
    def fleet(self) -> dict:
        return self._fleet

    def generate(self) -> None:
        self._fleet = dict()
        for ship in list(Fleet): # pyright: ignore[reportArgumentType]
            # Random directionality choice for now
            self._fleet[ship] = Ship(ship.name, FLEET[ship])

    def hit(self, px: int, py: int) -> bool:
        for ship in self.fleet:
            if self.fleet[ship].hit(px, py):
                return True
        return False

    def other_ships(self, ship: Fleet): # pyright: ignore[reportInvalidTypeForm]
        for other_ship in self.fleet:
            if ship is other_ship:
                continue
            yield self.fleet[other_ship]

    def can_place(self, ship: Fleet, sx: int, sy: int) -> bool: # pyright: ignore[reportInvalidTypeForm]
        if GameRules.check_xy(sx, sy):
            x, y = sx, sy
            if ship.directionality is Direction.HORIZONTAL:
                x += ship.length
            else:
                y += ship.length
            if GameRules.check_xy(x, y):
                possible = Ship.possible_places(
                    sx, sy, ship.length, ship.directionality
                )
                if any(
                    other.contains(px, py)
                    for other in self.other_ships(ship)
                    for px, py in possible
                ):
                    return False
                return True
            return False
        return False
