import pytest
from unittest.mock import MagicMock, patch

from src import GameRules
from src.AI import Random, HuntAndTargetAIAdv, ProbabilityAI


class TestBattleShipAISuite:

    @pytest.fixture
    def mock_game_rules(self):
        with patch("src.GameRules.SIZE", 10), patch("src.GameRules.FLEET", {"Carrier": 5, "PatrolBoat": 2}):
            yield

    @pytest.fixture
    def fresh_random_ai(self, mock_game_rules) -> Random:
        return Random()

    @pytest.fixture
    def fresh_hunt_ai(self, mock_game_rules) -> HuntAndTargetAIAdv:
        return HuntAndTargetAIAdv()

    # @pytest.fixture
    # def fresh_probability_ai(self, mock_game_rules) -> ProbabilityAI:
    #     return ProbabilityAI()

    # Tests for Random AI Strategy
    def test_random_ai_initialization(self, fresh_random_ai):
        assert len(fresh_random_ai.shots_taken) == 0
        assert len(fresh_random_ai.targets) == 0
        assert len(fresh_random_ai.potential_shots) > 0
        assert len(fresh_random_ai.left_overs) > 0

        total_spaces = len(fresh_random_ai.potential_shots) + len(fresh_random_ai.left_overs)
        assert total_spaces == fresh_random_ai.board_size**2

    def test_random_ai_get_shot_drains_potential_shots_first(self, fresh_random_ai):
        initial_potential_count = len(fresh_random_ai.potential_shots)

        for _ in range(initial_potential_count):
            x, y = fresh_random_ai.get_shot()
            assert (x, y) in fresh_random_ai.shots_taken

        assert len(fresh_random_ai.potential_shots) == 0

        x_left, y_left = fresh_random_ai.get_shot()
        assert (x_left, y_left) in (fresh_random_ai.shots_taken)

    def test_random_ai_register_hit_populates_targets(self, fresh_random_ai):
        assert len(fresh_random_ai.targets) == 0

        fresh_random_ai.register_hit(5, 5, has_sunk=False)

        assert len(fresh_random_ai.targets) == 4
        assert (4, 5) in fresh_random_ai.targets

    # Tests for HuntAndTargetAIAdv Strategy
    def test_hunt_ai_smallest_ship_left(self, fresh_hunt_ai):
        assert fresh_hunt_ai.smallest_ship_left == min(fresh_hunt_ai.ships_left.values())

        fresh_hunt_ai.ships_left = {"Carrier": 5, "Battleship": 4}
        assert fresh_hunt_ai.smallest_ship_left == 4

        fresh_hunt_ai.ships_left = {}
        assert fresh_hunt_ai.smallest_ship_left == 2

    def test_hunt_ai_rebuild_potential_shots_changes_parity_grid(self, fresh_hunt_ai):
        fresh_hunt_ai.potential_shots.clear()
        fresh_hunt_ai.ships_left = {"Battleship": 4}

        fresh_hunt_ai.rebuild_potential_shots()

        for x, y in fresh_hunt_ai.potential_shots:
            assert (x + y) % 4 == 0

    def test_hunt_ai_get_shot_prioritizes_targets_stack(self, fresh_hunt_ai):
        fresh_hunt_ai.targets.append((7, 7))

        x, y = fresh_hunt_ai.get_shot()
        assert (x, y) == (7, 7)
        assert len(fresh_hunt_ai.targets) == 0

