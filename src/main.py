import sys

from Game import Game, GameConfig
from Player import Difficulty, create_player
import name_generator as Names

from Logger import get_logger

logger = get_logger(__name__)


def run():
    print("Welcome to Battleship")
    logger.debug("Starting Game")

    config = GameConfig()
    names = Names.NameGanerator()

    p1_mode = Difficulty.MEDIUM
    p1_name = f"(1) Admiral {names.create_random_name()}"
    p1 = create_player(p1_name, p1_mode, config.board_width, config.board_width, config.fleet_composition)

    p2_mode = Difficulty.MEDIUM
    p2_name = f"(2) Admiral {names.create_random_name()}"
    p2 = create_player(p2_name, p2_mode, config.board_width, config.board_width, config.fleet_composition)

    player_tuple = (p1.difficulty, p2.difficulty)
    player_dict = {p1.name: p1, p2.name: p2}

    logger.debug("Init match engine")
    match_engine = Game(players=player_tuple, players_dict=player_dict)
    logger.debug("Running set_up on match engine")
    match_engine.set_up()
    logger.debug("Taking turns with match engine")
    match_engine.take_turns()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        logger.debug("Exiting game loop")
        sys.exit(0)
