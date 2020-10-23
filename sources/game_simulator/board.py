from enum import Enum

class Board:

    def __init__(self):
        self.board = self.__initialize_board()

    def __initialize_board(self):
        board = []
        with open('../static/board.txt', 'r') as f:
            for line in f:
                board.append(list(map(lambda x: Board.Space(x), line.strip('\n').split(' '))))
        return board

    def __str__(self):
        all_rows = []
        if len(self.board) > 0:
            header_row = ' ' * 4 + ' '.join([str(i).zfill(3) for i in range(len(self.board[0]))])
            all_rows.append(header_row)
        for i, row in enumerate(self.board):
            row_representation = []
            for s in row:
                if s.letter is not None:
                    row_representation.append(' ' + s.letter + ' ')
                else:
                    row_representation.append(s.space_type)
            all_rows.append('{} {}'.format(str(i).zfill(3), ' '.join(row_representation)))
        return '\n'.join(all_rows)


    def is_valid_play(self, word, starting_coordinate, direction):
        return True

    def play(self, word, starting_coordinate, direction):
        pass




    class Direction(Enum):
        HORIZONTAL = 0
        VERTICAL = 1

    class Space:

        class SpaceType(Enum):
            REGULAR = 'RES'
            DOUBLE_LETTER = '2LS'
            TRIPLE_LETTER = '3LS'
            DOUBLE_WORD = '2WS'
            TRIPLE_WORD = '3WS'

        def __init__(self, space_type=SpaceType.REGULAR, letter=None):
            self.space_type = space_type
            self.letter = letter


if __name__ == '__main__':
    b = Board()
    print(b)