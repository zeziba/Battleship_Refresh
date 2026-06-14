import pytest
from unittest.mock import patch

# Adjust the import path according to your test file location
from src import GameConfig, config, GameRules

"""
Auto-generated Test File
"""


class TestGameConfig:
    @pytest.fixture
    def custom_fleet(self):
        """Provides a controlled, custom fleet structure for dynamic configuration checks."""
        return {"Carrier": 5, "Battleship": 4, "Destroyer": 3}

    # --- Initialization & Default Checks ---

    def test_default_initialization(self):
        """Verifies that a fresh GameConfig maps directly to fallback specifications in GameRules."""
        fresh_config = GameConfig()

        assert fresh_config.board_width == GameRules.SIZE
        assert fresh_config.board_height == GameRules.SIZE
        assert fresh_config.fleet_composition == GameRules.FLEET

    def test_custom_initialization(self, custom_fleet):
        """Verifies that custom dimensions and parameters populate correctly on override instantiation."""
        custom_config = GameConfig(board_width=15, board_height=12, fleet_composition=custom_fleet)

        assert custom_config.board_width == 15
        assert custom_config.board_height == 12
        assert custom_config.fleet_composition == custom_fleet

    # --- State Mutation Clearing (reset_defaults) ---

    def test_reset_defaults_restores_dimensions(self):
        """Ensures that modified dimensions are properly reverted back to base GameRules defaults."""
        test_config = GameConfig(board_width=20, board_height=20)

        # Mutate dimensions further
        test_config.board_width = 8
        test_config.board_height = 8

        # Execute reset hook
        test_config.reset_defaults()

        assert test_config.board_width == GameRules.SIZE
        assert test_config.board_height == GameRules.SIZE

    def test_reset_defaults_copies_fleet_composition(self, custom_fleet):
        """Verifies that reset_defaults breaks reference checking by forcing a copy of GameRules.FLEET."""
        with patch.dict(GameRules.FLEET, custom_fleet, clear=True):
            test_config = GameConfig()

            # Alter the active configuration fleet dictionary
            test_config.fleet_composition["Carrier"] = 99

            # Reset should restore the current state of GameRules.FLEET
            test_config.reset_defaults()

            assert custom_fleet == test_config.fleet_composition

            # Verify it is a true copy, ensuring isolated pointer reference memory allocations
            assert test_config.fleet_composition is not GameRules.FLEET

    # --- Global Shared Instance Integrity ---

    def test_global_singleton_instance(self):
        """Validates that the package-level imported configuration acts as a reliable reference target."""
        assert isinstance(config, GameConfig)

        # Verify changes to the global instance persist until reset is explicitly called
        try:
            original_width = config.board_width
            config.board_width = 42
            assert config.board_width == 42
        finally:
            # Clean up after the test execution to avoid leaky test bugs across files
            config.reset_defaults()
