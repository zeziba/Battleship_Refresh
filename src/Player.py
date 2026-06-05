from dataclasses import dataclass
from enum import Enum, auto

import Board
import Fleet


class State(Enum):
    PERSON = auto()
    AI = auto()


@dataclass()
class Player:
    __name: str
    __state: State
    __board: Board.Board
    __fleet: Fleet.GeneralFleet

    @property
    def name(self):
        return self.__name

    @property
    def state(self) -> State:
        return self.__state

    @property
    def fleet(self) -> Fleet.GeneralFleet:
        return self.__fleet

    @property
    def board(self) -> Board.Board:
        return self.__board

    def generate_fleet(self) -> None:
        if self.state is State.AI:
            self.fleet.generate()
        else:
            self.fleet.generate()

    @property
    def get_ships(self) -> iter:
        for ship in self.fleet.fleet:
            yield self.fleet.fleet[ship]

    @property
    def destroyed(self) -> bool:
        if len(self.fleet.fleet) == 0:
            return True
        return all(self.fleet.fleet[ship].is_sunk for ship in self.fleet.fleet)

    def take_at_self_shot(self, x: int, y: int) -> tuple[bool, Board.Tile.Tile]:
        fleet, tile = self.fleet.hit(x, y), self.board.get(x, y)
        tile.hit = True
        return fleet, tile
