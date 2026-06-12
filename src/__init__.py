from dataclasses import dataclass, field

from src import GameRules


@dataclass
class GameConfig:
    board_width: int = GameRules.SIZE
    board_height: int = GameRules.SIZE
    fleet_composition: dict = field(default_factory=lambda: GameRules.FLEET)

config = GameConfig()