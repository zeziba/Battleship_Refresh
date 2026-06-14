from dataclasses import dataclass, field
from copy import deepcopy

from src import GameRules


@dataclass
class GameConfig:
    board_width: int = GameRules.SIZE
    board_height: int = GameRules.SIZE
    fleet_composition: dict = field(default_factory=lambda: deepcopy(GameRules.FLEET))

    def reset_defaults(self):
        self.board_height = GameRules.SIZE
        self.board_width = GameRules.SIZE
        self.fleet_composition = deepcopy(GameRules.FLEET)


config = GameConfig()


def check_xy(x: int, y: int) -> bool:
    """Checks if the x, y coords fall within the board"""
    return (0 <= x < config.board_width) and (0 <= y < config.board_height)
