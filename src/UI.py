from dataclasses import dataclass

import os
import time


@dataclass()
class UI:
    def get_coords(self, output: str) -> tuple[int, int]:
        x, y = input(f"{output}").split(" ")
        return int(x), int(y)

    def get_selection(self, selection: str) -> str:
        return input(f"{selection}")

    def output(self, selection: str) -> None:
        print(f"{selection}")

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause(seconds: float = 1.5):
        time.sleep(seconds)
    
    @staticmethod
    def prompt_to_continue():
        input("\nPress [Enter] to continue...")
