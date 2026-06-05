import random
import GameRules


class HuntAndTargetAI:

    def __init__(self):
        self.shots_taken = set()
        self.potential_shots = []
        self.targets = []
        self.board_size = GameRules.SIZE

        for x in range(GameRules.SIZE):
            for y in range(GameRules.SIZE):
                if (x + y) % 2 == 0:
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
    
    def register_hit(self, x: int, y: int):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x +dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if (nx, ny) not in self.shots_taken:
                    self.targets.append((nx, ny))


class HuntAndTargetAIAdv:

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
    
    def register_hit(self, x: int, y: int):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x +dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if (nx, ny) not in self.shots_taken:
                    self.targets.append((nx, ny))