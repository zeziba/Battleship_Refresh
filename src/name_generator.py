from pathlib import Path
import random

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESOURCE_FOLDER = PROJECT_ROOT / "resources"


class NameGenerator:

    def __init__(self) -> None:
        self._first_names = self._load_resources("first-names.txt")
        self._middle_names = self._load_resources("middle-names.txt")
        self._places = self._load_resources("places.txt")

    def create_random_name(self) -> str:
        if not (self._first_names and self._middle_names and self._places):
            raise ValueError("Failed to load resources")

        choice = random.choice
        return f"{choice(list(self._first_names))} {choice(list(self._middle_names))} of {choice(list(self._places))}"

    def _load_resources(self, filename: str) -> tuple[str, ...]:
        file_path = RESOURCE_FOLDER / filename

        with open(file_path, "r", encoding="utf-8") as file:
            return tuple(line.strip() for line in file if line.strip())


if __name__ == "__main__":
    generator = NameGenerator()
    print(generator.create_random_name())
