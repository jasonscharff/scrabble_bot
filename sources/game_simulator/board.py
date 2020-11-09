from enum import Enum
import os
import copy

class Board:

    def __init__(self, scrabble_dictionary, point_map):
        self.board = self.__initialize_board()
        self.scrabble_dictionary = scrabble_dictionary
        self.point_map = point_map
        self.played_words = set()

    def __initialize_board(self):
        board = []

        with open(os.path.join(os.path.dirname(__file__), '../static/board.txt'), 'r') as f:
            for line in f:
                board.append(list(map(lambda x: Board.Space(x), line.strip('\n').split(' '))))
        return board

    def __deepcopy__(self, memodict={}):
        new_board = Board(self.scrabble_dictionary, self.point_map)
        new_board.board = copy.deepcopy(self.board)
        new_board.played_words = self.played_words.copy()
        return new_board

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
        for word in words:
            valid = word in self.scrabble_dictionary
            if not valid:
                return False
        return True

    def points_earned_for(self, word, starting_coordinate, direction):
        score = 0
        if len(word) == 7:
            score += 50
        words = self.find_connected_words(word, starting_coordinate, direction)
        words.append((word, starting_coordinate, direction))
        for word in words:
            if word in self.played_words:
                continue
            word_score = 0
            coordinate = list(word[1])
            multiplier = 1
            for i in range(len(word[0])):
                # print(coordinate, word[0][i])
                space_type = self.board[coordinate[0]][coordinate[1]].space_type
                value = self.point_map[word[0][i]]
                if space_type == '2WS':
                    multiplier *= 2
                if space_type == '3WS':
                    multiplier *= 3
                if space_type == '2LS':
                    value *= 2
                if space_type == '3LS':
                    value *= 3
                word_score += value
                # print(word[0][i], value, space_type, type(space_type))
                if word[2] == Board.Direction.HORIZONTAL:
                    coordinate[1] += 1
                else:
                    coordinate[0] += 1
            word_score *= multiplier
            # print(word, word_score)
            score += word_score
        return score

    def find_connected_words(self, word, starting_coordinate, direction):
        # cc - abreviation of current coordinate
        cc = list(starting_coordinate)
        words = []
        if direction is Board.Direction.HORIZONTAL:
            for i in range(len(word)):
                c = [cc[0], cc[1]+i]
                w = word[i]
                start_coor = c
                for j in range(1, 15 - c[1]):
                    if c[0]+j == 15:
                        break
                    if self.board[c[0]+j][c[1]].letter is None:
                        break
                    else:
                        w += self.board[c[0]+j][c[1]].letter
                for k in range(1, c[1]):
                    if c[0]-k == 15:
                        break
                    if self.board[c[0]-k][c[1]].letter is None:
                        break
                    else:
                        w = self.board[c[0]-k][c[1]].letter + w
                        start_coor = [c[0]-k, c[1]]
                if len(w) > 1:
                    words.append((w, (start_coor[0], start_coor[1]), Board.Direction.VERTICAL))
        else:
            for i in range(len(word)):
                c = [cc[0]+i, cc[1]]
                w = word[i]
                start_coor = c
                for j in range(1, 15 - c[1]):
                    if c[1]+j == 15:
                        break
                    if self.board[c[0]][c[1] + j].letter is None:
                        break
                    else:
                        w += self.board[c[0]][c[1] + j].letter
                for k in range(1, c[0]):
                    if c[1]-k == 15:
                        break
                    if self.board[c[0]][c[1] - k].letter is None:
                        break
                    else:
                        w = self.board[c[0]][c[1] - k].letter + w
                        start_coor = [c[0], c[1] - k]
                if len(w) > 1:
                    words.append((w, (start_coor[0], start_coor[1]), Board.Direction.HORIZONTAL))
        return words

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
        words = self.find_connected_words(word, starting_coordinate, direction)
        words.append((word, starting_coordinate, direction))
        for w in words:
            self.played_words.add(w)


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

        def __copy__(self):
            return Board.Space(space_type=self.space_type, letter=self.letter)

