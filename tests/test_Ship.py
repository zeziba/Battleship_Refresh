from random import choice, randint

import pytest

import src.GameRules
import src.Ship


def direction() -> src.Ship.Direction:
    return choice(list(src.Ship.Direction))


def ship() -> src.Ship.Ship:
    name = choice(list(src.GameRules.FLEET.keys()))
    length = src.GameRules.FLEET[name]
    return src.Ship.Ship(name, length)


def test_direction():
    for d in src.Ship.Direction:
        assert type(d) is src.Ship.Direction
        assert d.name is not None
        assert d.value >= 0


@pytest.fixture()
def resource() -> src.Ship.Ship:
    yield ship()


def coord() -> int:
    return randint(0, 9)


class TestShip:
    def test_ship_setup(self, resource):
        assert resource is not None

    def test_ship_has_length(self, resource):
        assert hasattr(resource, "length")

    def test_ship_has_name(self, resource):
        assert hasattr(resource, "name")

    def test_ship_has_directionality(self, resource):
        assert hasattr(resource, "directionality")

    def test_ship_has_is_sunk(self, resource):
        assert hasattr(resource, "is_sunk")

    def test_ship_has_is_placed(self, resource):
        assert hasattr(resource, "is_placed")

    def test_ship_generation(self, resource):
        """Tests ship generation"""
        assert type(resource) is src.Ship.Ship
        assert resource.name is not None
        assert resource.length >= 0
        assert resource.hit_points >= 0
        assert resource.directionality is not None

    def test_ship_placement(self, resource):
        """Tests Ship Placement"""
        assert callable(resource.place_ship)

        b = src.Ship.Board.Board()
        b.generate_board()

        # Check vertical
        # Check at (0, 0)
        s = ship()
        assert s.place_ship(0, 0, b) is True
        assert s.is_placed is True

        # Check if can place same ship
        assert s.place_ship(0, 0, b) is False

        # Check each position to ensure out of bounds errors
        for i in range(src.GameRules.SIZE):
            s = ship()
            z = src.GameRules.SIZE - s.length + 1
            with pytest.raises(IndexError):
                assert s.place_ship(i, z, b) is True
        # Check random locations of the board to ensure it places the ships correctly
        for _ in range(50):
            s = ship()
            x, y = coord(), coord()
            y = y if y - s.length < 0 else y - s.length
            assert s.place_ship(x, y, b) is True
            assert s.is_placed is True

        # Check horizontal
        # Check at (0, 0)
        s = ship()
        s.directionality = src.Ship.Direction.HORIZONTAL
        assert s.place_ship(0, 0, b) is True
        assert s.is_placed is True

        # Check each position to ensure out of bounds errors
        for i in range(src.GameRules.SIZE):
            s = ship()
            s.directionality = src.Ship.Direction.HORIZONTAL
            z = src.GameRules.SIZE - s.length + 1
            with pytest.raises(IndexError):
                assert s.place_ship(z, i, b) is True
        # Check random locations of the board to ensure it places the ships correctly
        for _ in range(50):
            s = ship()
            s.directionality = src.Ship.Direction.HORIZONTAL
            x, y = coord(), coord()
            x = x if x - s.length < 0 else x - s.length
            assert s.place_ship(x, y, b) is True
            assert s.is_placed is True

    def test_ship_hit(self, resource):
        """Test if a ship is hit or not"""
        s = resource
        b = src.Ship.Board.Board()
        b.generate_board()
        assert callable(s.hit)
        assert s.hit(coord(), coord()) is False
        s.place_ship(0, 0, b)
        hp = s.hit_points
        assert s.is_sunk is False
        for key in s.positions:
            x, y = key.split(",")
            assert hp == s.hit_points
            assert s.hit(int(x), int(y)) is True
            hp -= 1
            assert s.hit(int(x), int(y)) is False
            assert hp == s.hit_points
        assert s.is_sunk is True

    def test_ship_contains(self, resource):
        s = resource
        b = src.Ship.Board.Board()
        b.generate_board()
        s.place_ship(0, 0, b)
        assert s.contains(0, 0) is True
