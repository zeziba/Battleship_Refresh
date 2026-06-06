from dataclasses import dataclass, field
from enum import Enum, auto

import GameRules
from Ship import Ship, Direction

Fleet: Enum = Enum("Fleet", {name: auto() for name in GameRules.FLEET})
FLEET: dict[str, int] = {ship: GameRules.FLEET[ship.name] for ship in list(Fleet)} # pyright: ignore[reportArgumentType]


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
