import sqlite3
import hashlib
from dataclasses import dataclass, field
from math import trunc
from typing import Any, Optional
from .Player import Difficulty
from .UI import output
from .GameRules import Output

DB_FILE = "battleship_stats.db"


def generate_player_id(player_name: str) -> str:
    return hashlib.sha256(player_name.strip().encode("utf-8")).hexdigest()[:16]


def display_database_summary(db_path: str = DB_FILE):
    query = """
        WITH player_match_stats AS (
            -- Calculate individual match wins, losses, and game-ending turn totals
            SELECT 
                p.difficulty,
                COUNT(CASE WHEN g.winner_id = p.player_id THEN 1 END) AS wins,
                COUNT(CASE WHEN g.loser_id = p.player_id THEN 1 END) AS losses,
                SUM(CASE WHEN g.winner_id = p.player_id THEN g.total_turns ELSE 0 END) AS total_turns_won,
                SUM(CASE WHEN g.loser_id = p.player_id THEN g.total_turns ELSE 0 END) AS total_turns_lost
            FROM players p
            LEFT JOIN games g ON p.player_id = g.winner_id OR p.player_id = g.loser_id
            GROUP BY p.difficulty
        ),
        player_shot_accuracy AS (
            -- Extract global shot metric accuracy details cleanly mapped to difficulty groups
            SELECT 
                p.difficulty,
                COUNT(s.turn_sequence) AS total_shots,
                COUNT(CASE WHEN s.shot_outcome = 1 THEN 1 END) AS total_hits
            FROM players p
            JOIN shot_logs s ON p.player_id = s.player_id
            GROUP BY p.difficulty
        )
        SELECT 
            m.difficulty,
            m.wins,
            m.losses,
            (m.wins + m.losses) AS total_games,
            -- Multiply by 100.0 first to escape Integer Division truncation bugs
            CASE 
                WHEN (m.wins + m.losses) > 0 THEN (m.wins * 100.0) / (m.wins + m.losses)
                ELSE 0.0 
            END AS win_rate,
            CASE 
                WHEN m.wins > 0 THEN m.total_turns_won / m.wins 
                ELSE 0 
            END AS avg_turns_to_win,
            CASE 
                WHEN a.total_shots > 0 THEN (a.total_hits * 100.0) / a.total_shots
                ELSE 0.0 
            END AS shot_accuracy
        FROM player_match_stats m
        LEFT JOIN player_shot_accuracy a ON m.difficulty = a.difficulty;
    """

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
    except sqlite3.OperationalError as err:
        output(f"[INFO] Analytics database is empty or uninitialized.")
        return

    active_rows = [r for r in rows if (r[1] and r[2]) > 0]
    if not active_rows:
        output(f"[INFO] No completed game tracking telemetry found.")
        return

    output(Output.STATS_FILLER)
    output(Output.STATS_HEADER_TITLE)
    output(Output.STATS_FILLER)
    output(Output.STATS_HEADER_SUB)
    output(Output.STATS_FILLER)

    for row in active_rows:
        diff, wins, losses, total_games, win_rate, avg_turns, accuracy = row

        output(
            Output.STATS_OUTPUT.format(
                f"{diff:<12}",
                f"{total_games:<5}",
                f"{wins:<5}",
                f"{losses:<6}",
                f"{win_rate:<5.1f}",
                f"{avg_turns:>12}",
                f"{accuracy:>12.1f}%",
            )
        )
    output(Output.STATS_FILLER)


@dataclass
class ShipPlacementData:
    name: str
    start_x: int
    start_y: int
    orientation: str
    size: int


@dataclass
class ChronologicalShot:
    player_id: str
    turn_sequence: int
    x: int
    y: int
    outcome: bool
    sunk_ship_name: Optional[str] = None


@dataclass
class MatchTelemetry:
    player_name: str
    difficulty: Difficulty
    player_id: str = field(init=False)
    initial_placements: list[ShipPlacementData] = field(default_factory=list)

    def __post_init__(self):
        self.player_id = generate_player_id(self.player_name)

    def record_placement(self, name: str, x: int, y: int, orientation: str, size: int):
        self.initial_placements.append(ShipPlacementData(name, x, y, orientation, size))


class GameStatTracker:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY, winner_id TEXT, loser_id TEXT, total_turns INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    player_id TEXT PRIMARY KEY, player_name TEXT UNIQUE, difficulty TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ship_placements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, game_id TEXT, player_id TEXT,
                    ship_name TEXT, start_x INTEGER, start_y INTEGER, orientation TEXT, size INTEGER,
                    FOREIGN KEY(game_id) REFERENCES games(game_id), FOREIGN KEY(player_id) REFERENCES players(player_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shot_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, game_id TEXT, player_id TEXT,
                    turn_sequence INTEGER, coord_x INTEGER, coord_y INTEGER, shot_outcome TEXT, sunk_ship_name TEXT,
                    FOREIGN KEY(game_id) REFERENCES games(game_id), FOREIGN KEY(player_id) REFERENCES players(player_id)
                )
            """)

    def _get_connection(self):
        return sqlite3.connect(DB_FILE)

    def register_match_entities(
        self, game_id: str, winner_tel: MatchTelemetry, loser_tel: MatchTelemetry, total_turns: int
    ):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            for tel in [winner_tel, loser_tel]:
                cursor.execute(
                    """
                    INSERT INTO players (player_id, player_name, difficulty) VALUES (?, ?, ?)
                    ON CONFLICT(player_id) DO UPDATE SET player_name=excluded.player_name, difficulty=excluded.difficulty
                """,
                    (tel.player_id, tel.player_name, tel.difficulty.value),
                )

                cursor.execute(
                    """INSERT INTO games (game_id, winner_id, loser_id, total_turns)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(game_id) DO UPDATE SET
                        winner_id=excluded.winner_id,
                        loser_id=excluded.loser_id,
                        total_turns=excluded.total_turns
                """,
                    (game_id, winner_tel.player_id, loser_tel.player_id, total_turns),
                )

                placement_rows = []
                for tel in [winner_tel, loser_tel]:
                    for p in tel.initial_placements:
                        placement_rows.append(
                            (game_id, tel.player_id, p.name, p.start_x, p.start_y, p.orientation, p.size)
                        )

                cursor.executemany(
                    """
                    INSERT OR IGNORE INTO ship_placements (game_id, player_id, ship_name, start_x, start_y, orientation, size)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    placement_rows,
                )
                conn.commit()

    def batch_write_shots(self, game_id: str, global_timeline: list[ChronologicalShot]):
        shot_rows = [
            (game_id, s.player_id, s.turn_sequence, s.x, s.y, s.outcome, s.sunk_ship_name) for s in global_timeline
        ]
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO shot_logs (game_id, player_id, turn_sequence, coord_x, coord_y, shot_outcome, sunk_ship_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                shot_rows,
            )
            conn.commit()
