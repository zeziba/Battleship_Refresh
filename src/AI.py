import random
import GameRules


class HuntAndTargetAI:
    shots_taken = set()
    targets = []
    board_size = GameRules.SIZE

    def __int__(self):
        pass

    def get_shot(self) -> tuple[int, int]:
        while self.targets:
            x, y = self.targets.pop()
            if (x, y) not in self.shots_taken:
                return x, y

        while True:
            x = random.randint(0, self.board_size - 1)
            y = random.randint(0, self.board_size - 1)
            if (x + y) % 2 == 0 and (x, y) not in self.shots_taken:
                self.shots_taken.add((x, y))
                return (x, y)
    
    def register_hit(self, x: int, y: int):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x +dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                if (nx, ny) not in self.shots_taken:
                    self.targets.append((nx, ny))