# strings/EnglishStrings.py

STRINGS: dict[str, str] = {
    # Coordinate Inputs
    "COORD_ENTER": "Please enter in your coords: x y\n\t",
    "COORD_ENTER_GENERIC": "Enter starting coordinate (e.g., A5 or 0,4): ",
    "DIR_ENTER": "Please enter in your directionality: h -> horizontal or v -> vertical\n\t",
    "DIR_INVALID": "Invalid orientation choice! Please type 'h' for horizontal or 'v' for vertical.",
    "START_LOCATION": "Please enter in the starting location of the {ship_color}{ship_name}{end_color}: x y\n\t",
    "TRY_AGAIN": "\tLocation is already selected.",
    # Placement Logic
    "PLACE": "Placing {green_color}{ship_name}{end_color}",
    "FAILED_PLACE": "{red_color}Failed{end_color} to place {ship_name} at ({x}, {y}) with directionality {direction} as not a valid location.",
    "OUTSIDE_BOARD": "({x}, {y}) is outside the board!",
    "MANGLED_PLACE": "Failed to place {ship_name} as input was mangled",
    "WRONG_INPUT": "Input must be in the form of {cyan_color}<int> <int>{end_color} {error_details}",
    "EXAMPLE_1": "\nExample:\n\t1 3\n\tA1\n\t1:3",
    "EXAMPLE_2": "\nExample:\n<h|v>",
    # Turn Execution
    "PRE_SHOT": "Preparing to take a shot at {yellow_color}{target}{end_color}",
    "SHOT_AT": "Shot at {green_color}({x},{y}){end_color} was a {cyan_color}{result}{end_color}",
    "INVALID_COORD": "Coordinates are not valid, attempt again",
    "CURRENT_TURN": "Currently turn: {yellow_color}{current_player}{end_color} with player {green_color}{target_player}{end_color} being targeted",
    "STRUCK_AGAIN": "Location has {red_color}already been struck once{end_color} before try again.",
    "AI_SHOT_TAKEN": "{green_color}AI{end_color} fired at {white_color}({x}, {y}){end_color}",
    "SUNK_SHIP": "{purple_color}{ship_name}{end_color} has been sunk!",
    "OVERLAP": "{red_color}Overlap Detected!{end_color} Position ({x}, {y}) is already occupied by {occupant}",
    # Game State Ending
    "WON_GAME": "{green_color}{player_name}{end_color} has won the game!",
    # UI Display Headers
    "BOARD_HEADER_PLAYER": "{green_color}Player - {player_id} Board{end_color}",
    "BOARD_HEADER_TARGET": "{yellow_color}Player - {player_id} Board{end_color}",
    # Statistics Subsystem Reporting
    "STATS_FILLER": "=" * 50,
    "STATS_HEADER_TITLE": f"{'BATTLESHIP LIFETIME PERFORMANCE STATS':^55}",
    "STATS_HEADER_SUB": (
        f"{'Difficulty':<12} | {'Games':<5} | {'Wins':<4} | "
        f"{'Losses':<6} | {'Win %':<6} | {'Avg Turn Win':<12} | {'Shot Accuracy':<13}"
    ),
    "STATS_OUTPUT": "{a} | {b} | {c} | {d} | {e} | {f} | {g}",
}
