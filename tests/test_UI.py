from random import randint

import pytest

import src.GameRules
import src.UI


@pytest.fixture()
def ui():
    UI = src.UI.UI()
    yield UI


def generate_input(s_out: str = ""):
    while True:
        yield "".join([chr(randint(97, 123)) for _ in range(randint(1, 100))])


def generate_numbers(s_out: str = ""):
    while True:
        yield f"{randint(0, 10)} {randint(0, 10)}"


class TestUI:
    def test_get_coords(self, ui, monkeypatch):
        assert hasattr(ui, "get_coords")
        for cho in list(src.GameRules.OUTPUTS[:3]):
            GEN = generate_numbers()
            monkeypatch.setattr("builtins.input", lambda args: next(GEN, args))
            for _ in range(10):
                ui.get_coords(cho)

    def test_get_selection(self, ui, monkeypatch):
        assert hasattr(ui, "get_selection")
        for cho in list(src.GameRules.OUTPUTS[:3]):
            GEN = generate_input()
            monkeypatch.setattr("builtins.input", lambda args: next(GEN, args))
            for _ in range(10):
                ui.get_selection(cho)
