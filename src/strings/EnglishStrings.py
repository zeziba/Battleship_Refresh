# strings/EnglishStrings.py

STRINGS: dict[str, str] = {
    # Coordinate Inputs
    "COORD_ENTER": "Please enter in your coords: x y\n\t",
    "COORD_ENTER_GENERIC": "Enter starting coordinate (e.g., A5 or 0,4): ",
    "DIR_ENTER": "Please enter in your directionality: h -> horizontal or v -> vertical\n\t",
    "DIR_INVALID": "Invalid orientation choice! Please type 'h' for horizontal or 'v' for vertical.",
    "START_LOCATION": "Please enter in the starting location of the {ship}{ship_name}{end}: x y\n\t",
    "TRY_AGAIN": "\tLocation is already selected.",
    # Placement Logic
    "PLACE": "Placing {green}{ship_name}{end}",
    "FAILED_PLACE": "{bold}{red}Failed{end} to place {ship_name} at ({x}, {y}) with directionality {direction} as not a valid location.",
    "OUTSIDE_BOARD": "({x}, {y}) is outside the board!",
    "MANGLED_PLACE": "Failed to place {ship_name} as input was mangled",
    "WRONG_INPUT": "Input must be in the form of {cyan}<int> <int>{end} {error_details}",
    "EXAMPLE_1": "\nExample:\n\t1 3\n\tA1\n\t1:3",
    "EXAMPLE_2": "\nExample:\n<h|v>",
    # Turn Execution
    "PRE_SHOT": "Preparing to take a shot at {yellow}{target}{end}",
    "SHOT_AT": "Shot at {green}({x},{y}){end} was a {cyan}{result}{end}",
    "INVALID_COORD": "Coordinates are not valid, attempt again",
    "CURRENT_TURN": "Currently turn: {yellow}{current_player}{end} with player {green}{target_player}{end} being targeted",
    "STRUCK_AGAIN": "Location has {italic}{light_red}already been struck once{end} before try again.",
    "AI_SHOT_TAKEN": "{green}AI{end} fired at {white}({x}, {y}){end}",
    "SUNK_SHIP": "{purple}{ship_name}{end} has been sunk!",
    "OVERLAP": "{red}Overlap Detected!{end} Position ({x}, {y}) is already occupied by {occupant}",
    # Game State Ending
    "WON_GAME": "{blink}{bold}{green}{player_name}{end} has won the game!{end}",
    # UI Display Headers
    "BOARD_HEADER_PLAYER": "{green}Player - {player_id} Board{end}",
    "BOARD_HEADER_TARGET": "{yellow}Player - {player_id} Board{end}",
    # Statistics Subsystem Reporting
    "STATS_FILLER": "=" * 50,
    "STATS_HEADER_TITLE": f"{'BATTLESHIP LIFETIME PERFORMANCE STATS':^55}",
    "STATS_HEADER_SUB": (
        f"{'Difficulty':<12} | {'Games':<5} | {'Wins':<4} | "
        f"{'Losses':<6} | {'Win %':<6} | {'Avg Turn Win':<12} | {'Shot Accuracy':<13}"
    ),
    "STATS_OUTPUT": "{a} | {b} | {c} | {d} | {e} | {f} | {g}",
}
