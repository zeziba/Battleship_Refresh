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


class State(Enum):
    RUNNING = auto()
    STOPPED = auto()
