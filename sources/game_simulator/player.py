from abc import ABC
from .board import Board

class Player(ABC):

    def __init__(self):
        self.score = 0
        self.tiles = []

    def add_tiles(self, tiles):
        self.tiles += tiles

    def play(self, current_board):
        pass

class AIPlayer(Player):

    def __init__(self, scrabble_dictionary):
        super().__init__()
        self.scrabble_dictionary = scrabble_dictionary


    def play_first(self, board):
        middle_spot = len(board.board) // 2 + 1
        rack = list(map(lambda x: x.letter, self.tiles))
        options = self.scrabble_dictionary.find_matches(
            hook=None,
            rack=rack,
            available_prefix_spaces=len(board.board) - middle_spot,
            available_suffix_spaces=len(board.board) - middle_spot
        )
        available_moves = []
        for prefix, suffix in options:
            word = prefix + suffix
            vertical_move = (word, (middle_spot, middle_spot - len(prefix)), Board.Direction.VERTICAL)
            horizontal_move = (word, (middle_spot - len(prefix)), Board.Direction.HORIZONTAL)
            available_moves.append(
                (
                    vertical_move,
                    board.points_earned_for(vertical_move[0], vertical_move[1], vertical_move[2])
                 )
            )
            available_moves.append(
                (
                    horizontal_move,
                    board.points_earned_for(horizontal_move[0], horizontal_move[1], horizontal_move[2])
                 )
            )
        best_move, points_earned = max(available_moves, key=lambda x: x[1])
        board.play(best_move[0], best_move[1], best_move[2])

    def play(self, board):
        rack = list(map(lambda x: x.letter, self.tiles))
        available_moves = []

        #first let's check horizontally
        for y, row in enumerate(board.board):
            previous_letter_index = 0
            current_prefix_count = 0
            hook = None
            for x, space in enumerate(board.board[y]):
                if space.letter is not None:
                    if hook is not None:
                        available_moves += self.__evaluate_moves(
                            board=board,
                            rack=rack,
                            hook=hook,
                            prefix_length=current_prefix_count,
                            suffix_length=len(board.board) - x - previous_letter_index - 1
                        )

                    current_prefix_count = x - previous_letter_index - 1
                    hook = ((x, y), space.letter)

            if hook is not None:
                available_moves += self.__evaluate_moves(
                    board=board,
                    rack=rack,
                    hook=hook,
                    prefix_length=current_prefix_count,
                    suffix_length=len(board.board) - x - previous_letter_index - 1,
                    direction=Board.Direction.HORIZONTAL
                )

        #now we check vertically using the same logic
        for x in range(board.board[0]):
            previous_letter_index = 0
            current_prefix_count = 0
            hook = None
            for y in range(board.board):
                space = board.board[x][y]
                if space.letter is not None:
                    if hook is not None:
                        available_moves += self.__evaluate_moves(
                            board=board,
                            rack=rack,
                            hook=hook,
                            prefix_length=current_prefix_count,
                            suffix_length=len(board.board) - x - previous_letter_index - 1,
                            direction=Board.Direction.VERTICAL
                        )

                    current_prefix_count = x - previous_letter_index - 1
                    hook = ((x, y), space.letter)

        best_move, points_earned = max(available_moves, key=lambda x: x[1])
        board.play(best_move[0], best_move[1], best_move[2])

    def __evaluate_moves(self, board, rack, hook, prefix_length, suffix_length, direction):
        available_moves = []

        options = self.scrabble_dictionary.find_matches(
            hook=hook[1],
            rack=rack,
            available_prefix_spaces=prefix_length,
            available_suffix_spaces=suffix_length
        )
        for prefix, suffix in options:
            word = prefix + hook + suffix
            if direction == Board.Direction.HORIZONTAL:
                move = (word, (hook[0][0] - len(prefix), hook[0][1]), Board.Direction.HORIZONTAL)
            else:
                move = (word, (hook[0][0], hook[0][1] - - len(prefix)), Board.Direction.VERTICAL)

            if board.is_valid_play(move[0], move[1], move[2]):
                available_moves.append(
                    (
                        move,
                        board.points_earned_for(move[0], move[1], move[2])
                    )
                )

        return available_moves






'''
#first go through each row
        for row in current_board.board:
            spaces_with_tiles = []
            for index, space in enumerate(row):
                if space.letter is not None:
                    spaces_with_tiles.append((index, space.letter))
            for index, space in enumerate(spaces_with_tiles):
                space_index, space_letter = space
                if index == 0:
                    left_space = space_index
                else:
                    left_space = space_index - spaces_with_tiles[index-1][0]
                if index == len(spaces_with_tiles) - 1:
                    right_space = len(row) - space_index - 1
                else:
                    right_space = spaces_with_tiles[index + 1][0] - space_index

                word_options = g.find_matches(space_letter, self.words, left_space, right_space)
                #we need to now calculate scores for these
'''




