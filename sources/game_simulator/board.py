from enum import Enum
import os

class Board:

    def __init__(self, scrabble_dictionary, point_map):
        self.board = self.__initialize_board()
        self.scrabble_dictionary = scrabble_dictionary
        self.point_map = point_map

    def __initialize_board(self):
        board = []

        with open(os.path.join(os.path.dirname(__file__), '../static/board.txt'), 'r') as f:
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
        # words = self.find_connected_words(word, starting_coordinate, direction)
        print(word)
        words = []
        dont_remove = set()
        # add to board
        cc = list(starting_coordinate)
        for i in range(len(word)):
            if self.board[cc[0]][cc[1]].letter is None:
                self.board[cc[0]][cc[1]].letter = word[i]
            else:
                dont_remove.add((cc[0], cc[1]))
            if direction is Board.Direction.HORIZONTAL:
                cc[1] += 1
            else:
                cc[0] += 1
        # check if board is valid
        # scan rows
        for i in range(15):
            w = ''
            for j in range(15):
                if self.board[i][j].letter is not None:
                    w += self.board[i][j].letter
                if self.board[i][j].letter is None:
                    if len(w) > 1:
                        words.append(w)
                        w = ''
                    else:
                        continue
            if len(w) > 1:
                words.append(w)
        # scan columns
        for i in range(15):
            w = ''
            for j in range(15):
                if self.board[j][i].letter is not None:
                    w += self.board[j][i].letter
                if self.board[j][i].letter is None:
                    if len(w) > 1:
                        words.append(w)
                        w = ''
                    else:
                        continue
            if len(w) > 1:
                words.append(w)
        # remove word from board
        cc = list(starting_coordinate)
        for i in range(len(word)):
            if (cc[0], cc[1]) in dont_remove:
                if direction is Board.Direction.HORIZONTAL:
                    cc[1] += 1
                else:
                    cc[0] += 1
                continue
            else:
                self.board[cc[0]][cc[1]].letter = None
            if direction is Board.Direction.HORIZONTAL:
                cc[1] += 1
            else:
                cc[0] += 1
        print(self)
        print('words variable:')
        print(words)
        for word in words:
            print(word)
            print(type(word))
            valid = word in self.scrabble_dictionary
            print(valid)
            if not valid:
                return False
        return True

    def points_earned_for(self, word, starting_coordinate, direction):
        score = 0
        words = self.find_connected_words(word, starting_coordinate, direction)
        words.append((word, starting_coordinate, direction))
        for word in words:
            word_score = 0
            coordinate = list(word[1])
            multiplier = 1
            for i in range(len(word[0])):
                space_type = self.board[coordinate[0]][coordinate[1]].space_type
                value = self.point_map[word[0][i]]
                if space_type is Board.Space.SpaceType.DOUBLE_WORD:
                    multiplier *= 2
                if space_type is Board.Space.SpaceType.TRIPLE_WORD:
                    multiplier *= 3
                if space_type is Board.Space.SpaceType.DOUBLE_LETTER:
                    value *= 2
                if space_type is Board.Space.SpaceType.TRIPLE_LETTER:
                    value *= 3
                word_score += value
                if direction == Board.Direction.HORIZONTAL:
                    coordinate[1] += 1
                else:
                    coordinate[0] += 1
            word_score *= multiplier
            score += word_score
        if len(word) == 7:
            score += 50
        return score

    def find_connected_words(self, word, starting_coordinate, direction):
        # cc - abreviation of current coordinate
        cc = list(starting_coordinate)
        words = []
        word_index = 0
        if direction is Board.Direction.HORIZONTAL:
            # check 3 spaces around first letter left, up, down
            if cc[0] < 14 and self.board[cc[0]+1][cc[1]].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0]+1, cc[1]]))
            if cc[0] > 0 and self.board[cc[0]-1][cc[1]].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0]-1, cc[1]]))
            if cc[1] > 0 and self.board[cc[0]][cc[1]-1].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0], cc[1]-1]))
            cc[1] += 1
            word_index += 1
            for i in range(1, len(word) - 1):
                # check 2 spaces around middle letters up, down
                if cc[0] < 14 and self.board[cc[0]+1][cc[1]].letter is not None:
                    words.extend(self.find_words(word, word_index, [cc[0]+1, cc[1]]))
                if cc[0] > 0 and self.board[cc[0]-1][cc[1]].letter is not None:
                    words.extend(self.find_words(word, word_index, [cc[0]-1, cc[1]]))
                cc[1] += 1
                word_index += 1
            # check 3 spaces around last letter right, up, down
            if cc[0] < 14 and self.board[cc[0]+1][cc[1]].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0]+1, cc[1]]))
            if cc[0] > 0 and self.board[cc[0]-1][cc[1]].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0]-1, cc[1]]))
            if cc[1] < 14 and self.board[cc[0]][cc[1]+1].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0], cc[1]+1]))
        else:
            # check 3 spaces around first letter up, left, right
            if cc[1] < 14 and self.board[cc[0]][cc[1]+1].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0], cc[1]+1]))
            if cc[1] > 0 and self.board[cc[0]][cc[1]-1].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0], cc[1]-1]))
            if cc[0] > 0 and self.board[cc[0]-1][cc[1]].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0]-1, cc[1]]))
            cc[0] += 1
            word_index += 1
            for i in range(1, len(word) - 1):
                # check 2 spaces around middle letters left, right
                if cc[1] < 14 and self.board[cc[0]][cc[1]+1].letter is not None:
                    words.extend(self.find_words(word, word_index, [cc[0], cc[1]+1]))
                if cc[1] > 0 and self.board[cc[0]][cc[1]-1].letter is not None:
                    words.extend(self.find_words(word, word_index, [cc[0], cc[1]-1]))
                cc[0] += 1
                word_index += 1
            # check 3 spaces around last letter down, right, left
            if cc[1] < 14 and self.board[cc[0]][cc[1]+1].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0], cc[1]+1]))
            if cc[1] > 0 and self.board[cc[0]][cc[1]-1].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0], cc[1]-1]))
            if cc[0] < 14 and self.board[cc[0]+1][cc[1]].letter is not None:
                words.extend(self.find_words(word, word_index, [cc[0]+1, cc[1]]))
        s = set(words)
        words = list(s)
        print(words)
        return words

    def find_words(self, word, word_index, starting_coordinate):
        cc = list(starting_coordinate)
        vertical = word[word_index]
        horizontal = word[word_index]
        vertical_start = []
        horizontal_start = []
        while self.board[cc[0]+1][cc[1]].letter:
            vertical = self.board[cc[0]+1][cc[1]].letter + vertical
            cc[0] += 1
        cc = starting_coordinate
        while self.board[cc[0]-1][cc[1]].letter:
            vertical = vertical + self.board[cc[0]-1][cc[1]].letter
            cc[0] -= 1
            vertical_start = cc
        cc = starting_coordinate
        while self.board[cc[0]][cc[1]+1].letter:
            horizontal = horizontal + self.board[cc[0]][cc[1]+1].letter
            cc[1] += 1
        cc = starting_coordinate
        while self.board[cc[0]][cc[1]-1].letter:
            horizontal = self.board[cc[0]][cc[1]-1].letter + horizontal
            cc[0] -= 1
            horizontal_start = cc
        ret = []
        if len(vertical) > 1:
            ret.append((vertical, tuple(vertical_start), 0))
        if len(horizontal) > 1:
            ret.append((horizontal, tuple(horizontal_start), 1))
        return ret

    def play(self, word, starting_coordinate, direction):
        # just add word to board
        cc = list(starting_coordinate)
        for i in range(len(word)):
            self.board[cc[0]][cc[1]].letter = word[i]
            self.board[cc[0]][cc[1]].space_type = Board.Space.SpaceType.REGULAR
            if direction is Board.Direction.HORIZONTAL:
                cc[1] += 1
            else:
                cc[0] += 1

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

