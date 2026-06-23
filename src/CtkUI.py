from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, Sequence, Tuple, Type, Optional, Literal
from enum import Enum, auto

import customtkinter as ctk
from dataclasses import dataclass, field

from . import config
from .Ship import Direction
from .Player import Difficulty

if TYPE_CHECKING:
    from .Game import Game
    from .Board import Board
    from .Player import Player
    from .name_generator import NameGenerator
    from .Stats import GameStatTracker

FontConfig = Tuple[str, int, str] | Tuple[str, int]


@dataclass
class FontSettings:
    title: FontConfig = ("Roboto", 48, "bold")
    header: FontConfig = ("Roboto", 24, "bold")
    board_title: FontConfig = ("Roboto", 18)
    body: FontConfig = ("Roboto", 16)
    stats: FontConfig = ("Consolas", 12)


@dataclass
class Colors:
    # --- TUI Palette (Text & Accents) ---
    accent: str = "#00FFCC"  # Neon Cyan for active elements/selections
    text_main: str = "#FFFFFF"  # Crisp white for high-readability text
    text_muted: str = "#8A95A5"  # Muted slate for secondary labels

    # --- Tactical Radar Colors (Hex Codes) ---
    ocean: str = "#1f538d"  # Default blue water
    grid_lines: str = "#142c4b"  # Subtle dark blue for grid borders
    hover: str = "#14375e"  # Darker blue for mouse hover
    disabled: str = "#2a2d2e"  # Grayed out for un-clickable tiles

    # --- Combat Status Colors ---
    hit: str = "#8B0000"  # Crimson Red
    miss: str = "#A9A9A9"  # Dark Gray / White
    ship: str = "#228B22"  # Forest Green (Friendly radar)
    sunk: str = "#000000"  # Black (Destroyed vessel)

    # --- Interactve Elements ---
    success: str = "#00FF66"
    danger_btn: str = "#8B0000"  # Red for Exit/Abort buttons
    danger_hover: str = "#5C0000"

    # --- Notification / Toast ---
    toast_bg: str = "#2b2b2b"
    toast_border: str = "#3f3f3f"

    # Text Status Colors
    adaptive_text: tuple[str, str] = ("#1A1A1A", "#F0F0F0")
    toast_info: tuple[str, str] = ("#1C3D5A", "#A0C4DF")  # Deep blue vs Soft tactical blue
    toast_success: tuple[str, str] = ("#1E4620", "#A2E8A2")  # Forest green vs Matrix green
    toast_warning: tuple[str, str] = ("#7B5C00", "#FEEBC8")  # Amber brown vs Soft warning gold


@dataclass
class UIConfig:
    # --- Window Settings ---
    window_title: str = "Battleship Command Center"
    window_width: int = 900
    window_height: int = 600
    window_resizable: Tuple[bool, bool] = (False, False)
    appearance_mode: Literal["Dark", "Light", "System"] = "Dark"
    color_theme: str = "blue"

    # --- Typography ---
    fonts: FontSettings = field(default_factory=FontSettings)

    # --- Grid & Tile Dimensions ---
    tile_size: int = 35
    tile_corner_radius: int = 8
    board_padx: int = 30
    board_pady: int = 10

    colors: Colors = field(default_factory=Colors)
    transparent: str = "transparent"


def show_toast(parent: ctk.CTkFrame, message: str, duration: int = 2500, anchor: str = "sw"):
    toast = ctk.CTkFrame(
        parent, fg_color=Colors.toast_bg, corner_radius=8, border_width=1, border_color=Colors.toast_border
    )

    parent.update_idletasks()
    max_allowed_width = int(parent.winfo_width() * 0.30)

    label = ctk.CTkLabel(
        toast, text=message, text_color=Colors.adaptive_text, wraplength=max_allowed_width - 20, justify="left"
    )
    label.pack(padx=12, pady=8, expand=True, fill="both")

    toast.place(relx=0.02, rely=0.98, relwidth=0.30, relheight=0.10, anchor=anchor)
    toast.after(duration, toast.destroy)


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, app_controller: BattleShipApp):
        super().__init__(master, fg_color="transparent")
        self.app_controller = app_controller
        self.ui_cfg = app_controller.ui_cfg

        # Title
        title: ctk.CTkLabel = ctk.CTkLabel(self, text="Battleship", font=self.ui_cfg.fonts.title)
        title.pack(pady=(50, 40))

        self.buttons = self._create_menu_buttons()
        self._layout_buttons()

    def _create_menu_buttons(self) -> list[ctk.CTkButton]:
        default_btn_config = {"master": self, "width": 200, "height": 40, "font": self.ui_cfg.fonts.body}

        menu_items = [
            ("Start Game", self.app_controller.show_game, {}),
            ("Options", self.app_controller.show_options, {}),
            ("View Statistics", self.app_controller.show_stats, {}),
            (
                "Exit Game",
                self.app_controller.quit,
                {
                    "fg_color": getattr(self.ui_cfg.colors, "danger_btn"),
                    "hover_color": getattr(self.ui_cfg.colors, "danger_hover"),
                },
            ),
        ]

        return [
            ctk.CTkButton(**default_btn_config, text=text, command=cmd, **extra_kwargs)
            for text, cmd, extra_kwargs in menu_items
        ]

    def _layout_buttons(self):
        for btn in self.buttons:
            btn.pack(pady=10)


class GameUIState(Enum):
    PLACEMENT = auto()
    ATTACKER = auto()
    DEFENDER = auto()
    GAME_OVER = auto()


class GameFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, app_controller: BattleShipApp):
        super().__init__(master, fg_color="transparent")
        self.app_controller = app_controller
        self.ui_cfg = app_controller.ui_cfg
        self.players = {"attacker": 0, "defender": 0}

        # State Machine
        self.current_state: GameUIState = GameUIState.PLACEMENT

        # Ship placement data
        self.ships_to_place: dict[str, int] = config.fleet_composition
        self.c_ship_orientation: str = "H"  # | "V"
        self.c_ship_index: int = 0

        self.player_turn = 0
        self.current_player = 0

        self._init_layout()
        self.update_state_view()

    def _init_layout(self):
        # Status
        self.status_label: ctk.CTkLabel = ctk.CTkLabel(self, text="Game")
        self.status_label.pack(pady=10)

        # Controls
        self.control_container: ctk.CTkFrame = ctk.CTkFrame(self)
        self.control_container.pack(pady=5, fill="x")

        self.btn_orientation: ctk.CTkButton = ctk.CTkButton(
            self.control_container,
            text=f"Orientation: {self.c_ship_orientation} (Press R to flip)",
            command=self.toggle_orientation,
        )
        self.btn_orientation.pack(padx=10, side="left")

        self.btn_start_game: ctk.CTkButton = ctk.CTkButton(
            self.control_container,
            text="Start Game",
            command=self._start_game,
        )
        self.btn_start_game.pack(padx=10, side="left")

        btn_back: ctk.CTkButton = ctk.CTkButton(
            self.control_container,
            text="Abort Game",
            fg_color=self.ui_cfg.colors.danger_btn,
            hover_color=self.ui_cfg.colors.danger_hover,
            command=self.app_controller.show_menu,
        )
        btn_back.pack(pady=20, side="right")

        # Board
        self.board_frame: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Board Buttons
        self.p1_buttons: dict[tuple[int, int], ctk.CTkButton] = {}
        self.p2_buttons: dict[tuple[int, int], ctk.CTkButton] = {}

        self._build_board(
            self.board_frame,
            "Attacker",
            self.p1_buttons,
            side="left",
            interactive=True,
            command=self.handle_placement_click,
        )

        self.master.bind("<r>", lambda event: self.toggle_orientation)
        self.master.bind("<R>", lambda event: self.toggle_orientation)

    def change_state(self, next: GameUIState):
        self.current_state = next

    def get_tile_state(self, board: Board, x: int, y: int):
        tile = board.get(x, y)
        return tile

    def _update_p1_tile(self, p1: Player, x: int, y: int):
        btn = self.p1_buttons[(x, y)]
        tile_state = self.get_tile_state(p1.board, x, y)
        tile = p1.board.get(x, y)

        color_miss = self.ui_cfg.colors.miss
        color_hit = self.ui_cfg.colors.hit
        color_ocean = self.ui_cfg.colors.ocean
        color_sunk = self.ui_cfg.colors.sunk

        if isinstance(tile_state, bool):
            if tile_state:
                btn.configure(text="O", fg_color=color_miss)
            else:
                btn.configure(text="", fg_color=color_ocean)
            return

        if not tile.has:
            return

        if tile.has.hit:
            if tile.has.is_sunk:
                ship_initial = tile.has.name[0].upper()
                btn.configure(text=ship_initial, fg_color=color_sunk)
            else:
                btn.configure(text="X", fg_color=color_hit)
        else:
            btn.configure(text="", fg_color=color_ocean)

    def _update_p2_tile(self, p2: Player, x: int, y: int):
        btn = self.p2_buttons[(x, y)]

        if self.current_state == GameUIState.PLACEMENT:
            btn.configure(text="", fg_color=self.ui_cfg.colors.disabled, state="disabled")
            return

        color_miss = self.ui_cfg.colors.miss
        color_hit = self.ui_cfg.colors.hit
        color_ocean = self.ui_cfg.colors.ocean
        color_sunk = self.ui_cfg.colors.sunk

        btn.configure(state="normal")
        tile_state = self.get_tile_state(p2.board, x, y)
        tile = p2.board.get(x, y)

        if isinstance(tile_state, bool):
            if tile_state:
                btn.configure(text="O", fg_color=color_miss)
            else:
                btn.configure(text="", fg_color=color_ocean)
            return

        if not tile.has:
            return

        if tile.has.hit:
            if tile.has.is_sunk:
                ship_initial = tile.has.name[0].upper()
                btn.configure(text=ship_initial, fg_color=color_sunk)
            else:
                btn.configure(text="X", fg_color=color_hit)
        else:
            btn.configure(text="", fg_color=color_ocean)

    def update_state_view(self):
        ship_name = ""
        if self.current_state == GameUIState.PLACEMENT and self.ships_to_place:
            ship_name = list(self.ships_to_place.keys())[self.c_ship_index]

        state_config = {
            GameUIState.PLACEMENT: (f"Deployment Phase: Placing {ship_name}", "normal", "transparent"),
            GameUIState.ATTACKER: ("Attack Phase", "disabled", "transparent"),
            GameUIState.DEFENDER: ("Defense Phase", "disabled", "#D1A119"),
            GameUIState.GAME_OVER: ("Game Over", "disabled", "transparent"),
        }

        text, btn_state, fg_color = state_config.get(self.current_state, ("", "disabled", "transparent"))

        self.status_label.configure(text=text, fg_color=fg_color)
        self.btn_orientation.configure(state=btn_state)

    def _start_game(self):
        # Remove old game
        if hasattr(self.app_controller, "game") and self.app_controller.game:
            del self.app_controller.game

        self.btn_orientation.configure(state="enabled")
        self.btn_start_game.configure(state="disabled")
        self.update_state_view()

        if not (
            self.app_controller._game_engine
            and self.app_controller.player_gen
            and self.app_controller.board_gen
            and self.app_controller.name_gen
        ):
            return

        self.player_turn = 0
        self.current_player = 0

        # config = self.app_controller.config

        create_player = self.app_controller.player_gen
        names = self.app_controller.name_gen
        if not (create_player and names):
            return False

        player_difficulty: Sequence[Difficulty | None] = list(self.app_controller._player_difficulty.values())
        p1_difficulty = player_difficulty[0]
        p2_difficulty = player_difficulty[1]
        if not p1_difficulty or not p2_difficulty:
            return

        board = self.app_controller.board_gen
        game = self.app_controller._game_engine

        p1_board = board(config.board_width, config.board_height)
        p1_name = f"(1) Admiral {names.create_random_name()}"
        p1 = create_player(p1_name, p1_difficulty, p1_board, config.fleet_composition)
        p1.generate_fleet(config.fleet_composition)

        # Setup player 2
        p2_board = board(config.board_width, config.board_height)
        p2_name = f"(2) Admiral {names.create_random_name()}"
        p2 = create_player(p2_name, p2_difficulty, p2_board, config.fleet_composition)
        p2.generate_fleet(config.fleet_composition)

        player_dict = {p1_name: p1, p2_name: p2}

        self.app_controller.game = game(players_dict=player_dict)

    def _build_board(
        self,
        parent: ctk.CTkFrame,
        title: str,
        button_dict: Dict[Tuple[int, int], ctk.CTkButton],
        side: str,
        interactive: bool,
        command: Callable[[int, int, Dict[tuple[int, int], ctk.CTkButton]], None] | None = None,
    ):
        # Remove old buttons
        for btn_set in button_dict.values():
            btn_set.destroy()
        button_dict.clear()

        _cmd = command or (lambda x, y, b_dict: self.handle_attacker_click(x, y, b_dict))

        board_frame = ctk.CTkFrame(parent, fg_color=self.ui_cfg.colors.grid_lines)
        col_position = 0 if side.lower() == "left" else 1
        board_frame.grid(row=0, column=col_position, pady=(10, 5), padx=20)

        lbl = ctk.CTkLabel(board_frame, text=title, font=self.ui_cfg.fonts.board_title)
        lbl.grid(row=0, column=0, columnspan=config.board_width, pady=(10, 5))

        default_color: str = self.ui_cfg.colors.ocean if not interactive else self.ui_cfg.colors.disabled
        hover_color: str = self.ui_cfg.colors.hover if not interactive else self.ui_cfg.colors.ocean

        for x in range(config.board_width):
            for y in range(config.board_height):
                cmd = (lambda cx=x, cy=y: _cmd(cx, cy, button_dict)) if interactive else None

                btn: ctk.CTkButton = ctk.CTkButton(
                    board_frame,
                    text="",
                    width=self.ui_cfg.tile_size,
                    height=self.ui_cfg.tile_size,
                    corner_radius=self.ui_cfg.tile_corner_radius,
                    fg_color=default_color,
                    hover_color=hover_color,
                    command=cmd,
                )
                btn.grid(row=y + 1, column=x, padx=1, pady=1)
                button_dict[(x, y)] = btn

    def toggle_orientation(self):
        if self.current_state != GameUIState.PLACEMENT:
            return

        self.c_ship_orientation = "V" if self.c_ship_orientation == "H" else "H"
        self.btn_orientation.configure(text=f"Orientation: {self.c_ship_orientation} (Press R to flip)")

    def refresh_board_dsiplay(self):
        p1: Player | None = self.app_controller.players.get("Player One")
        p2: Player | None = self.app_controller.players.get("Player Two")

        if not p1 or not p2:
            # Log here
            return

        width = config.board_width
        height = config.board_height

        for x in range(width):
            for y in range(height):
                if (x, y) in self.p1_buttons:
                    self._update_p1_tile(p1, x, y)
                if (x, y) in self.p2_buttons:
                    self._update_p1_tile(p2, x, y)

    def handle_placement_click(self, x: int, y: int, button_dict: dict[tuple[int, int], ctk.CTkButton]):
        if not self.app_controller.players:
            return
        if not self.current_state == GameUIState.PLACEMENT:
            return
        if not self.status_label:
            return

        btn = button_dict.get((x, y))
        if not btn:
            return

        show_toast(self, f"Clicked ({x}, {y})")
        c_player = list(self.app_controller.players.keys())[0]
        ori = Direction.HORIZONTAL if self.c_ship_orientation == "H" else Direction.VERTICAL
        player = self.app_controller.players[c_player]
        success, message = player.place_ship_gui(x, y, ori)

        if success:
            self.refresh_board_dsiplay()
            next_ship = player.next_ship_to_place
            if next_ship is None:
                self.current_state = GameUIState.ATTACKER
                show_toast(self, f"All Ships Placed\n{message}")
            else:
                self.status_label.configure(text=f"Place your next ship: {next_ship}")
        else:
            show_toast(self, f"{message}")

        is_disabled = btn.cget("fg_color") == self.ui_cfg.colors.disabled

        if is_disabled:
            fg_color = self.ui_cfg.colors.ocean
            hover_color = self.ui_cfg.colors.hover
        else:
            fg_color = self.ui_cfg.colors.disabled
            hover_color = self.ui_cfg.colors.danger_hover

        btn.configure(fg_color=fg_color, hover_color=hover_color)

    def handle_attacker_click(self, x: int, y: int, button_dict: dict[tuple[int, int], ctk.CTkButton]):
        pass

    def handle_defender_click(self, x: int, y: int, button_dict: dict[tuple[int, int], ctk.CTkButton]):
        pass


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, app_controller: BattleShipApp):
        super().__init__(master)
        self.app_controller = app_controller
        self.ui_cfg = app_controller.ui_cfg

        title: ctk.CTkLabel = ctk.CTkLabel(self, text="Game Statistics", font=self.ui_cfg.fonts.board_title)
        title.pack(pady=(20, 20))

        self.stats_textbox: ctk.CTkTextbox = ctk.CTkTextbox(self, width=600, height=300, font=self.ui_cfg.fonts.stats)
        self.stats_textbox.pack(pady=10)
        # Add data here
        self.stats_textbox.insert("0.0", "Loading Database records...")
        self.stats_textbox.configure(state="disabled")

        btn_back: ctk.CTkButton = ctk.CTkButton(self, text="Back to Main Menu", command=app_controller.show_menu)
        btn_back.pack(pady=20)

    def update_stats(self):
        self.stats_textbox.configure(state="normal")

        self.stats_textbox.delete("1.0", "end")

        if self.app_controller.telemetry_output:
            data = self.app_controller.telemetry_output()
        else:
            data = "Error loading stats"

        self.stats_textbox.insert("1.0", f"{data}")

        self.stats_textbox.configure(state="disabled")


class OptionFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, app_controller: BattleShipApp):
        super().__init__(master)
        self.app_controller = app_controller

        # Title Label
        title: ctk.CTkLabel = ctk.CTkLabel(self, text="Options", font=self.app_controller.ui_cfg.fonts.title)
        title.pack(pady=20)

        # Button Container
        self.btn_container = ctk.CTkFrame(self)
        self.btn_container.pack(pady=10, fill="x", padx=40)

        self.btn_difficulty = {}
        btn_config = {
            "Player One": (
                self.app_controller.ui_cfg.transparent,
                self.app_controller.ui_cfg.colors.hover,
            ),
            "Player Two": (
                self.app_controller.ui_cfg.transparent,
                self.app_controller.ui_cfg.colors.hover,
            ),
        }

        for key, items in btn_config.items():
            fg_color, hover_color = items

            if key not in self.app_controller._player_difficulty:
                if self.app_controller.accepted_difficulties:
                    self.app_controller._player_difficulty[key] = self.app_controller.accepted_difficulties[0]

            current_diff = self.app_controller._player_difficulty[key]
            diff_text = getattr(current_diff, "name", None)

            self.btn_difficulty[key] = ctk.CTkButton(
                self.btn_container,
                text=f"{key}: {diff_text}",
                fg_color=fg_color,
                hover_color=hover_color,
                command=lambda k=key: self._update_difficulty_btn(k),
            )
            self.btn_difficulty[key].pack(pady=10, fill="x", padx=20)

        # Back Button
        btn_back: ctk.CTkButton = ctk.CTkButton(self, text="Back to Main Menu", command=app_controller.show_menu)
        btn_back.pack(pady=30)

    def _update_difficulty_btn(self, name: str):
        available_difficulties = self.app_controller.accepted_difficulties
        if not available_difficulties:
            return

        current_difficulty = self.app_controller._player_difficulty[name]
        if not current_difficulty:
            return

        try:
            current_index = available_difficulties.index(current_difficulty)
            next_index = (current_index + 1) % len(available_difficulties)
        except ValueError:
            next_index = 0

        new_difficulty = available_difficulties[next_index]
        self.app_controller._player_difficulty[name] = new_difficulty

        difficulty_text = getattr(new_difficulty, "name", None)
        self.btn_difficulty[name].configure(text=f"{name}: {difficulty_text}")


class BattleShipApp(ctk.CTk):
    def __init__(
        self,
        game_engine: Optional[Type[Game]] = None,
        player_gen: Optional[Callable[[str, Difficulty, Board, dict[str, int]], Player]] = None,
        board_gen: Optional[Callable[[int, int], Board]] = None,
        name_gen: Optional[NameGenerator] = None,
        accepted_difficulties: Optional[list[Difficulty]] = None,
        telemetry: Optional[GameStatTracker] = None,
        telemetry_output: Optional[Callable[[], str]] = None,
    ):
        super().__init__()
        self.ui_cfg = UIConfig()
        self.game: Optional[Game] = None

        # Init setup from configuration
        ctk.set_appearance_mode(self.ui_cfg.appearance_mode)
        ctk.set_default_color_theme(self.ui_cfg.color_theme)
        self.title(self.ui_cfg.window_title)
        self.geometry(f"{self.ui_cfg.window_width}x{self.ui_cfg.window_height}")
        self.resizable(width=self.ui_cfg.window_resizable[0], height=self.ui_cfg.window_resizable[1])

        # Init Game
        self._game_engine = game_engine
        self.player_gen = player_gen
        self.board_gen = board_gen
        self.name_gen = name_gen
        self.accepted_difficulties = accepted_difficulties
        self._telemetry = telemetry
        self.telemetry_output = telemetry_output

        self.players: dict[str, Player] = {}

        self._player_difficulty: dict[str, Difficulty] = {"Player One": Difficulty.EASY, "Player Two": Difficulty.HARD}

        # Master Frame Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.current_frame: Optional[ctk.CTkFrame] = None
        self.show_menu()

    def _switch_frame(self, frame_class: Type[ctk.CTkFrame]):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(master=self.container, app_controller=self)
        self.current_frame.pack(fill="both", expand=True)

    def show_menu(self):
        self._switch_frame(MainMenuFrame)

    def show_game(self):
        self._switch_frame(GameFrame)

    def show_stats(self):
        self._switch_frame(StatsFrame)
        if isinstance(self.current_frame, StatsFrame):
            self.current_frame.update_stats()

    def show_options(self):
        self._switch_frame(OptionFrame)


if __name__ == "__main__":
    app = BattleShipApp()
    app.mainloop()
