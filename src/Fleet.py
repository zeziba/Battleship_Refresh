from dataclasses import dataclass, field
from enum import auto, StrEnum

import GameRules
from Ship import Ship

class FleetType(StrEnum):
    CARRIER = auto()
    BATTLESHIP = auto()
    PATROLBOAT = auto()
    SUBMARINE = auto()
    DESTROYER = auto()


@dataclass
class GeneralFleet:
    _fleet: dict[FleetType, Ship] = field(default_factory=dict)

    def __post_init__(self):
        rule_map = {
            FleetType.CARRIER: "CARRIER",
            FleetType.BATTLESHIP: "BATTLESHIP",
            FleetType.PATROLBOAT: "PATROLBOAT",
            FleetType.SUBMARINE: "SUBMARINE",
            FleetType.DESTROYER: "DESTROYER"
        }

        if self._fleet:
            temp = dict()
            for enum_type, rule_name in rule_map.items():
                ship_length = GameRules.FLEET[rule_name]
                temp[enum_type] = Ship(name=rule_name, length=ship_length)

            self._fleet = temp

            return
        

        for enum_type, rule_name in rule_map.items():
            ship_length = GameRules.FLEET[rule_name]
            self._fleet[enum_type] = Ship(name=rule_name, length=ship_length)

    @property
    def ships(self) -> list[Ship]:
        return list(self._fleet.values())
    
    @property
    def all_sunk(self):
        return all(ship.is_sunk for ship in self.ships)

    def hit(self, px: int, py: int) -> bool:
        for ship in self.ships:
            if ship.hit(px, py):
                return True
        return False

    def other_ships(self, target_ship: Ship):
        for ship in self.ships:
            if ship is target_ship:
                continue
            yield ship
