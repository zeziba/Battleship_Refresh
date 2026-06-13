import pytest
from unittest.mock import MagicMock, patch

from src.Fleet import FleetType, GeneralFleet
from src.Ship import Ship


class TestFleetSuite:
    @pytest.fixture
    def mock_gamerules_fleet(self):
        test_fleet_config = {
            "CARRIER": 5,
            "BATTLESHIP": 4,
            "PATROLBOAT": 2,
            "SUBMARINE": 3,
            "DESTROYER": 3,
        }
        with patch("src.GameRules.FLEET", test_fleet_config):
            yield test_fleet_config

    @pytest.fixture
    def fresh_default_fleet(self, mock_gamerules_fleet) -> GeneralFleet:
        return GeneralFleet()

    def test_fleet_type_enum_values(self):
        assert FleetType.CARRIER == "carrier"
        assert FleetType.BATTLESHIP == "battleship"
        assert FleetType.PATROLBOAT == "patrolboat"
        assert FleetType.DESTROYER == "destroyer"
        assert FleetType.SUBMARINE == "submarine"

    def test_fleet_initialization_populates_all_types(self, fresh_default_fleet, mock_gamerules_fleet):
        assert fresh_default_fleet._fleet is not None
        assert len(fresh_default_fleet._fleet) == 5
        
        for enum_type in FleetType:
            assert enum_type in fresh_default_fleet._fleet
            ship_instance = fresh_default_fleet._fleet[enum_type]
            assert isinstance(ship_instance, Ship)

            rule_name = enum_type.name
            assert ship_instance.name == rule_name
            assert ship_instance.length == mock_gamerules_fleet[rule_name]

    def test_fleet_initialization_with_custom_fleet_comp(self, mock_gamerules_fleet):
        custom_comp = {"CARRIER": 5, "SUBMARINE": 3}
        custom_fleet = GeneralFleet(fleet_comp=custom_comp)
        
        assert custom_fleet._fleet is not None
        assert len(custom_fleet._fleet) == 5
        assert custom_fleet.fleet_comp == custom_comp

    def test_ships_property_returns_list_of_ships(self, fresh_default_fleet):
        ships_list = fresh_default_fleet.ships
        assert isinstance(ships_list, list)
        assert len(ships_list) == 5
        assert all(isinstance(ship, Ship) for ship in ships_list)

    def test_ships_property_when_fleet_is_empty(self):
        empty_fleet = GeneralFleet()
        empty_fleet._fleet = {}
        assert empty_fleet.ships == []

    def test_all_sunk_property_evaluates_true(self, fresh_default_fleet):
        mock_sunk_ships = []
        for _ in range(5):
            mock_ship = MagicMock(spec=Ship)
            mock_ship.is_sunk = True
            mock_sunk_ships.append(mock_ship)

        for enum_type, mock_ship in zip(FleetType, mock_sunk_ships):
            fresh_default_fleet._fleet[enum_type] = mock_ship

        assert fresh_default_fleet.all_sunk is True

    def test_all_sunk_property_false_if_any_alive(self, fresh_default_fleet):
        mock_ships = []
        for i in range(5):
            mock_ship = MagicMock(spec=Ship)
            mock_ship.is_sunk = (i != 4)
            mock_ships.append(mock_ship)

        for enum_type, mock_ship in zip(FleetType, mock_ships):
            fresh_default_fleet._fleet[enum_type] = mock_ship

        assert fresh_default_fleet.all_sunk is False

    def test_hit_method_registers_damage_on_target_ship(self, fresh_default_fleet):
        mock_ship_miss = MagicMock(spec=Ship)
        mock_ship_miss.hit.return_value = False

        mock_ship_hit = MagicMock(spec=Ship)
        mock_ship_hit.hit.return_value = True

        fresh_default_fleet._fleet[FleetType.CARRIER] = mock_ship_miss
        fresh_default_fleet._fleet[FleetType.BATTLESHIP] = mock_ship_hit

        assert fresh_default_fleet.hit(2, 3) is True
        
        mock_ship_miss.hit.assert_called_once_with(2, 3)
        mock_ship_hit.hit.assert_called_once_with(2, 3)

    def test_hit_method_returns_false_on_total_miss(self, fresh_default_fleet):
        assert fresh_default_fleet.hit(9, 9) == False