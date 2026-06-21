from __future__ import annotations
import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generator, Optional

from . import GameRules

if TYPE_CHECKING:
    from .Ship import Ship


class BattleShipAI(ABC):
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
            shot = self.priority_targets.pop(0)
            if shot in self.potential_shots:
                self.potential_shots.remove(shot)
            self.shots_taken.add(shot)
            return shot

        shot = self._get_consistent_random_shot()
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

    def _generate_around_shot(self, shot: tuple[int, int]) -> Generator[tuple[int, int]]:
        x, y = shot
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_width and 0 <= ny < self.board_height:
                yield nx, ny

    def _generate_targets_around(self, shot: tuple[int, int]):
        for nx, ny in self._generate_around_shot(shot):
            potential_shot = (nx, ny)
            if (potential_shot not in self.shots_taken) and (potential_shot not in self.priority_targets):
                self.priority_targets.append(potential_shot)

    def _get_consistent_random_shot(self) -> tuple[int, int]:
        better_options = []
        for x, y in self.potential_shots:
            adjacent_tiles = self._generate_around_shot((x, y))

            has_neighboring_miss = any(
                (nx, ny) in self.shots_taken and (nx, ny) not in self.unsunk_hits for nx, ny in adjacent_tiles
            )

            if not has_neighboring_miss:
                better_options.append((x, y))

        pool = better_options if better_options else self.potential_shots
        return random.choice(pool)


class HuntAndTargetAIAdv(BattleShipAI):

    def __init__(self, width: int, height: int):
        super().__init__()
        self.shots_taken = set()
        self.board_width = width
        self.board_height = height

        self.unsunk_hits: list[tuple[int, int]] = []
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
                if (potential_shot not in self.shots_taken) and (potential_shot not in self.potential_targets):
                    self.potential_targets.append(potential_shot)

    def _rebuild_potential_shots(self):
        self.potential_targets.clear()
        target_heatmap = {}

        for hit in self.unsunk_hits:
            hx, hy = hit

            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for dx, dy in directions:
                for i in range(1, self.smallest_ship_left):
                    nx, ny = hx + (dx * i), hy + (dy * i)

                    if 0 <= nx < self.board_width and 0 <= ny < self.board_height:
                        coord = nx, ny

                        if coord in self.shots_taken:
                            continue

                        if coord not in target_heatmap:
                            target_heatmap[coord] = 0
                        target_heatmap[coord] += 1
                    else:
                        break
        if target_heatmap:
            sorted_targets = sorted(target_heatmap.items(), key=lambda item: item[1], reverse=True)
            self.potential_targets = [coord for coord, weight in sorted_targets]

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
