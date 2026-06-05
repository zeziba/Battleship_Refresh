import pytest
from io import StringIO
import sys

import src.Game

src.Game.TESTING = True


@pytest.fixture()
def game():
    players = (False, False)
    yield src.Game.Game(players=players)


@pytest.fixture()
def game_players():
    players = (True, True)
    yield src.Game.Game(players=players)


def get_coord():
    size = src.Game.GameRules.SIZE
    for i in range(size ** 2):
        yield i % size, i // size


class TestGame:
    def test_game_setup(self, game):
        assert game is not None

    def test_game_has_players(self, game):
        assert hasattr(game, "players")

    def test_game_has_player(self, game):
        assert hasattr(game, "player")

    def test_game_has_state(self, game):
        assert hasattr(game, "state")

    def test_game_has_stopped(self, game):
        assert hasattr(game, "stopped")

    def test_game_start(self, game):
        g = game
        assert g.stopped
        g.start()
        assert not g.stopped

    def test_game_stop(self, game):
        g = game
        assert g.stopped
        g.start()
        assert not g.stopped
        g.stop()
        assert g.stopped

    def test_game_players(self, game):
        assert type(game.players) is tuple
        for i in game.players:
            assert type(i) is bool

    def test_game_dict_players(self, game):
        assert all(type(p) is src.Game.Player.Player for p in game.player)

    def test_game_set_up(self, game):
        # Test AI setup
        g = game
        for p in g.player:
            assert len(p.fleet.fleet) == 0
            assert len(p.board.tiles) == 0
        g.set_up()
        for p in g.player:
            assert len(p.fleet.fleet) == len(src.Game.GameRules.FLEET)
            assert len(p.board.tiles) == src.Game.GameRules.SIZE ** 2
        src.Game.TESTING = False
        # Just need to check if g.set_up still works if TESTING is disabled
        g.set_up()
        src.Game.TESTING = True

    def test_game_set_up_players(self, game_players, monkeypatch):
        output = sys.stdout
        sys.stdout = StringIO()
        # Test Players Setup
        g = game_players

        def generated_input(*args, **kwargs):
            def xy(x: int = 0, y: int = 0, direction: str = "h"):
                for i in range(src.Game.GameRules.SIZE):
                    yield x, y
                    yield x, y
                    x = x + 1 if direction == "h" else 1
                    y = y + 1 if direction == "v" else 0

            inputs_coords = [f"{x} {y}" for x, y in xy()]
            inputs_dir = ["v" for _ in range(len(inputs_coords))]
            inputs = [
                sub_item for item in zip(inputs_coords, inputs_dir) for sub_item in item
            ]
            for input_ in inputs:
                yield input_

        src.Game.TESTING = False
        GEN = generated_input()
        monkeypatch.setattr("builtins.input", lambda args: next(GEN, args))
        for p in g.player:
            assert len(p.fleet.fleet) == 0
            assert len(p.board.tiles) == 0
        g.set_up()
        for p in g.player:
            assert len(p.fleet.fleet) == len(src.Game.GameRules.FLEET)
            assert len(p.board.tiles) == src.Game.GameRules.SIZE ** 2

        sys.stdout = output

    def test_game_check_win(self, game):
        g = game
        assert g.stopped
        g.set_up()
        size = src.Game.GameRules.SIZE
        for i in range(size ** 2 - 1):
            x, y = i % size, i // size
            for p in g.player:
                assert not g.stopped
                p.fleet.hit(x, y)
            if g.any_won:
                break
        assert g.stopped
