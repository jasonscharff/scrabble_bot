from collections import namedtuple
from .board import Board


class PlayerUtils:

    Hook = namedtuple('Hook', 'coordinates letter prefix_length suffix_length')
    Move = namedtuple("Move", 'word starting_coordinate direction')

    @staticmethod
    def identify_all_moves(board, scrabble_dictionary, rack):
        all_hooks = (
            (Board.Direction.HORIZONTAL, PlayerUtils.find_horizontal_hooks(board)),
            (Board.Direction.VERTICAL, PlayerUtils.find_vertical_hooks(board)),
        )

        moves = []

        for direction, hooks in all_hooks:
            for hook in hooks:
                moves += PlayerUtils.identify_moves_from_hook(
                    scrabble_dictionary=scrabble_dictionary,
                    board=board,
                    rack=rack,
                    hook_letter=hook.letter,
                    hook_coordinates=hook.coordinates,
                    prefix_length=hook.prefix_length,
                    suffix_length=hook.suffix_length,
                    direction=direction
                )

        return moves

    @staticmethod
    def find_horizontal_hooks(board):
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
                        if current_prefix_count >= 0 and suffix_count >= 0 and (
                                current_prefix_count > 0 or suffix_count > 0):
                            hooks.append(
                                PlayerUtils.Hook(hook_coordinates, hook_letter, current_prefix_count, suffix_count)
                            )
                    current_prefix_count = y - previous_letter_index - 2
                    previous_letter_index = y
                    hook_coordinates, hook_letter = (x, y), space.letter
            y += 1
            if hook_coordinates is not None:
                suffix_count = y - previous_letter_index - 1
                if current_prefix_count >= 0 and suffix_count >= 0 and (current_prefix_count > 0 or suffix_count > 0):
                    hooks.append(PlayerUtils.Hook(hook_coordinates, hook_letter, current_prefix_count, suffix_count))
        return hooks

    @staticmethod
    def find_vertical_hooks(board):
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
                                PlayerUtils.Hook(hook_coordinates, hook_letter, current_prefix_count, suffix_count)
                            )
                    current_prefix_count = x - previous_letter_index - 2
                    previous_letter_index = x
                    hook_coordinates, hook_letter = (x, y), space.letter
            x += 1
            if hook_coordinates is not None:
                suffix_count = x - previous_letter_index - 1
                if current_prefix_count >= 0 and suffix_count >= 0 and (current_prefix_count > 0 or suffix_count > 0):
                    hooks.append(PlayerUtils.Hook(hook_coordinates, hook_letter, current_prefix_count, suffix_count))
        return hooks

    @staticmethod
    def identify_moves_from_hook(scrabble_dictionary,
                                 board,
                                 rack,
                                 hook_letter,
                                 hook_coordinates,
                                 prefix_length,
                                 suffix_length,
                                 direction):
        available_moves = []
        options = scrabble_dictionary.find_matches(
            hook=hook_letter,
            rack=rack,
            available_prefix_spaces=prefix_length,
            available_suffix_spaces=suffix_length
        )
        for prefix, suffix in options:
            word = prefix + hook_letter if hook_letter is not None else '' + suffix
            if direction == Board.Direction.HORIZONTAL:
                move = PlayerUtils.Move(word, (hook_coordinates[0], hook_coordinates[1] - len(prefix)), Board.Direction.HORIZONTAL)
            else:
                move = PlayerUtils.Move(word, (hook_coordinates[0] - len(prefix), hook_coordinates[1]), Board.Direction.VERTICAL)

            if board.is_valid_play(word=move.word, starting_coordinate=move.starting_coordinate, direction=move.direction):
                available_moves.append(move)

        return available_moves

    @staticmethod
    def score_moves(board, moves):
        return list(
            map(
                lambda m: (
                    m,
                    board.points_earned_for(
                        word=m.word,
                        starting_coordinate=m.starting_coordinate,
                        direction=m.direction
                    ),
                ),
                moves
            )
        )