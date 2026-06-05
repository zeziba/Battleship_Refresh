from random import choice

import pytest

import src.Tile
import src.Ship
import src.GameRules


@pytest.fixture()
def tile():
    yield src.Tile.Tile(None, False)


class TestTile:
    def test_tile_setup(self, tile):
        assert tile is not None

    def test_tile_has_hit(self, tile):
        assert hasattr(tile, "hit")

    def test_tile_has_contains(self, tile):
        assert hasattr(tile, "contains")

    def test_tile_contains(self, tile):
        assert tile.contains is False
        tile.contains = 1
        assert tile.contains is True
        with pytest.raises(IndexError):
            tile.contains = 5

    def test_tile_init_hit(self, tile):
        assert tile.hit is False

    def test_tile_can_hit(self, tile):
        t = tile
        t.hit = not t.hit
        assert t.hit is True
        t.hit = not t.hit

    def test_tile_has_obj_return(self, tile):
        name = choice(list(src.GameRules.FLEET.keys()))
        length = src.GameRules.FLEET[name]
        ship = src.Ship.Ship(name, length)
        tile.contains = ship
        assert tile.has is ship
        assert type(tile.has) is src.Ship.Ship
