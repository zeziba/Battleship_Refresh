from dataclasses import dataclass, field
from enum import auto, StrEnum
from typing import Optional

from Logger import get_logger

logger = get_logger(__name__)

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
    _fleet: Optional[dict[FleetType, Ship]] = None
    fleet_comp: dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        logger.debug("Post Init for GeneralFleet")
        rule_map = {
            FleetType.CARRIER: "CARRIER",
            FleetType.BATTLESHIP: "BATTLESHIP",
            FleetType.PATROLBOAT: "PATROLBOAT",
            FleetType.SUBMARINE: "SUBMARINE",
            FleetType.DESTROYER: "DESTROYER"
        }

        if self.fleet_comp:
            temp = dict()
            for enum_type, rule_name in rule_map.items():
                ship_length = GameRules.FLEET[rule_name]
                temp[enum_type] = Ship(name=rule_name, length=ship_length)

            self._fleet = temp

            return
        

        self._fleet = dict()
        for enum_type, rule_name in rule_map.items():
            ship_length = GameRules.FLEET[rule_name]
            self._fleet[enum_type] = Ship(name=rule_name, length=ship_length)

    @property
    def ships(self) -> list[Ship]:
        logger.debug("Getting GeneralFleet._fleet as list(Ship)")
        if not self._fleet:
            return list()
        return list(self._fleet.values())
    
    @property
    def all_sunk(self):
        logger.debug("Checking if each ship is sunk")
        return all(ship.is_sunk for ship in self.ships)

    def hit(self, px: int, py: int) -> bool:
        logger.debug(f"Checking if ({px}, {py}) is a hit")
        for ship in self.ships:
            if ship.hit(px, py):
                return True
        return False

    def other_ships(self, target_ship: Ship):
        logger.debug("Checking if ship is the target ship")
        for ship in self.ships:
            if ship is target_ship:
                continue
            yield ship
