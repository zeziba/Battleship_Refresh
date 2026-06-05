from enum import Enum, auto, StrEnum

from Logger import get_logger
logger = get_logger(__name__)

SIZE = 10

class Colors(StrEnum):
    RESET = "\033[0m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[7m"
    BRIGHT_RED = "\033[196m"

EmptyTile = f"{Colors.BLUE}. {Colors.RESET}"
HitTile = f"{Colors.RED}X {Colors.RESET}"
UnknownTile = f"{Colors.WHITE}U {Colors.RESET}"
FillTile = f"{Colors.YELLOW}0 {Colors.RESET}"
SunkShip = f"{Colors.BRIGHT_RED}* {Colors.RESET}"


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

OUTPUTS = (
    "Please enter in your coords: x y\n\t",
    "Please enter in your directionality: h -> horizontal or v -> vertical\n\t",
    f"Please enter in the starting location of the {Colors.BLUE}{{}}{Colors.RESET}: x y\n\t",
    f"Placing {Colors.GREEN}{{}}{Colors.RESET}",
    f"{Colors.RED}Failed{Colors.RESET} to place {{}} at ({{}}, {{}}) with directionality {{}} as not a valid location.",
    "Failed to place {} as input was mangled",
    f"Input must be in the form of {Colors.CYAN}<int> <int>{Colors.RESET} {{}}",
    "\nExample:\n1 3",
    "\nExample:\n<h|v>",
    f"Preparing to take a shot at {Colors.YELLOW}{{}}{Colors.RESET}",
    f"Shot at {Colors.GREEN}({{}},{{}}){Colors.RESET} {{}}",
    "Coordinates are not valid, attempt again",
    f"Currently turn: {Colors.YELLOW}{{}}{Colors.RESET} with player {Colors.GREEN}{{}}{Colors.RESET} being targeted",
    f"{Colors.GREEN}{{}}{Colors.RESET} has won the game!",  
    f"Location has {Colors.RED}already been struck once{Colors.RESET} before try again.",
)


class State(Enum):
    RUNNING = auto()
    STOPPED = auto()
