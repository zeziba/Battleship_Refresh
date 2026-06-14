from dataclasses import dataclass, field
from typing import Generator, Tuple

from .Logger import get_logger

from . import Player

TESTING = False
logger = get_logger(__name__)

Difficulty = Player.Difficulty


@dataclass
class TurnResult:
    turnNumber: int
    attacker: Player.Player
    defender: Player.Player
    shot_x: int
    shot_y: int
    hit: bool
    sunk_ship: str = ""
    game_over: bool = False


@dataclass()
class Game:
    """
    Create and maintain the differing objects to enable a game of battleship to be played.

    The rules of the game are "simple."
    """

    players_dict: dict[str, Player.Player] = field(default_factory=dict)

    @property
    def _get_turn(self) -> Generator[Tuple[int, Player.Player, Player.Player], None, None]:
        turn = 1
        players: list[Player.Player] = list(self.players_dict.values())
        attacker, defender = players[0], players[1]
        while True:
            attacker, defender = defender, attacker
            yield turn, attacker, defender

            turn += 1

    def take_turns(self):
        for turn, attacker, defender in self._get_turn:
            shot_x, shot_y, is_hit, sunk_ship = attacker.take_turn(defender)

            game_over = defender.fleet.all_sunk

            yield TurnResult(
                turnNumber=turn,
                attacker=attacker,
                defender=defender,
                shot_x=shot_x,
                shot_y=shot_y,
                hit=is_hit,
                sunk_ship=sunk_ship,
                game_over=game_over,
            )
