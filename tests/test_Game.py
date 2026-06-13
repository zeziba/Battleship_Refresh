import pytest
from unittest.mock import MagicMock, patch

from src.Game import Game, Difficulty
import src.GameRules as GameRules


class TestGameSuite:

    @pytest.fixture
    def mock_ui(self):
        with patch("src.UI.UI") as mock_class:
            instance = mock_class.return_value
            instance.output = MagicMock()
            instance.clear_screen = MagicMock()
            yield instance

    @pytest.fixture
    def mock_player_classes(self):
        with patch("src.Player.Player") as mock_player:
            yield mock_player

    @pytest.fixture
    def fresh_game(self, mock_ui, mock_player_classes) -> Game:
        return Game(players=(Difficulty.EASY, Difficulty.HARD))
    
    # Initialization & Lifecycle Configuration Tests

    def test_game_post_init_flow(self, mock_ui, mock_player_classes):
        with patch("src.Game.Game.set_up") as mock_setup:
            game_instance = Game(players=(Difficulty.EASY, Difficulty.EASY))
            
            mock_setup.assert_called_once()
            assert game_instance.state == GameRules.State.STOPPED

    def test_game_stop_mutates_state(self, fresh_game):
        fresh_game.state = GameRules.State.RUNNING  # Artificially set game to active running state
        fresh_game.stop()
        assert fresh_game.state == GameRules.State.STOPPED

    def test_iter_players_generator_yields_all_values(self, fresh_game):
        mock_p1 = MagicMock()
        mock_p2 = MagicMock()
        fresh_game.players_dict = {"Player_1": mock_p1, "Player_2": mock_p2}

        yielded_players = list(fresh_game.iter_players)
        assert len(yielded_players) == 2
        assert mock_p1 in yielded_players
        assert mock_p2 in yielded_players

    # Turn Execution & Combat Loop Orchestration

    def test_take_turn_handles_already_targeted_loop(self, fresh_game, mock_ui):
        mock_attacker = MagicMock()
        mock_attacker.choose_target.side_effect = [(1, 1), (2, 2)]

        mock_defender = MagicMock()
        mock_defender.is_already_targeted.side_effect = [True, False]
        
        mock_tile = MagicMock()
        mock_tile.has = None
        mock_defender.take_at_self_shot.return_value = mock_tile

        fresh_game._take_turn(mock_attacker, mock_defender)

        assert mock_attacker.choose_target.call_count == 2
        mock_ui.output.assert_any_call(GameRules.Output.TRY_AGAIN)
        mock_defender.take_at_self_shot.assert_called_once_with(2, 2)

    def test_take_turn_notifies_ui_on_ship_hit(self, fresh_game, mock_ui):
        mock_attacker = MagicMock()
        mock_attacker.choose_target.return_value = (4, 5)

        mock_defender = MagicMock()
        mock_defender.is_already_targeted.return_value = False

        mock_ship = MagicMock()
        mock_ship.is_sunk = False
        mock_ship.name = "Cruiser"
        
        mock_tile = MagicMock()
        mock_tile.has = mock_ship
        mock_defender.take_at_self_shot.return_value = mock_tile

        fresh_game._take_turn(mock_attacker, mock_defender)

        expected_output = GameRules.Output.SHOT_AT.format(4, 5, "Cruiser")
        mock_ui.output.assert_any_call(expected_output)

    def test_take_turn_notifies_ui_on_ship_sunk(self, fresh_game, mock_ui):
        """Verify UI triggers specific SUNK_SHIP payload notification when structural threshold hits zero."""
        mock_attacker = MagicMock()
        mock_attacker.choose_target.return_value = (0, 0)
        mock_defender = MagicMock()
        mock_defender.is_already_targeted.return_value = False

        mock_ship = MagicMock()
        mock_ship.is_sunk = True
        mock_ship.name = "Submarine"
        
        mock_tile = MagicMock()
        mock_tile.has = mock_ship
        mock_defender.take_at_self_shot.return_value = mock_tile

        fresh_game._take_turn(mock_attacker, mock_defender)

        expected_output = GameRules.Output.SUNK_SHIP.format("Submarine")
        mock_ui.output.assert_any_call(expected_output)

    # Core Match Loop Sequencing Tests

    def test_take_turns_clears_screen_at_intervals(self, fresh_game, mock_ui):
        mock_attacker = MagicMock()
        mock_defender = MagicMock()
        
        with patch.object(Game, "_get_turn", new_callable=property) as mock_get_turn:
            mock_get_turn.return_value = [ # pyright: ignore[reportAttributeAccessIssue]
                (0, mock_attacker, mock_defender),
                (1, mock_attacker, mock_defender),
                (2, mock_attacker, mock_defender)
            ]
            
            # Patch child loop step out to avoid downstream exception generation
            with patch.object(Game, "_take_turn") as mock_single_turn_step:
                fresh_game.take_turns()
                
                # Turn 0 triggers clear, plus initial entry call, turn 3 isn't reached here
                # Check your code structure: calls at entry, and if turn % 3 == 0 inside loop
                assert mock_ui.clear_screen.call_count >= 2