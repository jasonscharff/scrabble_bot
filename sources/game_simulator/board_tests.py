import unittest
from .board import Board
from ..data_structures.gaddag import GADDAG
from .tile_bag import TileBag


class MyTestCase(unittest.TestCase):
    # def test_scoring(self):
    #     g = GADDAG()
    #     tile_bag = TileBag()
    #     board = Board(g, tile_bag.map)
    #
    #     self.assertEqual(board.points_earned_for('CONNECT', (4, 4), Board.Direction.VERTICAL), 94)
    #     self.assertEqual(board.points_earned_for('EQUAL', (3, 0), Board.Direction.VERTICAL), 30)
    #     self.assertEqual(board.points_earned_for('BAT', (0, 0), Board.Direction.HORIZONTAL), 11)
    #
    #     board.board[7][7].letter = 'V'
    #     board.board[8][7].letter = 'O'
    #     board.board[9][7].letter = 'T'
    #     board.board[10][7].letter = 'E'
    #     self.assertEqual(board.points_earned_for('SAY', (11, 7), Board.Direction.HORIZONTAL), 16)
    #     self.assertEqual(board.points_earned_for('SI', (8, 6), Board.Direction.VERTICAL), 8)
    #
    #     board.board[11][7].letter = 'S'
    #     board.board[11][8].letter = 'A'
    #     board.board[11][9].letter = 'Y'
    #     self.assertEqual(board.points_earned_for('HOSE', (12, 8), Board.Direction.HORIZONTAL), 25)


    def test_validation(self):
        g = GADDAG()
        tile_bag = TileBag()
        board = Board(g, tile_bag.map)
        self.assertEqual(board.is_valid_play('HAPPY', (7, 7), Board.Direction.HORIZONTAL), True)
        # self.assertEqual(board.find_connected_words('HAPPY', (7, 7), Board.Direction.HORIZONTAL), [])
        board.board[7][7].letter = 'H'
        board.board[7][8].letter = 'A'
        board.board[7][9].letter = 'P'
        board.board[7][10].letter = 'P'
        board.board[7][11].letter = 'Y'
        self.assertEqual(board.is_valid_play('PILL', (7, 10), Board.Direction.VERTICAL), True)
        # self.assertEqual(board.find_connected_words('PILL', (7, 9), Board.Direction.VERTICAL), ['HAPPY'])

        self.assertEqual(board.is_valid_play('ZIP', (8, 7), Board.Direction.HORIZONTAL), False)
        # self.assertEqual(board.find_connected_words('ZIP', (8, 7), Board.Direction.HORIZONTAL), ['HZ', 'AI', 'PP'])

        self.assertEqual(board.is_valid_play('OH', (6, 7), Board.Direction.HORIZONTAL), True)
        # self.assertEqual(board.find_connected_words('OH', (6, 7), Board.Direction.HORIZONTAL), ['OH', 'HA'])

        board.board[8][10].letter = 'I'
        board.board[9][10].letter = 'L'
        board.board[10][10].letter = 'L'

        board.board[5][11].letter = 'J'
        board.board[6][11].letter = 'O'

        self.assertEqual(board.is_valid_play('SOD', (6, 10), Board.Direction.HORIZONTAL), True)
        # self.assertEqual(board.find_connected_words('SOD', (6, 10), Board.Direction.HORIZONTAL),['SPILL', 'JOY', 'HAPPY'])

        self.assertEqual(board.is_valid_play('DO', (6, 10), Board.Direction.HORIZONTAL), False)
        # self.assertEqual(board.find_connected_words('DO', (6, 10), Board.Direction.HORIZONTAL), ['DPILL', 'JOY', 'HAPPY'])


    # def test_play(self):
    #     g = GADDAG()
    #     tile_bag = TileBag()
    #     board = Board(g, tile_bag.map)
    #     board1 = Board(g, tile_bag.map)
    #     board1.board[0][0].letter = 'H'
    #     board1.board[1][0].letter = 'E'
    #     board1.board[2][0].letter = 'Y'
    #
    #     self.assertEqual(board.play('HEY', (0, 0), Board.Direction.VERTICAL), board1)
    #
    #     board1.board[0][1].letter = 'E'
    #     board1.board[0][2].letter = 'Y'
    #     self.assertEqual(board.play('HEY', (0, 0), Board.Direction.HORIZONTAL), board1)




if __name__ == '__main__':
    unittest.main()
