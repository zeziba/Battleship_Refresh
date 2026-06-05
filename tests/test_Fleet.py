from random import choice

import pytest

import src.Fleet


def test_fleet():
    for i in list(src.Fleet.Fleet):
        assert hasattr(i, "name")
        assert hasattr(i, "value")


def test_FLEET():
    for ship, value in src.Fleet.FLEET.items():
        assert ship in list(src.Fleet.Fleet)
        assert type(value) is int


@pytest.fixture()
def resource():
    f = src.Fleet.GeneralFleet()
    f.generate()
    yield f


class TestGenerateFleet:
    def test_fleet_setup(self, resource):
        assert resource is not None

    def test_fleet_has_fleet(self, resource):
        assert hasattr(resource, "fleet")

    def test_gen_fleet(self):
        """Tests Fleet Generation"""
        fleet = src.Fleet.GeneralFleet()
        assert len(fleet.fleet) == 0
        fleet.generate()
        assert len(fleet.fleet) == len(src.Fleet.FLEET)

    def test_generated_fleet(self, resource):
        """Tests Generated Fleet"""
        f = resource
        assert f.fleet is not None
        for ship in f.fleet:
            assert type(f.fleet[ship]) is src.Fleet.Ship.Ship

    def test_fleet_hit(self, resource):
        f = resource
        board = src.Fleet.Ship.Board.Board()
        board.generate_board()
        for index, ship in enumerate(f.fleet):
            f.fleet[ship].place_ship(index, 0, board)
        for ship in f.fleet:
            for pos in f.fleet[ship].positions:
                x, y = pos.split(",")
                x = int(x)
                y = int(y)
                assert f.hit(x, y) is True
                assert board.get(x, y).hit is True, f"{board.get(x, y)}"
        assert f.hit(0, 0) is False

    def test_fleet_other_fleet(self, resource):
        """Test Fleet:GeneralFleet:other_ships"""
        ship = choice(list(src.Fleet.Fleet))
        for s in resource.other_ships(ship):
            assert s is not ship

    def test_fleet_check_possible_placement(self, resource):
        """Test the check possible placement from Fleet:GeneralFleet:check_possible_placement"""
        fleet = resource
        # Test all failing positions
        for direction in list(src.Fleet.Ship.Direction):
            for key, ship in fleet.fleet.items():
                ship.directionality = direction
                for xy in range(src.Fleet.GameRules.SIZE - 1):
                    v = src.Fleet.GameRules.SIZE - ship.length
                    x = v if direction is src.Fleet.Ship.Direction.HORIZONTAL else xy
                    y = (
                        v
                        if direction is not src.Fleet.Ship.Direction.HORIZONTAL
                        else xy
                    )
                    assert (
                        fleet.can_place(ship, x, y) is False
                    ), f"{ship}@(X: {x}, Y: {y}):{ship.directionality} should have failed"
                for xy in range(src.Fleet.GameRules.SIZE - 1):
                    v = -1
                    x = v if direction is src.Fleet.Ship.Direction.HORIZONTAL else xy
                    y = (
                        v
                        if direction is not src.Fleet.Ship.Direction.HORIZONTAL
                        else xy
                    )
                    assert (
                        fleet.can_place(ship, x, y) is False
                    ), f"{ship}@(X: {x}, Y: {y}):{ship.directionality} should have failed"

        # Test some passing positions
        for direction in list(src.Fleet.Ship.Direction):
            for key, ship in fleet.fleet.items():
                ship.directionality = direction
                for xy in range(src.Fleet.GameRules.SIZE - 1):
                    x = (
                        xy
                        if direction is not src.Fleet.Ship.Direction.HORIZONTAL
                        else 0
                    )
                    y = xy if direction is src.Fleet.Ship.Direction.HORIZONTAL else 0
                    assert (
                        fleet.can_place(ship, x, y) is True
                    ), f"{ship}@(X: {x}, Y: {y}):{ship.directionality} should have passed"

        # Test if can place ship on another ship
        ships = [ship for ship in fleet.fleet]
        board = src.Fleet.Ship.Board.Board()
        board.generate_board()
        fleet.fleet[ships[0]].place_ship(0, 0, board)
        for other in fleet.other_ships(fleet.fleet[ships[0]]):
            assert (
                fleet.can_place(other, 0, 0) is False
            ), f"{other}@(X: 0, Y: 0) should have failed"
