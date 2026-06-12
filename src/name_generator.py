from pathlib import Path
from os import path
import random

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESOURCE_FOLDER = "resources"

class NameGenerator:
    _first_names: set[str] = set()
    _middle_names: set[str] = set()
    _places: set[str] = set()

    def __init__(self) -> None:
        with open(path.join(PROJECT_ROOT, RESOURCE_FOLDER, "first-names.txt"), "r") as file:
            self._first_names = set([line.strip() for line in file.readlines()])
        with open(path.join(PROJECT_ROOT, RESOURCE_FOLDER, "middle-names.txt"), "r") as file:
            self._middle_names = set([line.strip() for line in file.readlines()])
        with open(path.join(PROJECT_ROOT, RESOURCE_FOLDER, "places.txt"), "r") as file:
            self._places = set([line.strip() for line in file.readlines()])

    def create_random_name(self) -> str:
        choice = random.choice
        return f"{choice(list(self._first_names))} {choice(list(self._middle_names))} of {choice(list(self._places))}"
    

if __name__ == "__main__":
    generator = NameGenerator()
    print(generator.create_random_name())