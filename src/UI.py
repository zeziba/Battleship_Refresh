from dataclasses import dataclass


@dataclass()
class UI:
    def get_coords(self, output: str) -> tuple[int, int]:
        x, y = input(f"{output}").split(" ")
        return int(x), int(y)

    def get_selection(self, selection: str) -> str:
        return input(f"{selection}")

    def output(self, selection: str) -> None:
        print(f"{selection}")
