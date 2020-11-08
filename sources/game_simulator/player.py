from abc import ABC
from .board import Board
from .player_utils import PlayerUtils
import random

class Player(ABC):

    def __init__(self):
        self.score = 0
        self.tiles = []

    def add_tiles(self, tiles):
        self.tiles += tiles

    def finalize_move(self, board, move, points_earned):
        board.play(word=move.word,
                   starting_coordinate=move.starting_coordinate,
                   direction=move.direction)

        self.score += points_earned
        for letter in move.word:
            for tile in self.tiles:
                if tile.letter == letter:
                    self.tiles.remove(tile)
                    break

class GreedyPlayer(Player):

    def __init__(self, scrabble_dictionary):
        super().__init__()
        self.scrabble_dictionary = scrabble_dictionary


    def play_first(self, board):
        middle_spot = len(board.board) // 2
        rack = list(map(lambda x: x.letter, self.tiles))

        all_moves = []
        for direction in [Board.Direction.HORIZONTAL, Board.Direction.VERTICAL]:
            all_moves += PlayerUtils.identify_moves_from_hook(
                scrabble_dictionary=self.scrabble_dictionary,
                board=board, rack=rack,
                hook_letter=None,
                hook_coordinates=(middle_spot, middle_spot),
                prefix_length=len(board.board) - middle_spot,
                suffix_length=len(board.board) - middle_spot,
                direction=direction
            )

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = max(scored_moves, key=lambda x: x[1])
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

    def play(self, board):
        all_moves = PlayerUtils.identify_all_moves(board=board,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, self.tiles)))

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = max(scored_moves, key=lambda x: x[1])
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

class RandomPlayer(Player):

    def __init__(self, scrabble_dictionary):
        super().__init__()
        self.scrabble_dictionary = scrabble_dictionary


    def play_first(self, board):
        middle_spot = len(board.board) // 2
        rack = list(map(lambda x: x.letter, self.tiles))

        all_moves = []
        for direction in [Board.Direction.HORIZONTAL, Board.Direction.VERTICAL]:
            all_moves += PlayerUtils.identify_moves_from_hook(
                scrabble_dictionary=self.scrabble_dictionary,
                board=board, rack=rack,
                hook_letter=None,
                hook_coordinates=(middle_spot, middle_spot),
                prefix_length=len(board.board) - middle_spot,
                suffix_length=len(board.board) - middle_spot,
                direction=direction
            )

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = random.choice(scored_moves)
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

    def play(self, board):
        all_moves = PlayerUtils.identify_all_moves(board=board,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, self.tiles)))

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = random.choice(scored_moves)
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

