from dataclasses import dataclass, field
from enum import Enum, auto

import GameRules
import Ship

Fleet = Enum("Fleet", {name: auto() for name in GameRules.FLEET})
FLEET = {ship: GameRules.FLEET[ship.name] for ship in list(Fleet)}


@dataclass
class GeneralFleet:
    __fleet: dict[Fleet : Ship.Ship] = field(default_factory=dict)

    @property
    def fleet(self) -> dict:
        return self.__fleet

    def generate(self) -> None:
        self.__fleet = dict()
        for ship in list(Fleet):
            # Random directionality choice for now
            self.__fleet[ship] = Ship.Ship(ship.name, FLEET[ship])

    def hit(self, px: int, py: int) -> bool:
        for ship in self.fleet:
            if self.fleet[ship].hit(px, py):
                return True
        return False

    def other_ships(self, ship: Fleet) -> iter:
        for other_ship in self.fleet:
            if ship is other_ship:
                continue
            yield self.fleet[other_ship]

    def can_place(self, ship: Fleet, sx: int, sy: int) -> bool:
        if GameRules.check_xy(sx, sy):
            x, y = sx, sy
            if ship.directionality is Ship.Direction.HORIZONTAL:
                x += ship.length
            else:
                y += ship.length
            if GameRules.check_xy(x, y):
                possible = Ship.Ship.possible_places(
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
