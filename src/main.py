import sys

from .Game import Game
from .Player import Difficulty, create_player
from .Board import Board
import src.UI as UI
import src.name_generator as Names
from src import config as _config

from .Logger import get_logger

logger = get_logger(__name__)


def build_game(p1_difficulty: Difficulty, p2_difficulty: Difficulty) -> Game:
    names = Names.NameGenerator()

    # Setup player 1
    p1_board = Board(_config.board_width, _config.board_height)
    p1_name = f"(1) Admiral {names.create_random_name()}"
    p1 = create_player(p1_name, p1_difficulty, _config.board_width, _config.board_width, _config.fleet_composition)
    p1.generate_fleet(_config.fleet_composition)

    # Setup player 2
    p2_board = Board(_config.board_width, _config.board_height)
    p2_name = f"(2) Admiral {names.create_random_name()}"
    p2 = create_player(p2_name, p2_difficulty, _config.board_width, _config.board_width, _config.fleet_composition)
    p2.generate_fleet(_config.fleet_composition)

    player_dict = {
        p1_name: p1,
        p2_name: p2
    }

    return Game(players_dict=player_dict)


def run():
    print("Welcome to Battleship")
    logger.debug("Starting Game")

    game = build_game(Difficulty.MEDIUM, Difficulty.MEDIUM)

    for result in game.take_turns():
        UI.print_turn_result(result)
        UI.print_boards(result.attacker.name, result.attacker.board, result.defender.name, result.defender.board, result.turnNumber % 50 == 0)

        if result.game_over:
            UI.print_game_over(result.attacker.name, result.defender.board)
            break


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        logger.debug("Exiting game loop")
        sys.exit(0)
