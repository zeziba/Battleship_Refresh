import pytest
from unittest.mock import MagicMock

from src import config as _config
from src.Board import Board, HITTILE, EMPTYTILE


class TestBoardSuite:
    @pytest.fixture()
    def fresh_board(self) -> Board:
        return Board()
    
    @pytest.fixture()
    def mock_tile(self):
        tile = MagicMock()
        tile.hit = False
        tile.contains = None
        tile.has = None
        return tile
    
    @pytest.fixture()
    def mock_ship(self):
        ship = MagicMock()
        ship.name = ""
        ship.length = 0
        ship.is_sunk = False
        return ship
    
    def test_board_initialization_defaults(self, fresh_board: Board):
        assert fresh_board.width == _config.board_width
        assert fresh_board.height == _config.board_height
        assert len(fresh_board.tiles) == fresh_board.width * fresh_board.height

    def test_board_initialization_custom_dimensions(self):
        custom_board = Board(height=12, width=8)
        assert custom_board.width == 8
        assert custom_board.height == 12
        assert custom_board.size == 96

    def test_board_size_property(self, fresh_board: Board):
        expected_size = fresh_board.width * fresh_board.height
        assert fresh_board.size == expected_size

    def test_tiles_property_returns_immutable_tuple(self, fresh_board: Board):
        tiles_property = fresh_board.tiles
        assert isinstance(tiles_property, tuple)

        with pytest.raises(TypeError):
            tiles_property[0] = MagicMock() # pyright: ignore[reportIndexIssue]
    
    def test_convert_to_1d_index_valid(self, fresh_board: Board):
        assert fresh_board._convert_to_1d_index(0, 0) == 0
        assert fresh_board._convert_to_1d_index(1, 2) == 1 + (2 * fresh_board.width)

    @pytest.mark.parametrize("x, y", [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ])
    def test_convert_to_1d_index_out_of_bounds_raises_index_error(self, fresh_board: Board,x: int, y: int):
        if 0 <= x < fresh_board.width and 0 <= y < fresh_board.height:
            pytest.skip("Parameterized coordinate is accidentally valid for current default size")
        
        with pytest.raises(IndexError, match="track outside of board"):
            fresh_board._convert_to_1d_index(x, y)

    def test_all_ships_sunk_when_empty(self, fresh_board: Board):
        assert fresh_board.all_ships_sunk is False

    def test_all_ships_sunk_true(self, fresh_board: Board, mock_ship, mock_tile):
        mock_ship.is_sunk = True

        mock_tile.has = mock_ship

        fresh_board._tiles[0] = mock_tile

        assert fresh_board.all_ships_sunk is True

    def  test_all_ships_sunk_false(self, fresh_board: Board):
        mock_ship_1 = MagicMock()
        mock_ship_1.is_sunk = True
        mock_ship_2 = MagicMock()
        mock_ship_2.is_sunk = False

        mock_occupied_tile_1 = MagicMock()
        mock_occupied_tile_1.has = mock_ship_1
        mock_occupied_tile_2 = MagicMock()
        mock_occupied_tile_2.has = mock_ship_2

        fresh_board._tiles[0] = mock_occupied_tile_1
        fresh_board._tiles[1] = mock_occupied_tile_2

        assert fresh_board.all_ships_sunk is False

    def test_board_scales_with_global_config_mutation(self):
        original_default = _config.board_width
        try:
            _config.board_width = 15
            custom_board = Board(_config.board_height, _config.board_width)
            assert custom_board.height == 10
            assert custom_board.width == 15
        finally:
            _config.board_width = original_default