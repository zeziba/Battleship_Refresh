from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, Tuple, Type, Optional, Any
from enum import Enum, auto

import customtkinter as ctk
from dataclasses import dataclass

from . import config

if TYPE_CHECKING:
    from .Game import Game
    from .Board import Board


@dataclass
class UIConfig:
    # --- Window Settings ---
    window_title: str = "Battleship Command Center"
    window_width: int = 900
    window_width_resizable: bool = False
    window_height: int = 600
    window_height_resizable: bool = False
    appearance_mode: str = "Dark"  # "Dark", "Light", or "System"
    color_theme: str = "blue"

    # --- Typography ---
    font_title: tuple = ("Roboto", 48, "bold")
    font_header: tuple = ("Roboto", 24, "bold")
    font_board_title: tuple = ("Roboto", 18)
    font_body: tuple = ("Roboto", 16)
    font_stats: tuple = ("Consolas", 14)

    # --- Grid & Tile Dimensions ---
    tile_size: int = 35
    tile_corner_radius: int = 4
    board_padx: int = 30
    board_pady: int = 10

    # --- Tactical Radar Colors (Hex Codes) ---
    color_ocean: str = "#1f538d"  # Default blue water
    color_hover: str = "#14375e"  # Darker blue for mouse hover
    color_disabled: str = "#2a2d2e"  # Grayed out for un-clickable tiles

    # --- Combat Status Colors ---
    color_hit: str = "#8B0000"  # Crimson Red
    color_miss: str = "#A9A9A9"  # Dark Gray / White
    color_ship: str = "#228B22"  # Forest Green (Friendly radar)
    color_sunk: str = "#000000"  # Black (Destroyed vessel)

    color_danger_btn: str = "#8B0000"  # Red for Exit/Abort buttons
    color_danger_hover: str = "#5C0000"

    color_toast_bg: str = "#2b2b2b"
    color_toast_border: str = "#3f3f3f"


def show_toast(parent: ctk.CTkFrame, message: str, duration: int = 2500, anchor: str = "sw"):
    toast = ctk.CTkFrame(
        parent,
        fg_color=UIConfig.color_toast_bg,
        corner_radius=8,
        border_width=1,
        border_color=UIConfig.color_toast_border,
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
        title: ctk.CTkLabel = ctk.CTkLabel(self, text="Battleship", font=self.ui_cfg.font_title)
        title.pack(pady=(50, 40))

        # Action Buttons
        btns: list[ctk.CTkButton] = [
            ctk.CTkButton(
                self,
                text="Start Game",
                width=200,
                height=40,
                font=self.ui_cfg.font_body,
                command=self.app_controller.show_game,
            ),
            ctk.CTkButton(
                self,
                text="Options",
                width=200,
                height=40,
                font=self.ui_cfg.font_body,
                command=self.app_controller.show_options,
            ),
            ctk.CTkButton(
                self,
                text="View Statistics",
                width=200,
                height=40,
                font=self.ui_cfg.font_body,
                command=self.app_controller.show_stats,
            ),
            ctk.CTkButton(
                self,
                text="Exit Game",
                width=200,
                height=40,
                font=self.ui_cfg.font_body,
                command=self.app_controller.quit,
                fg_color=self.ui_cfg.color_danger_btn,
                hover_color=self.ui_cfg.color_danger_hover,
            ),
        ]
        for btn in btns:
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
            fg_color=self.ui_cfg.color_danger_btn,
            hover_color=self.ui_cfg.color_danger_hover,
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

        board_frame = ctk.CTkFrame(parent)
        col_position = 0 if side.lower() == "left" else 1
        board_frame.grid(row=0, column=col_position, pady=(10, 5), padx=20)

        lbl = ctk.CTkLabel(board_frame, text=title, font=self.ui_cfg.font_board_title)
        lbl.grid(row=0, column=0, columnspan=config.board_width, pady=(10, 5))

        default_color: str = self.ui_cfg.color_ocean if not interactive else self.ui_cfg.color_disabled
        hover_color: str = self.ui_cfg.color_hover if not interactive else self.ui_cfg.color_ocean

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
                btn.grid(row=y + 1, column=x, padx=2, pady=2)
                button_dict[(x, y)] = btn

    def toggle_orientation(self):
        if self.current_state != GameUIState.PLACEMENT:
            return

        self.c_ship_orientation = "V" if self.c_ship_orientation == "H" else "H"
        self.btn_orientation.configure(text=f"Orientation: {self.c_ship_orientation} (Press R to flip)")

    def handle_placement_click(self, x: int, y: int, button_dict: dict[tuple[int, int], ctk.CTkButton]):
        if not self.status_label:
            return
        # self.status_label.configure(text=f"Clicked ({x}, {y})", fg_color="transparent")
        show_toast(self, f"Clicked ({x}, {y})")

        btn = button_dict[(x, y)]

        fg_color = btn.cget("fg_color")
        hover_color = btn.cget("hover_color")

        btn.configure(
            fg_color=self.ui_cfg.color_ocean if fg_color == self.ui_cfg.color_disabled else self.ui_cfg.color_disabled,
            hover_color=(
                self.ui_cfg.color_hover
                if hover_color == self.ui_cfg.color_danger_hover
                else self.ui_cfg.color_danger_hover
            ),
        )

    def handle_attacker_click(self, x: int, y: int, button_dict: dict[tuple[int, int], ctk.CTkButton]):
        pass

    def handle_defender_click(self, x: int, y: int, button_dict: dict[tuple[int, int], ctk.CTkButton]):
        pass


class StatsFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, app_controller: BattleShipApp):
        super().__init__(master)
        self.app_controller = app_controller
        self.ui_cfg = app_controller.ui_cfg

        title: ctk.CTkLabel = ctk.CTkLabel(self, text="Game Statistics", font=self.ui_cfg.font_board_title)
        title.pack(pady=(20, 20))

        self.stats_textbox: ctk.CTkTextbox = ctk.CTkTextbox(self, width=600, height=300, font=self.ui_cfg.font_stats)
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
        self.resizable(width=self.ui_cfg.window_width_resizable, height=self.ui_cfg.window_height_resizable)

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
