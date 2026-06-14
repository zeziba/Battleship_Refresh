from dataclasses import dataclass, field
from math import trunc
from .Player import Difficulty
from .UI import output
from .GameRules import Output


@dataclass
class DifficultyStats:
    wins: int = 0
    losses: int = 0
    total_turns_won: int = 0
    total_turns_lost: int = 0

    @property
    def avg_turns_to_win(self) -> float:
        return self.total_turns_won/ self.wins if self.wins > 0 else 0.0
    
    @property
    def avg_turns_to_lose(self) -> float:
        return self.total_turns_lost / self.losses if self.losses > 0 else 0.0
    
    @property
    def win_rate(self) -> float:
        total_games = self.wins + self.losses
        return trunc((self.wins / total_games) * 1e3) / 1e1 if total_games > 0 else 0.0
    

@dataclass
class GameStatTracker:
    by_difficulty: dict[str, DifficultyStats] = field(default_factory=lambda: {diff.value: DifficultyStats() for diff in Difficulty})

    def  record_game(self, winner_difficult: Difficulty, loser_difficulty: Difficulty, total_turns: int):
        winner_stats = self.by_difficulty[winner_difficult.value]
        loser_stats = self.by_difficulty[loser_difficulty.value]

        winner_stats.wins += 1
        winner_stats.total_turns_won += total_turns

        loser_stats.losses += 1
        loser_stats.total_turns_lost += total_turns

    def display_summary(self):
        output(Output.STATS_FILLER)
        output(Output.STATS_HEADER_TITLE)
        output(Output.STATS_FILLER)
        output(Output.STATS_HEADER_SUB)
        output(Output.STATS_FILLER)

        for diff, stats in self.by_difficulty.items():
            total_games = stats.losses + stats.wins
            if total_games == 0:
                continue

            win_rate_str = f"{stats.win_rate:.1f}%"
            wl_str = f"{stats.wins}/{stats.losses}"
            avg_w = f"{stats.avg_turns_to_win:.1f}" if stats.wins > 0 else "N/A"
            avg_l = f"{stats.avg_turns_to_lose:.1f}" if stats.losses > 0 else "N/A"
        
            output(Output.STATS_OUTPUT.format(
                f"{diff.upper():<12}",
                f"{win_rate_str:<10}",
                f"{wl_str:<6}",
                f"{avg_w:<10}",
                f"{avg_l}"
            ))
        output(Output.STATS_FILLER)