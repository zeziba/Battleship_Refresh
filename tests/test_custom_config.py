import pytest
from unittest.mock import patch
import src
from src import GameConfig, GameRules
from src.Game import Game
from src.Player import Difficulty
from src.main import build_game


class TestCustomConfig:
    @pytest.fixture(autouse=True)
    def auto_cleanup_config(self):
        """
        Autouse fixture ensuring that every individual test execution starts
        with a clean configuration environment and clears states afterward.
        """
        src.config.reset_defaults()
        yield
        src.config.reset_defaults()

    def test_default_config_initialization(self):
        """Verifies that the global configuration boots with established baseline parameters."""
        assert src.config.board_height == 10
        assert src.config.board_width == 10

    def test_custom_dimensions(self):
        """
        Ensures that modifying global layout parameters accurately propagates down
        to structural components and game-ready players via build_game.
        """
        # Mutate the global configuration directly before building the session entities
        src.config.board_height = 15
        src.config.board_width = 15

        # Replicate main.py initialization factory logic flow exactly
        game = build_game(Difficulty.MEDIUM, Difficulty.EASY)

        # Extract the initialized component players to verify grid space allocations
        for player in game.players_dict.values():
            assert player.board.width == 15
            assert player.board.height == 15

    def test_subsequent_isolation(self):
        """Confirms that previous modifications do not bleed over into standalone execution runs."""
        assert src.config.board_height == 10
        assert src.config.board_width == 10

    def test_reset_defaults_clears_fleet_mutations(self):
        """
        Verifies that adding a custom ship can be cleanly discarded by reset_defaults()
        without mutating the underlying baseline definitions inside GameRules.
        """
        mock_fleet = {"Carrier": 5, "Battleship": 4, "Destroyer": 3}

        with patch.dict(GameRules.FLEET, mock_fleet, clear=True):
            test_config = GameConfig()

            assert len(test_config.fleet_composition) == 3

            # Simulate a dynamic runtime runtime modification
            test_config.fleet_composition["Submarine"] = 99
            assert "Submarine" in test_config.fleet_composition

            # Fire configuration normalization cleanup hook
            test_config.reset_defaults()

            # Confirm the configuration successfully stripped the mutated submarine key
            assert "Submarine" not in test_config.fleet_composition
            assert len(test_config.fleet_composition) == 3
            assert test_config.fleet_composition == mock_fleet
