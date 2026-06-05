import pytest

import src.Board


@pytest.fixture()
def board():
    yield src.Board.Board()


class TestBoard:
    def test_board_setup(self, board):
        assert board is not None

    def test_board_has_tiles(self, board):
        assert hasattr(board, "tiles") is True

    def test_board_has_tiles_setter(self, board):
        assert hasattr(getattr(type(board), "tiles", None), "fset")

    def test_board_tiles_set(self, board):
        b = board
        b.generate_board()
        ship_tile = src.Board.Tile.Tile("Ship", False)
        assert b.get(0, 0).has is None
        b.tiles_set(0, 0, ship_tile)
        for x, y in [(-1, 0), (0, -1), (10, 0), (0, 10)]:
            with pytest.raises(IndexError):
                b.tiles_set(x, y, ship_tile)

    def test_board_get(self, board):
        b = board
        b.generate_board()
        for index, _ in enumerate(b.tiles):
            # px + py * SIZE
            x, y = index % src.Board.SIZE, index // src.Board.SIZE
            assert type(b.get(x, y)) is src.Board.Tile.Tile

    def test_board_generate_board(self, board):
        b = board
        assert len(b.tiles) == 0
        b.generate_board()
        assert len(b.tiles) == src.Board.SIZE ** 2
        for t in b.tiles:
            assert type(t) is src.Board.Tile.Tile

    def test_board_generate_output(self, board):
        b = board
        b.generate_board()
        b_out = b.output_readable()
        assert (
            len(b_out) == src.Board.SIZE ** 2 * len(src.Board.HITTILE) + src.Board.SIZE
        )
        # print()
        # print(f"{b_out}")
        ship_tile = src.Board.Tile.Tile("Ship", False)
        changes = b.tiles_set(0, 0, ship_tile)
        # print(f"{changes}")
        b_out_changes = b.output_readable(False)
        # print(f"{b_out}")
        assert len(b_out) == len(b_out_changes)
        assert b_out != b_out_changes

    def test_board_output_array(self, board):
        b = board
        b.generate_board()
        b_out = b.output_array()
        assert len(b_out) == src.Board.SIZE ** 2
        assert all(type(tile) is int for tile in b_out)
