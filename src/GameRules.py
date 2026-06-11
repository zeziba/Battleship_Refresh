from enum import Enum, auto, StrEnum

from Logger import get_logger

logger = get_logger(__name__)

SIZE = 10
ESC = '\033'


class Colors(StrEnum):
    WHITE = f"{ESC}[7m"
    BRIGHT_RED = f"{ESC}[196m"
    BLACK = f"{ESC}[0;30m"
    RED = f"{ESC}[0;31m"
    GREEN = f"{ESC}[0;32m"
    BROWN = f"{ESC}[0;33m"
    BLUE = f"{ESC}[0;34m"
    PURPLE = f"{ESC}[0;35m"
    CYAN = f"{ESC}[0;36m"
    LIGHT_GRAY = f"{ESC}[0;37m"
    DARK_GRAY = f"{ESC}[1;30m"
    LIGHT_RED = f"{ESC}[1;31m"
    LIGHT_GREEN = f"{ESC}[1;32m"
    YELLOW = f"{ESC}[1;33m"
    LIGHT_BLUE = f"{ESC}[1;34m"
    LIGHT_PURPLE = f"{ESC}[1;35m"
    LIGHT_CYAN = f"{ESC}[1;36m"
    LIGHT_WHITE = f"{ESC}[1;37m"
    BOLD = f"{ESC}[1m"
    FAINT = f"{ESC}[2m"
    ITALIC = f"{ESC}[3m"
    UNDERLINE = f"{ESC}[4m"
    BLINK = f"{ESC}[5m"
    NEGATIVE = f"{ESC}[7m"
    CROSSED = f"{ESC}[9m"
    END = f"{ESC}[0m"


EmptyTile = f"{Colors.LIGHT_BLUE}. {Colors.END}"
HitTile = f"{Colors.RED}X {Colors.END}"
UnknownTile = f"{Colors.WHITE}U {Colors.END}"
MissTile = f"{Colors.DARK_GRAY}+{Colors.END} "


def check_xy(x: int, y: int) -> bool:
    """Checks if the x, y coords fall within the board"""
    logger.info(f"Checking ({x}, {y})")
    return (0 <= x < SIZE) and (0 <= y < SIZE)


FLEET = {
    "CARRIER": 5,
    "BATTLESHIP": 4,
    "PATROLBOAT": 2,
    "SUBMARINE": 3,
    "DESTROYER": 3,
}

class Output(StrEnum):
    COORD_ENTER = "Please enter in your coords: x y\n\t"
    COORD_ENTER_GENERIC = "Enter starting coordinate (e.g., A5 or 0,4): "
    DIR_ENTER = "Please enter in your directionality: h -> horizontal or v -> vertical\n\t"
    DIR_INVALID = "Invalid orientation choice! Please type 'h' for horizontal or 'v' for vertical."
    START_LOCATION = f"Please enter in the starting location of the {Colors.BLUE}{{}}{Colors.END}: x y\n\t"
    TRY_AGAIN = "\tLocation is already selected."
    PLACE = f"Placing {Colors.GREEN}{{}}{Colors.END}"
    FAILED_PLACE = f"{Colors.RED}Failed{Colors.END} to place {{}} at ({{}}, {{}}) with directionality {{}} as not a valid location."
    OUTSIDE_BOARD = "({}, {}) is outside the board!"
    MANGLED_PLACE = "Failed to place {} as input was mangled"
    WRONG_INPUT = f"Input must be in the form of {Colors.CYAN}<int> <int>{Colors.END} {{}}"
    EXAMPLE_1 = "\nExample:\n\t1 3\n\tA1\n\t1:3"
    EXAMPLE_2 = "\nExample:\n<h|v>"
    PRE_SHOT = f"Preparing to take a shot at {Colors.YELLOW}{{}}{Colors.END}"
    SHOT_AT = f"Shot at {Colors.GREEN}({{}},{{}}){Colors.END} hit {Colors.LIGHT_CYAN}{{}}{Colors.END}"
    INVALID_COORD = "Coordinates are not valid, attempt again"
    CURRENT_TURN = f"Currently turn: {Colors.YELLOW}{{}}{Colors.END} with player {Colors.GREEN}{{}}{Colors.END} being targeted"
    WON_GAME = f"{Colors.GREEN}{{}}{Colors.END} has won the game!"
    STRUCK_AGAIN = f"Location has {Colors.RED}already been struck once{Colors.END} before try again."
    AI_SHOT_TAKEN = f"{Colors.GREEN}AI{Colors.END} fired at {Colors.LIGHT_WHITE}({{}}, {{}}){Colors.END}"
    SUNK_SHIP = f"{Colors.LIGHT_PURPLE}{{}}{Colors.END} has been sunk!"
    OVERLAP = f"{Colors.RED}Overlap Detected!{Colors.END} Position ({{}}, {{}}) is already occupied by {{}}"


class State(Enum):
    RUNNING = auto()
    STOPPED = auto()
