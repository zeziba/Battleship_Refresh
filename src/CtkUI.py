from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, Tuple, Type, Optional, Literal
from enum import Enum, auto

import customtkinter as ctk
from dataclasses import dataclass, field

from . import config

if TYPE_CHECKING:
    from .Game import Game
    from .Board import Board

FontConfig = Tuple[str, int, str] | Tuple[str, int]


@dataclass
class FontSettings:
    title: FontConfig = ("Roboto", 48, "bold")
    header: FontConfig = ("Roboto", 24, "bold")
    board_title: FontConfig = ("Roboto", 18)
    body: FontConfig = ("Roboto", 16)
    stats: FontConfig = ("Consolas", 14)


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
    tile_corner_radius: int = 4
    board_padx: int = 30
    board_pady: int = 10

    colors: Colors = field(default_factory=Colors)


def show_toast(parent: ctk.CTkFrame, message: str, duration: int = 2500, anchor: str = "sw"):
    toast = ctk.CTkFrame(
        parent,
        fg_color=Colors.toast_bg,
        corner_radius=8,
        border_width=1,
        border_color=Colors.toast_border,
    )

    parent.update_idletasks()
    max_allowed_width = int(parent.winfo_width() * 0.30)

    label = ctk.CTkLabel(toast, text=message, text_color="white", wraplength=max_allowed_width - 20, justify="left")
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

    def handle_placement_click(self, x: int, y: int, button_dict: dict[tuple[int, int], ctk.CTkButton]):
        if not self.status_label:
            return

        show_toast(self, f"Clicked ({x}, {y})")

        btn = button_dict.get((x, y))
        if not btn:
            return

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


class OptionFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, app_controller: BattleShipApp):
        super().__init__(master)
        self.app_controller = app_controller

        title: ctk.CTkLabel = ctk.CTkLabel(self, text="Options")
        title.pack(pady=10)

        btn_back: ctk.CTkButton = ctk.CTkButton(self, text="Back to Main Menu", command=app_controller.show_menu)
        btn_back.pack(pady=20)


class BattleShipApp(ctk.CTk):
    def __init__(self, game_engine: Optional[Game] = None):
        super().__init__()
        self.ui_cfg = UIConfig()
        self.game: Optional[Game] = game_engine

        # Init setup from configuration
        ctk.set_appearance_mode(self.ui_cfg.appearance_mode)
        ctk.set_default_color_theme(self.ui_cfg.color_theme)
        self.title(self.ui_cfg.window_title)
        self.geometry(f"{self.ui_cfg.window_width}x{self.ui_cfg.window_height}")
        self.resizable(width=self.ui_cfg.window_resizable[0], height=self.ui_cfg.window_resizable[1])

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

    def show_options(self):
        self._switch_frame(OptionFrame)


if __name__ == "__main__":
    app = BattleShipApp()
    app.mainloop()
