from __future__ import annotations
import sys
import uuid

from .Game import Game
from .Player import Difficulty, create_player
from .Board import Board
from .Ship import Direction
import src.UI as UI
import src.name_generator as Names
from src import config as _config
from .Stats import GameStatTracker, MatchTelemetry, ChronologicalShot, DB_FILE, display_database_summary

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Player import Player

from .Logger import get_logger

logger = get_logger(__name__)


def build_game(p1_difficulty: Difficulty, p2_difficulty: Difficulty) -> Game:
    names = Names.NameGenerator()

    # Setup player 1
    p1_board = Board(_config.board_width, _config.board_height)
    p1_name = f"(1) Admiral {names.create_random_name()}"
    p1 = create_player(p1_name, p1_difficulty, p1_board, _config.fleet_composition)
    p1.generate_fleet(_config.fleet_composition)

    # Setup player 2
    p2_board = Board(_config.board_width, _config.board_height)
    p2_name = f"(2) Admiral {names.create_random_name()}"
    p2 = create_player(p2_name, p2_difficulty, p2_board, _config.fleet_composition)
    p2.generate_fleet(_config.fleet_composition)

    player_dict = {p1_name: p1, p2_name: p2}

    return Game(players_dict=player_dict)


def build_player_telemetry(name: str, player: Player):
    tel = MatchTelemetry(name, player.difficulty)
    for ship in player.fleet.ships:
        _x, _y = list(ship._positions.keys())[0]
        tel.record_placement(
            name=ship.name,
            x=_x,
            y=_y,
            orientation="H" if ship.directionality == Direction.HORIZONTAL else "V",
            size=ship.length,
        )
    return tel


def run():
    UI.output("Welcome to Battleship")
    tracker = GameStatTracker(DB_FILE)
    current_game_id = str(uuid.uuid4())[:8]
    logger.debug("Starting Game")

    game = build_game(Difficulty.EASY, Difficulty.MEDIUM)

    telemetry_profiles: dict[str, MatchTelemetry] = {}
    logger.debug(f"Building Telemetry data")
    for name, player in game.players_dict.items():
        telemetry_profiles[name] = build_player_telemetry(name, player)

    global_timeline: list[ChronologicalShot] = []
    global_turn_counter = 0

    for result in game.take_turns():
        UI.print_turn_result(result)
        UI.print_boards(
            result.attacker.name,
            result.attacker.board,
            result.defender.name,
            result.defender.board,
            # result.turnNumber % 50 == 0,
        )

        global_turn_counter += 1
        attacker_tel = telemetry_profiles[result.attacker.name]

        sunk_name = result.sunk_ship if hasattr(result, "sunk_ship") and result.sunk_ship else None

        global_timeline.append(
            ChronologicalShot(
                player_id=attacker_tel.player_id,
                turn_sequence=global_turn_counter,
                x=result.shot_x,
                y=result.shot_y,
                outcome=result.hit,
                sunk_ship_name=sunk_name,
            )
        )

        if result.game_over:
            UI.print_game_over(result.attacker.name, result.defender.board)

            winner_tel = telemetry_profiles[result.attacker.name]
            loser_tel = telemetry_profiles[result.defender.name]

            tracker.register_match_entities(current_game_id, winner_tel, loser_tel, result.turnNumber)
            tracker.batch_write_shots(current_game_id, global_timeline)

            break

    display_database_summary(DB_FILE)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        logger.debug("Exiting game loop")
        sys.exit(0)
