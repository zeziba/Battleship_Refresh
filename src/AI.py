import random
from abc import ABC, abstractmethod

from . import GameRules


class BattleShipAI(ABC):
    shots_taken: set
    potential_shots: list
    targets: list
    board_size: int
    ships_left: dict[str, int]

    @abstractmethod
    def get_shot(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def register_hit(self, x: int, y: int, has_sunk: bool = False) -> None:
        pass


class Random(BattleShipAI):

    def __init__(self):
        self.shots_taken = set()
        self.potential_shots = []
        self.targets = []
        self.board_size = GameRules.SIZE
        self.ships_left = GameRules.FLEET.copy()
        self.left_overs = []

        for x in range(GameRules.SIZE):
            for y in range(GameRules.SIZE):
                if (x + y) % 2 == 0:
                    self.potential_shots.append((x, y))
                else:
                    self.left_overs.append((x, y))

    def get_shot(self) -> tuple[int, int]:
        if self.potential_shots:
            x, y = random.choice(self.potential_shots)
            self.potential_shots.remove((x, y))
            self.shots_taken.add((x, y))
            return x, y

        x, y = random.choice(self.left_overs)
        self.left_overs.remove((x, y))
        return x, y

    def register_hit(self, x: int, y: int, has_sunk: bool = False):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if (nx, ny) not in self.shots_taken:
                    self.targets.append((nx, ny))


class HuntAndTargetAIAdv(BattleShipAI):

    def __init__(self):
        self.shots_taken = set()
        self.potential_shots = []
        self.targets = []
        self.board_size = GameRules.SIZE
        self.ships_left = GameRules.FLEET.copy()

        for x in range(GameRules.SIZE):
            for y in range(GameRules.SIZE):
                if (x + y) % 2 == 0:
                    self.potential_shots.append((x, y))

    @property
    def smallest_ship_left(self):
        if self.ships_left:
            return min(self.ships_left.values())
        return 2

    def rebuild_potential_shots(self):
        smallest = self.smallest_ship_left
        for x in range(GameRules.SIZE):
            for y in range(GameRules.SIZE):
                if (x + y) % smallest != 0:
                    continue
                if (x, y) in self.shots_taken:
                    continue
                self.potential_shots.append((x, y))

    def get_shot(self) -> tuple[int, int]:
        while self.targets:
            x, y = self.targets.pop()
            if (x, y) in self.potential_shots:
                self.potential_shots.remove((x, y))
            self.shots_taken.add((x, y))
            return x, y

        if self.potential_shots:
            x, y = random.choice(self.potential_shots)
            self.potential_shots.remove((x, y))
            self.shots_taken.add((x, y))
            return x, y

        while True:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if (x, y) not in self.shots_taken:
                self.shots_taken.add((x, y))
                return (x, y)

    def register_hit(self, x: int, y: int, has_sunk: bool = False):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if (nx, ny) not in self.shots_taken:
                    self.targets.append((nx, ny))
        if has_sunk:
            self.rebuild_potential_shots()


class ProbabilityAI(BattleShipAI):
    _starting_ships: dict[str, int]

    def __init__(self) -> None:
        self.board_size = GameRules.SIZE

    @property
    def starting_ships(self):
        return self._starting_ships

    @starting_ships.setter
    def starting_ships(self, ships):
        self._starting_ships = ships
