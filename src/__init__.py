from dataclasses import dataclass, field

from src import GameRules


@dataclass
class GameConfig:
    board_width: int = GameRules.SIZE
    board_height: int = GameRules.SIZE
    fleet_composition: dict = field(default_factory=lambda: GameRules.FLEET)

    def reset_defaults(self):
        self.board_height = GameRules.SIZE
        self.board_width = GameRules.SIZE
        self.fleet_composition = GameRules.FLEET.copy()


config = GameConfig()
