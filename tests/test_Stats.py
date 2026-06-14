import pytest
import sqlite3
from unittest.mock import patch
from math import trunc

from src.Player import Difficulty
from src.Stats import GameStatTracker


class TestGameStatTracker:

    @pytest.fixture
    def mock_db_tracker(self):
        """
        Fixture that forces GameStatTracker to use a SINGLE, persistent
        in-memory SQLite database connection for the duration of the test.
        """
        # 1. Spin up a single connection that stays alive in RAM
        persistent_conn = sqlite3.connect(":memory:")

        # 2. Force the tracker to always return this specific connection
        with patch.object(GameStatTracker, "_get_connection", return_value=persistent_conn):
            # The tracker will now instantiate and run _init_db() on our persistent connection
            tracker = GameStatTracker()
            yield tracker

        # 3. Clean up the connection after the test completes
        persistent_conn.close()

    def test_database_initialization(self, mock_db_tracker):
        """Verifies that the database successfully bootstraps the game_history table."""
        with mock_db_tracker._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game_history';")
            table_exists = cursor.fetchone()

        assert table_exists is not None
        assert table_exists[0] == "game_history"

    def test_record_game_inserts_row(self, mock_db_tracker):
        """Confirms that executing record_game writes clean entries into the data table."""
        mock_db_tracker.record_game(Difficulty.EASY, Difficulty.MEDIUM, total_turns=42)

        with mock_db_tracker._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT winner_difficulty, loser_difficulty, total_turns FROM game_history;")
            rows = cursor.fetchall()

        assert len(rows) == 1
        assert rows[0][0] == Difficulty.EASY.value
        assert rows[0][1] == Difficulty.MEDIUM.value
        assert rows[0][2] == 42

    def test_display_summary_with_no_games(self, mock_db_tracker):
        """Ensures display_summary cleanly handles an empty database table without crashing."""
        with patch("src.Stats.output") as mock_output:
            mock_db_tracker.display_summary()

            assert mock_output.called

    def test_display_summary_formatting_and_math(self, mock_db_tracker):
        """Validates dynamic SQL aggregations, metrics computations, and print formatting blocks."""
        mock_db_tracker.record_game(Difficulty.EASY, Difficulty.MEDIUM, total_turns=30)
        mock_db_tracker.record_game(Difficulty.EASY, Difficulty.HARD, total_turns=40)
        mock_db_tracker.record_game(Difficulty.MEDIUM, Difficulty.EASY, total_turns=50)

        with patch("src.Stats.output") as mock_output:
            mock_db_tracker.display_summary()

            printed_lines = [call.args[0] for call in mock_output.call_args_list]
            easy_summary_line = next((line for line in printed_lines if "easy" in line.lower()), None)

            assert easy_summary_line is not None
            assert "66.6%" in easy_summary_line
            assert "2/1" in easy_summary_line
            assert "35.0" in easy_summary_line
            assert "50.0" in easy_summary_line
