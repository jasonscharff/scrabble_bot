from abc import ABC
from .board import Board
from .player_utils import PlayerUtils
import random
import copy

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
    

class AllKnowingPlayer(Player):

    def __init__(self, scrabble_dictionary):
        super().__init__()
        self.scrabble_dictionary = scrabble_dictionary


    def play_first(self, board, opponent_rack):
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

        if not all_moves:
            return

        best_move, points_earned, delta = self.identify_lowest_delta_move(board, all_moves, opponent_rack)
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

    def play(self, board, opponent_rack):
        all_moves = PlayerUtils.identify_all_moves(board=board,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, self.tiles)))
        if len(all_moves) == 0:
            return

        best_move, points_earned, delta = self.identify_lowest_delta_move(board, all_moves, opponent_rack)
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

    def identify_lowest_delta_move(self, board, all_moves, opponent_rack):
        scored_moves = sorted(PlayerUtils.score_moves(board, moves=all_moves), key=lambda x: x[1], reverse=True)

        #only look at top 25 greedy moves
        if len(scored_moves) > 25:
            scored_moves = scored_moves[:25]

        optimal_moves = []
        opponent_rack_letters = list(map(lambda x: x.letter, opponent_rack))

        for move, score in scored_moves:
            temp_board = copy.deepcopy(board)
            temp_board.play(
                word=move.word,
                starting_coordinate=move.starting_coordinate,
                direction=move.direction
            )
            opponents_moves = PlayerUtils.identify_all_moves(board=temp_board,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=opponent_rack_letters)

            opponents_scored_moves = PlayerUtils.score_moves(temp_board, moves=opponents_moves)
            if opponents_scored_moves:
                _, opponents_response_score = max(opponents_scored_moves, key=lambda x: x[1])
            else:
                opponents_response_score = 0

            optimal_moves.append((move, score, score - opponents_response_score))

        return max(optimal_moves, key=lambda x: x[2])

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

