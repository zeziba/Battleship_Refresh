from enum import Enum, auto

SIZE = 10

EmptyTile = ". "
HitTile = "X "
UnknownTile = "U "
FillTile = "{} "


def check_xy(x: int, y: int) -> bool:
    """Checks if the x, y coords fall within the board"""
    size = SIZE - 1
    return (size >= x >= 0) and (size >= y >= 0)


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
    "Please enter in the starting location of the {}: x y\n\t",
    "Placing {}",
    "Failed to place {} at ({}, {}) with directionality {} as not a valid location.",
    "Failed to place {} as input was mangled",
    "Input must be in the form of <int> <int> {}",
    "\nExample:\n1 3",
    "\nExample:\n<h|v>",
    "Preparing to take a shot at {}",
    "Shot at ({},{}) {}",
    "Coordinates are not valid, attempt again",
    "Currently turn: {} with player {} being targeted",
    "{} has won the game!",
    "Location has already been struck once before try again.",
)


class State(Enum):
    RUNNING = auto()
    STOPPED = auto()
