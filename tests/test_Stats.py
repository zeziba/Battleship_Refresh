# tests/test_stats.py
from math import trunc
from src.Stats import GameStatTracker
from src.Player import Difficulty

class TestGameStatsTracker:
    def test_record_single_game(self):
        tracker = GameStatTracker()
        
        # Test recording a Medium win against Easy on turn 32
        tracker.record_game(Difficulty.MEDIUM, Difficulty.EASY, 32)
        
        med_stats = tracker.by_difficulty[Difficulty.MEDIUM.value]
        easy_stats = tracker.by_difficulty[Difficulty.EASY.value]
        
        assert med_stats.wins == 1
        assert med_stats.losses == 0
        assert med_stats.total_turns_won == 32
        assert med_stats.win_rate == 100.0
        assert med_stats.avg_turns_to_win == 32.0
        
        assert easy_stats.wins == 0
        assert easy_stats.losses == 1
        assert easy_stats.total_turns_lost == 32
        assert easy_stats.win_rate == 0.0
        assert easy_stats.avg_turns_to_lose == 32.0

    def test_averages_calculation(self):
        tracker = GameStatTracker()
        
        # Simulate 2 wins and 1 loss for MEDIUM
        tracker.record_game(Difficulty.MEDIUM, Difficulty.EASY, 20)
        tracker.record_game(Difficulty.MEDIUM, Difficulty.HUMAN, 30)
        tracker.record_game(Difficulty.HUMAN, Difficulty.MEDIUM, 40)
        
        med_stats = tracker.by_difficulty[Difficulty.MEDIUM.value]
        
        assert med_stats.wins == 2
        assert med_stats.losses == 1
        assert med_stats.win_rate == trunc((2 / 3) * 1e3) / 1e1
        assert med_stats.avg_turns_to_win == 25.0  # (20 + 30) / 2
        assert med_stats.avg_turns_to_lose == 40.0 # 40 / 1