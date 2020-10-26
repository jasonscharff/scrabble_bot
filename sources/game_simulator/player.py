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

class GreedyPlayer(Player):

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
            horizontal_move = (word, (middle_spot - len(prefix), middle_spot), Board.Direction.HORIZONTAL)
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
        print(available_moves)
        best_move, points_earned = max(available_moves, key=lambda x: x[1])
        board.play(best_move[0], best_move[1], best_move[2])
        self.score += points_earned
        print('word played: %s' % best_move[0])
        for letter in best_move[0]:
            for tile in self.tiles:
                if tile.letter == letter:
                    self.tiles.remove(tile)
                    break


    def find_horizontal_hooks(self, board):
        hooks = []

        for x, row in enumerate(board.board):
            previous_letter_index = -2
            current_prefix_count = 0
            hook_coordinates = None
            hook_letter = None
            for y, space in enumerate(board.board[x]):
                if space.letter is not None:
                    if hook_coordinates is not None:
                        suffix_count = y - previous_letter_index - 2
                        if current_prefix_count >= 0 and suffix_count >= 0 and (current_prefix_count > 0 or suffix_count > 0):
                            hooks.append(
                                (hook_coordinates, hook_letter, current_prefix_count, suffix_count)
                            )
                    current_prefix_count = y - previous_letter_index - 2
                    previous_letter_index = y
                    hook_coordinates, hook_letter = (x, y), space.letter
            y += 1
            if hook_coordinates is not None:
                suffix_count = y - previous_letter_index - 1
                if current_prefix_count >= 0 and suffix_count >= 0 and (current_prefix_count > 0 or suffix_count > 0):
                    hooks.append(
                        (hook_coordinates, hook_letter, current_prefix_count, suffix_count)
                    )
        return hooks

    def find_vertical_hooks(self, board):
        hooks = []
        for y in range(len(board.board[0])):
            previous_letter_index = -2
            current_prefix_count = 0
            hook_coordinates = None
            hook_letter = None
            for x in range(len(board.board)):
                space = board.board[x][y]
                if space.letter is not None:
                    if hook_coordinates is not None:
                        suffix_count = x - previous_letter_index - 2
                        if current_prefix_count >= 0 and suffix_count >= 0 and (
                                current_prefix_count > 0 or suffix_count > 0):
                            hooks.append(
                                (hook_coordinates, hook_letter, current_prefix_count, suffix_count)
                            )
                    current_prefix_count = x - previous_letter_index - 2
                    previous_letter_index = x
                    hook_coordinates, hook_letter = (x, y), space.letter
            x += 1
            if hook_coordinates is not None:
                suffix_count = x - previous_letter_index - 1
                if current_prefix_count >= 0 and suffix_count >= 0 and (current_prefix_count > 0 or suffix_count > 0):
                    hooks.append(
                        (hook_coordinates, hook_letter, current_prefix_count, suffix_count)
                    )
        return hooks

    def play(self, board):
        rack = list(map(lambda x: x.letter, self.tiles))
        available_moves = []
        available_horizontal_moves = self.find_horizontal_hooks(board)
        available_vertical_moves = self.find_vertical_hooks(board)
        for hook_coordinates, hook_letter, prefix_count, suffix_count in available_horizontal_moves:
            available_moves.append(
                self.__evaluate_moves(
                    board=board,
                    rack=rack,
                    hook_letter=hook_letter,
                    hook_coordinates=hook_coordinates,
                    prefix_length=prefix_count,
                    suffix_length=suffix_count,
                    direction=Board.Direction.HORIZONTAL
                )
            )

        for hook_coordinates, hook_letter, prefix_count, suffix_count in available_vertical_moves:
            available_moves.append(
                self.__evaluate_moves(
                    board=board,
                    rack=rack,
                    hook_letter=hook_letter,
                    hook_coordinates=hook_coordinates,
                    prefix_length=prefix_count,
                    suffix_length=suffix_count,
                    direction=Board.Direction.VERTICAL
                )
            )
        print(available_moves)
        best_move, points_earned = max(available_moves, key=lambda x: x[1])
        board.play(best_move[0], best_move[1], best_move[2])
        self.score += points_earned
        print('word played: %s' % best_move[0])
        for letter in best_move[0]:
            for tile in self.tiles:
                if tile.letter == letter:
                    self.tiles.remove(tile)
                    break

    def __evaluate_moves(self, board, rack, hook_letter, hook_coordinates, prefix_length, suffix_length, direction):
        available_moves = []

        options = self.scrabble_dictionary.find_matches(
            hook=hook_letter,
            rack=rack,
            available_prefix_spaces=prefix_length,
            available_suffix_spaces=suffix_length
        )
        for prefix, suffix in options:
            word = prefix + hook_letter + suffix
            if direction == Board.Direction.HORIZONTAL:
                move = (word, (hook_coordinates[0], hook_coordinates[1] - len(prefix)), Board.Direction.HORIZONTAL)
            else:
                move = (word, (hook_coordinates[0] - len(prefix), hook_coordinates[1]), Board.Direction.VERTICAL)

            if board.is_valid_play(move[0], move[1], move[2]):
                available_moves.append(
                    (
                        move,
                        board.points_earned_for(move[0], move[1], move[2])
                    )
                )

        return available_moves