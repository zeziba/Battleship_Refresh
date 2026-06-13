# tests/test_custom_config.py
import src
from src.Game import Game, Difficulty
from src.Player import Difficulty


def test_default_config_initialization():
    assert src.config.board_height == 10
    assert src.config.board_width == 10


def test_custom_dimensions():
    src.config.board_height = 15
    src.config.board_width = 15

    game = Game(players=(Difficulty.EASY, Difficulty.MEDIUM), config=src.config)

    assert game.config.board_width == 15
    assert game.config.board_height == 15


def test_subsequent_isolation():
    assert src.config.board_height == 10
    assert src.config.board_width == 10
