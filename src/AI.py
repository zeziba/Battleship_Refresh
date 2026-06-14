from __future__ import annotations
import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from . import GameRules

if TYPE_CHECKING:
    from .Ship import Ship


class BattleShipAI(ABC):
    shots_taken: set = set()

    @abstractmethod
    def get_shot(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def register_result(self, shot: tuple[int, int], has_hit: bool, sunk_ship: Optional[Ship] = None) -> None:
        pass


class Random(BattleShipAI):

    def __init__(self, width: int, height: int):
        self.board_width = width
        self.board_height = height
        self.shots_taken: set = set()
        self.priority_targets: list[tuple[int, int]] = []
        self.potential_shots: list[tuple[int, int]] = []
        self.unsunk_hits: list[tuple[int, int]] = []

        for x in range(self.board_width):
            for y in range(self.board_height):
                self.potential_shots.append((x, y))

    def get_shot(self) -> tuple[int, int]:
        if self.priority_targets:
            shot = self.priority_targets.pop(random.randint(0, len(self.priority_targets) - 1))
            if shot in self.potential_shots:
                self.potential_shots.remove(shot)
            self.shots_taken.add(shot)
            return shot

        if not self.potential_shots:
            raise IndexError("No more potential shots on the board")

        shot = random.choice(self.potential_shots)
        self.potential_shots.remove(shot)
        self.shots_taken.add(shot)
        return shot

    def register_result(self, shot: tuple[int, int], has_hit: bool, sunk_ship: Optional[Ship] = None):
        if has_hit:
            self.unsunk_hits.append(shot)
            if sunk_ship:
                self.unsunk_hits = [pos for pos in self.unsunk_hits if not sunk_ship.contains(pos[0], pos[1])]
                self._rebuild_priority_targets()
            else:
                self._generate_targets_around(shot)

    def _rebuild_priority_targets(self):
        self.priority_targets.clear()
        for hit in self.unsunk_hits:
            self._generate_targets_around(hit)

    def _generate_targets_around(self, shot: tuple[int, int]):
        x, y = shot
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_width and 0 <= ny < self.board_height:
                potential_shot = (nx, ny)
                if (potential_shot not in self.shots_taken) and (potential_shot not in self.priority_targets):
                    self.priority_targets.append(potential_shot)


class HuntAndTargetAIAdv(BattleShipAI):

    def __init__(self, width: int, height: int):
        super().__init__()
        self.board_width = width
        self.board_height = height

        self.unsunk_hits: list[tuple[int, int]] = []
        self.fired_shots: list[tuple[int, int]] = []
        self.potential_targets: list[tuple[int, int]] = []

        self.ships_left = GameRules.FLEET.copy()

    @property
    def smallest_ship_left(self):
        if self.ships_left:
            return min(self.ships_left.values())
        return 2

    def get_shot(self) -> tuple[int, int]:
        while self.potential_targets:
            shot = self.potential_targets.pop(0)
            if shot not in self.shots_taken:
                self.shots_taken.add(shot)
                return shot

        if self.unsunk_hits:
            self._rebuild_potential_shots()
            if self.potential_targets:
                shot = self.potential_targets.pop()
                self.shots_taken.add(shot)
                return shot

        shot = self._get_hunt_shot()
        self.shots_taken.add(shot)
        return shot

    def register_result(self, shot: tuple[int, int], has_hit: bool, sunk_ship: Optional[Ship] = None):
        if has_hit:
            self.unsunk_hits.append(shot)
            if sunk_ship:
                if sunk_ship.name in self.ships_left:
                    self.ships_left.pop(sunk_ship.name)
                self.unsunk_hits = [pos for pos in self.unsunk_hits if not sunk_ship.contains(pos[0], pos[1])]
            else:
                self._generate_targets_around(shot)

    def _generate_targets_around(self, shot: tuple[int, int]):
        x, y = shot
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_width and 0 <= ny < self.board_height:
                potential_shot = (nx, ny)
                if (potential_shot not in self.fired_shots) and (potential_shot not in self.potential_targets):
                    self.potential_targets.append(potential_shot)

    def _rebuild_potential_shots(self):
        self.potential_targets.clear()
        for hit in self.unsunk_hits:
            self._generate_targets_around(hit)

    def _get_hunt_shot(self) -> tuple[int, int]:
        left_over_shots = [
            (x, y)
            for x in range(self.board_width)
            for y in range(self.board_height)
            if (x, y) not in self.shots_taken
            if (x + y) % self.smallest_ship_left == 0
        ]

        if not left_over_shots:
            left_over_shots = [
                (x, y)
                for x in range(self.board_width)
                for y in range(self.board_height)
                if (x, y) not in self.shots_taken
            ]

        return random.choice(left_over_shots)


class ProbabilityAI(BattleShipAI):
    pass
