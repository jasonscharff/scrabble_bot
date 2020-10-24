import unittest
from .player import GreedyPlayer
from .board import Board
from ..data_structures.gaddag import GADDAG
from .tile_bag import Tile

class PlayerTests(unittest.TestCase):
    def test_greedy_horizontal_hook_detection(self):
        tile = Tile('A', 1)
        player = GreedyPlayer(GADDAG())
        board = Board()

        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            []
        )
        board.board[0][3].letter = tile

        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            [((0,3), tile, 3, 11)]
        )

        board.board[0][0].letter = tile

        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            [
                ((0,3), tile, 1, 11),
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[0][4].letter = tile

        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            [
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[0][7].letter = tile

        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            [
                ((0, 0), tile, 0, 1),
                ((0, 7), tile, 1, 7),
            ]
        )

        board = Board()
        board.board[3][0].letter = tile
        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            [
                ((3, 0), tile, 0, 14),
            ]
        )

        board = Board()
        board.board[14][14].letter = tile
        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            [
                ((14, 14), tile, 14, 0),
            ]
        )

    def test_greedy_vertical_hook_detection(self):
        tile = Tile('A', 1)
        player = GreedyPlayer(GADDAG())
        board = Board()

        self.assertCountEqual(
            player.find_vertical_hooks(board),
            []
        )
        board.board[3][0].letter = tile

        self.assertCountEqual(
            player.find_vertical_hooks(board),
            [((3, 0), tile, 3, 11)]
        )

        board.board[0][0].letter = tile

        self.assertCountEqual(
            player.find_vertical_hooks(board),
            [
                ((3, 0), tile, 1, 11),
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[4][0].letter = tile

        self.assertCountEqual(
            player.find_vertical_hooks(board),
            [
                ((0, 0), tile, 0, 1)
            ]
        )

        board.board[7][0].letter = tile

        self.assertCountEqual(
            player.find_vertical_hooks(board),
            [
                ((0, 0), tile, 0, 1),
                ((7, 0), tile, 1, 7),
            ]
        )


        board = Board()
        board.board[0][3].letter = tile
        self.assertCountEqual(
            player.find_vertical_hooks(board),
            [
                ((0, 3), tile, 0, 14),
            ]
        )

        board = Board()
        board.board[14][14].letter = tile
        self.assertCountEqual(
            player.find_horizontal_hooks(board),
            [
                ((14, 14), tile, 14, 0),
            ]
        )


if __name__ == '__main__':
    unittest.main()
