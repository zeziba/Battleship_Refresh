from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Generator

if TYPE_CHECKING:
    import Board
    import Fleet
    import Ship
    from AI import BattleShipAI


class State(Enum):
    PERSON = auto()
    AI = auto()


@dataclass()
class Player:
    _name: str
    _state: State
    _board: Board.Board
    _fleet: Fleet.GeneralFleet
    _ai_brain: BattleShipAI | None = None

    @property
    def name(self):
        return self._name

    @property
    def state(self) -> State:
        return self._state

    @property
    def fleet(self) -> Fleet.GeneralFleet:
        return self._fleet

    @property
    def board(self) -> Board.Board:
        return self._board

    def generate_fleet(self) -> None:
        if self.state is State.AI:
            self.fleet.generate()
        else:
            self.fleet.generate()

    @property
    def get_ships(self) -> Generator[Ship.Ship, Any, None]:
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
