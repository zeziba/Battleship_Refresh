from enum import Enum, auto, StrEnum
from .Logger import get_logger

logger = get_logger(__name__)

SIZE = 10
ESC = "\033"


class Colors(StrEnum):
    # Standard Reset
    END = f"{ESC}[0m"

    # Foreground Colors
    BLACK = f"{ESC}[30m"
    RED = f"{ESC}[31m"
    GREEN = f"{ESC}[32m"
    BROWN = f"{ESC}[33m"
    BLUE = f"{ESC}[34m"
    PURPLE = f"{ESC}[35m"
    CYAN = f"{ESC}[36m"
    LIGHT_GRAY = f"{ESC}[37m"

    # Bright Foreground Colors
    DARK_GRAY = f"{ESC}[90m"
    LIGHT_RED = f"{ESC}[91m"
    LIGHT_GREEN = f"{ESC}[92m"
    YELLOW = f"{ESC}[93m"
    LIGHT_BLUE = f"{ESC}[94m"
    LIGHT_PURPLE = f"{ESC}[95m"
    LIGHT_CYAN = f"{ESC}[96m"
    LIGHT_WHITE = f"{ESC}[97m"
    BRIGHT_RED = f"{ESC}[38;5;196m"  # 256-color extended palette
    WHITE = f"{ESC}[7m"  # Inverted for block effect

    # Text Styles
    BOLD = f"{ESC}[1m"
    FAINT = f"{ESC}[2m"
    ITALIC = f"{ESC}[3m"
    UNDERLINE = f"{ESC}[4m"
    BLINK = f"{ESC}[5m"
    NEGATIVE = f"{ESC}[7m"
    CROSSED = f"{ESC}[9m"


EmptyTile = f"{Colors.LIGHT_BLUE}. {Colors.END}"
HitTile = f"{Colors.RED}X {Colors.END}"
UnknownTile = f"{Colors.WHITE}U {Colors.END}"
MissTile = f"{Colors.DARK_GRAY}+ {Colors.END}"


FLEET: dict[str, int] = {
    "CARRIER": 5,
    "BATTLESHIP": 4,
    "PATROLBOAT": 2,
    "SUBMARINE": 3,
    "DESTROYER": 3,
}


class Output(StrEnum):
    # Coordinate Inputs
    COORD_ENTER = "Please enter in your coords: x y\n\t"
    COORD_ENTER_GENERIC = "Enter starting coordinate (e.g., A5 or 0,4): "
    DIR_ENTER = "Please enter in your directionality: h -> horizontal or v -> vertical\n\t"
    DIR_INVALID = "Invalid orientation choice! Please type 'h' for horizontal or 'v' for vertical."
    START_LOCATION = f"Please enter in the starting location of the {Colors.BLUE}{{}}{Colors.END}: x y\n\t"
    TRY_AGAIN = "\tLocation is already selected."

    # Placement Logic
    PLACE = f"Placing {Colors.GREEN}{{}}{Colors.END}"
    FAILED_PLACE = f"{Colors.RED}Failed{Colors.END} to place {{}} at ({{}}, {{}}) with directionality {{}} as not a valid location."
    OUTSIDE_BOARD = "({}, {}) is outside the board!"
    MANGLED_PLACE = "Failed to place {} as input was mangled"
    WRONG_INPUT = f"Input must be in the form of {Colors.CYAN}<int> <int>{Colors.END} {{}}"
    EXAMPLE_1 = "\nExample:\n\t1 3\n\tA1\n\t1:3"
    EXAMPLE_2 = "\nExample:\n<h|v>"

    # Turn Execution
    PRE_SHOT = f"Preparing to take a shot at {Colors.YELLOW}{{}}{Colors.END}"
    SHOT_AT = f"Shot at {Colors.GREEN}({{}},{{}}){Colors.END} was a {Colors.LIGHT_CYAN}{{}}{Colors.END}"
    INVALID_COORD = "Coordinates are not valid, attempt again"
    CURRENT_TURN = (
        f"Currently turn: {Colors.YELLOW}{{}}{Colors.END} with player {Colors.GREEN}{{}}{Colors.END} being targeted"
    )
    STRUCK_AGAIN = f"Location has {Colors.RED}already been struck once{Colors.END} before try again."
    AI_SHOT_TAKEN = f"{Colors.GREEN}AI{Colors.END} fired at {Colors.LIGHT_WHITE}({{}}, {{}}){Colors.END}"
    SUNK_SHIP = f"{Colors.LIGHT_PURPLE}{{}}{Colors.END} has been sunk!"
    OVERLAP = f"{Colors.RED}Overlap Detected!{Colors.END} Position ({{}}, {{}}) is already occupied by {{}}"

    # Game State Ending
    WON_GAME = f"{Colors.GREEN}{{}}{Colors.END} has won the game!"

    # UI Display Headers
    BOARD_PRINTPUT_HEADER_1 = f"{Colors.GREEN}Player - {{}} Board{Colors.END}"
    BOARD_PRINTPUT_HEADER_2 = f"{Colors.YELLOW}Player - {{}} Board{Colors.END}"

    # Statistics Subsystem Reporting
    STATS_FILLER = "=" * 50
    STATS_HEADER_TITLE = f"{'BATTLESHIP LIFETIME PERFORMANCE STATS':^55}"
    STATS_HEADER_SUB = (
        f"{'Difficulty':<12} | {'Games':<5} | {'Wins':<4} | "
        f"{'Losses':<6} | {'Win %':<6} | {'Avg Turn Win':<12} | {'Shot Accuracy':<13}"
    )
    STATS_OUTPUT = "{} | {} | {} | {} | {} | {} | {}"


class State(Enum):
    RUNNING = auto()
    STOPPED = auto()
