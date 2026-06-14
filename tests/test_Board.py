import pytest
from unittest.mock import MagicMock, patch

# Adjust the import path based on your actual package name if necessary
from src.Board import Board

"""
Auto-generated Test File
"""


class TestBoard:
    @pytest.fixture
    def mock_dependencies(self):
        """Fixture to patch dependencies like config, GameRules, and Tile if needed."""
        with patch("src.config") as mock_config, patch("src.GameRules") as mock_rules, patch("src.Tile") as mock_tile:

            # Setup default config width/height
            mock_config.board_width = 10

            # Mock Tile creation to return a Mock object by default
            mock_tile.Tile.side_effect = lambda has, hit: MagicMock(has=has, hit=hit)

            yield {"config": mock_config, "GameRules": mock_rules, "Tile": mock_tile}

    @pytest.fixture
    def default_board(self, mock_dependencies):
        """Provides a standard 10x10 board for testing."""
        return Board(height=10, width=10)

    # --- Initialization & Properties Tests ---

    def test_board_initialization(self, default_board):
        """Test that the board initializes with correct dimensions and tile count."""
        assert default_board.height == 10
        assert default_board.width == 10
        assert default_board.size == 100
        assert len(default_board.tiles) == 100

    def test_board_size_zero(self):
        """Test size calculation when width or height is zero."""
        board = Board(height=0, width=10)
        assert board.size == 0

    # --- Coordinate Conversion & Indexing Tests ---

    def test_convert_to_1d_index_valid(self, default_board):
        """Test standard 2D to 1D index mathematical mapping."""
        # Top-left corner
        assert default_board._convert_to_1d_index(0, 0) == 0
        # Somewhere in the middle: x=5, y=3 -> 5 + (3 * 10) = 35
        assert default_board._convert_to_1d_index(5, 3) == 35
        # Bottom-right corner
        assert default_board._convert_to_1d_index(9, 9) == 99

    @pytest.mark.parametrize(
        "x, y",
        [
            (-1, 5),  # X under bounds
            (10, 5),  # X out of bounds
            (5, -1),  # Y under bounds
            (5, 10),  # Y out of bounds
            (10, 10),  # Both out of bounds
        ],
    )
    def test_convert_to_1d_index_out_of_bounds(self, default_board, x, y):
        """Test that indexing outside the board dimensions raises an IndexError."""
        with pytest.raises(IndexError, match="track outside of board"):
            default_board._convert_to_1d_index(x, y)

    def test_convert_to_1d_index_value_error(self):
        """Test that missing height or width raises a ValueError."""
        board = Board(height=0, width=0)
        # Manually force dimensions to None to test the ValueError branch
        board.width = None  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(ValueError, match="Width or Height not set"):
            board._convert_to_1d_index(0, 0)

    # --- Getters and Setters Tests ---

    def test_get_and_tiles_set(self, default_board):
        """Test that you can set a tile at a coordinate and retrieve it accurately."""
        mock_tile = MagicMock()

        # Set the tile
        result = default_board.tiles_set(4, 2, mock_tile)

        # Check that the setter returns the tile and it's placed in the correct 1D index (24)
        assert result == mock_tile
        assert default_board._tiles[24] == mock_tile

        # Retrieve the tile via get()
        assert default_board.get(4, 2) == mock_tile

    # --- Game Logic Tests (all_ships_sunk) ---

    def test_all_ships_sunk_empty_board(self, default_board):
        """If there are no ships on the board, all_ships_sunk should return False."""
        # Ensure all mocked tiles have 'has = None'
        for tile in default_board._tiles:
            tile.has = None

        assert default_board.all_ships_sunk is False

    def test_all_ships_sunk_true(self, default_board):
        """Should return True if all ships present on the board are sunk."""
        # Setup a mix of empty tiles and sunk ships
        mock_sunk_ship = MagicMock()
        mock_sunk_ship.is_sunk = True

        for i in range(len(default_board._tiles)):
            if i < 3:
                # Place 3 sunk ships
                default_board._tiles[i].has = mock_sunk_ship
            else:
                # Rest are empty
                default_board._tiles[i].has = None

        assert default_board.all_ships_sunk is True

    def test_all_ships_sunk_false(self, default_board):
        """Should return False if at least one ship on the board is afloat."""
        mock_sunk_ship = MagicMock()
        mock_sunk_ship.is_sunk = True

        mock_alive_ship = MagicMock()
        mock_alive_ship.is_sunk = False

        # 1 sunk ship, 1 alive ship, rest empty
        default_board._tiles[0].has = mock_sunk_ship
        default_board._tiles[1].has = mock_alive_ship
        for i in range(2, len(default_board._tiles)):
            default_board._tiles[i].has = None

        assert default_board.all_ships_sunk is False
