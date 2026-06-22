# strings/EnglishStrings.py

STRINGS: dict[str, str] = {
    # Coordinate Inputs
    "COORD_ENTER": "Please enter in your coords: x y\n\t",
    "COORD_ENTER_GENERIC": "Enter starting coordinate (e.g., A5 or 0,4): ",
    "DIR_ENTER": "Please enter in your directionality: h -> horizontal or v -> vertical\n\t",
    "DIR_INVALID": "{bold}{light_red}Invalid orientation choice!{end} Please type 'h' for horizontal or 'v' for vertical.",
    "START_LOCATION": "Please enter in the starting location of the {blue}{ship_name}{end}: x y\n\t",
    "TRY_AGAIN": "\t{yellow}Location is already selected.{end}",
    # Placement Logic
    "PLACE": "Placing {green}{ship_name}{end}...",
    "FAILED_PLACE": "{bold}{light_red}Failed to place{end} {ship_name} at ({x}, {y}) with directionality '{direction}' (Invalid Location).",
    "OUTSIDE_BOARD": "{red}({x}, {y}) is outside the board boundaries!{end}",
    "MANGLED_PLACE": "{bold}{red}Input Error:{end} Failed to place {ship_name} because the format was mangled.",
    "WRONG_INPUT": "Input must be in the form of {cyan}<int> <int>{end} -> {faint}{error_details}{end}",
    "EXAMPLE_1": "{dark_gray}\nExample:\n\t1 3\n\tA1\n\t1:3{end}",
    "EXAMPLE_2": "{dark_gray}\nExample:\n\th | v{end}",
    # Turn Execution
    "PRE_SHOT": "Preparing to take a shot at {yellow}{target}{end}",
    "SHOT_AT": "Shot at {light_white}({x},{y}){end} resulted in a {bold}{cyan}{result}{end}!",
    "INVALID_COORD": "{light_red}Coordinates are not valid, please attempt again.{end}",
    "CURRENT_TURN": "Current Turn: {bold}{yellow}{current_player}{end} ➔ Target: {green}{target_player}{end}",
    "STRUCK_AGAIN": "{bold}{light_red}Warning:{end} Location has {italic}already been struck once{end} before. Try again.",
    "AI_SHOT_TAKEN": "{bold}{light_purple}AI{end} fired tactical payload at {light_white}({x}, {y}){end}",
    "SUNK_SHIP": "{bold}{purple}💥 Sunk! {ship_name}{end} has been completely destroyed!",
    "OVERLAP": "{bold}{light_red}Overlap Detected!{end} Position ({x}, {y}) is already occupied by {bold}{yellow}{occupant}{end}",
    # Game State Ending
    "WON_GAME": "\n{blink}{bold}{light_green}🏆 {player_name} HAS WON THE GAME! 🏆{end}\n",
    # UI Display Headers
    "BOARD_HEADER_PLAYER": "╔"
    + "═" * 65
    + "╗\n║ {bold}{green}Player - {player_id} Friendly Fleet Map{end} ║\n╚"
    + "═" * 65
    + "╝",
    "BOARD_HEADER_TARGET": "╔"
    + "═" * 65
    + "╗\n║ {bold}{yellow}Player - {player_id} Target Radar Grid{end} ║\n╚"
    + "═" * 65
    + "╝",
    # Statistics Subsystem Reporting
    "STATS_FILLER": "{dark_gray}" + "=" * 80 + "{end}",
    "STATS_HEADER_TITLE": f"{{bold}}{{light_cyan}}{'BATTLESHIP LIFETIME PERFORMANCE STATS':^55}{{end}}",
    "STATS_HEADER_SUB": (
        f"{{underline}}{'Difficulty':<12} | {'Games':<5} | {'Wins':<4} | "
        f"{'Losses':<6} | {'Win %':<6} | {'Avg Turn Win':<12} | {'Shot Accuracy':<13}{{end}}"
    ),
    "STATS_OUTPUT": "{a:<12} | {b:<5} | {c:<4} | {d:<6} | {e:<6} | {f:<12} | {g:<13}",
}
