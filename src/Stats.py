import sqlite3
from dataclasses import dataclass, field
from math import trunc
from .Player import Difficulty
from .UI import output
from .GameRules import Output

DB_FILE = "battleship_stats.db"


@dataclass
class DifficultyStats:
    wins: int = 0
    losses: int = 0
    total_turns_won: int = 0
    total_turns_lost: int = 0

    @property
    def avg_turns_to_win(self) -> float:
        return self.total_turns_won / self.wins if self.wins > 0 else 0.0

    @property
    def avg_turns_to_lose(self) -> float:
        return self.total_turns_lost / self.losses if self.losses > 0 else 0.0

    @property
    def win_rate(self) -> float:
        total_games = self.wins + self.losses
        return trunc((self.wins / total_games) * 1e3) / 1e1 if total_games > 0 else 0.0


@dataclass
class GameStatTracker:
    by_difficulty: dict[str, DifficultyStats] = field(
        default_factory=lambda: {diff.value: DifficultyStats() for diff in Difficulty}
    )

    def __post_init__(self):
        self._init_db()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_history (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           winner_difficulty TEXT NOT NULL,
                           loser_difficulty TEXT NOT NULL,
                           total_turns INTEGER NOT NULL,
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """)

    def _get_connection(self):
        return sqlite3.connect(DB_FILE)

    def record_game(self, winner_difficulty: Difficulty, loser_difficulty: Difficulty, total_turns: int):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO game_history (winner_difficulty, loser_difficulty, total_turns)
                VALUES (?, ?, ?)
                """,
                (winner_difficulty.value, loser_difficulty.value, total_turns),
            )
            conn.commit()

    def display_summary(self):
        output(Output.STATS_FILLER)
        output(Output.STATS_HEADER_TITLE)
        output(Output.STATS_FILLER)
        output(Output.STATS_HEADER_SUB)
        output(Output.STATS_FILLER)

        for difficulty in Difficulty:
            diff = difficulty.value
            with self._get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT COUNT(*), AVG(total_turns) FROM game_history WHERE winner_difficulty = ?", (diff,)
                )
                wins, avg_w_raw = cursor.fetchone()
                wins = wins or 0

                cursor.execute(
                    "SELECT COUNT(*), AVG(total_turns) FROM game_history WHERE loser_difficulty = ?", (diff,)
                )
                losses, avg_l_raw = cursor.fetchone()
                losses = losses or 0

            total_games = wins + losses
            if total_games == 0:
                continue

            win_rate = trunc((wins / total_games) * 1e3) / 1e1 if total_games > 0 else 0

            win_rate_str = f"{win_rate:.1f}%"
            wl_str = f"{wins}/{losses}"
            avg_w = f"{avg_w_raw:.1f}" if wins > 0 else "N/A"
            avg_l = f"{avg_l_raw:.1f}" if losses > 0 else "N/A"

            output(
                Output.STATS_OUTPUT.format(
                    f"{diff.upper():<12}", f"{win_rate_str:<10}", f"{wl_str:<6}", f"{avg_w:<10}", f"{avg_l}"
                )
            )
        output(Output.STATS_FILLER)
