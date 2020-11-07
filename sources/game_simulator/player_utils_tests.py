import unittest
from .player_utils import PlayerUtils
from .board import Board
from ..data_structures.gaddag import GADDAG
from .tile_bag import Tile, TileBag


class PlayerTests(unittest.TestCase):
    def test_horizontal_hook_detection(self):
        tile = Tile('A', 1)
        tile_map = TileBag().map
        board = Board(GADDAG(), tile_map)

        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            []
        )
        board.board[0][3].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            [((0,3), tile, 3, 11)]
        )

        board.board[0][0].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            [
                ((0,3), tile, 1, 11),
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[0][4].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            [
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[0][7].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            [
                ((0, 0), tile, 0, 1),
                ((0, 7), tile, 1, 7),
            ]
        )

        board = Board(GADDAG(), tile_map)
        board.board[3][0].letter = tile
        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            [
                ((3, 0), tile, 0, 14),
            ]
        )

        board = Board(GADDAG(), tile_map)
        board.board[14][14].letter = tile
        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            [
                ((14, 14), tile, 14, 0),
            ]
        )

    def test_greedy_vertical_hook_detection(self):
        tile = Tile('A', 1)
        tile_map = TileBag().map
        board = Board(GADDAG(), tile_map)

        self.assertCountEqual(
            PlayerUtils.find_vertical_hooks(board),
            []
        )
        board.board[3][0].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_vertical_hooks(board),
            [((3, 0), tile, 3, 11)]
        )

        board.board[0][0].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_vertical_hooks(board),
            [
                ((3, 0), tile, 1, 11),
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[4][0].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_vertical_hooks(board),
            [
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[7][0].letter = tile

        self.assertCountEqual(
            PlayerUtils.find_vertical_hooks(board),
            [
                ((0, 0), tile, 0, 1),
                ((7, 0), tile, 1, 7),
            ]
        )

        board = Board(GADDAG(), tile_map)
        board.board[0][3].letter = tile
        self.assertCountEqual(
            PlayerUtils.find_vertical_hooks(board),
            [
                ((0, 3), tile, 0, 14),
            ]
        )

        board = Board(GADDAG(), tile_map)
        board.board[14][14].letter = tile
        self.assertCountEqual(
            PlayerUtils.find_horizontal_hooks(board),
            [
                ((14, 14), tile, 14, 0),
            ]
        )


if __name__ == '__main__':
    unittest.main()
