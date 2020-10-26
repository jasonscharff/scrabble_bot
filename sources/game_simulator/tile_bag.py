import random
import os

class Tile:

    def __init__(self, letter, point_value):
        self.letter = letter
        self.point_value = point_value

    def __str__(self):
        return self.letter

    def __eq__(self, other):
        return self.letter == other.letter and self.point_value == other.point_value


class TileBag:

    def __init__(self):
        self.tiles = self.__generate_tiles()
        self.map = self.__make_map()

    def draw(self, number):
        return [self.tiles.pop() for _ in range(number)]

    def __generate_tiles(self):
        all_tiles = []
        with open(os.path.join(os.path.dirname(__file__), '../static/tiles.txt'), 'r') as f:
            for line in f:
                count, letter, value = line.strip('\n').split(' ')
                all_tiles += [Tile(letter, int(value)) for _ in range(int(count))]

        random.shuffle(all_tiles)
        return all_tiles

    def __make_map(self):
        letter_point_map = {}
        with open(os.path.join(os.path.dirname(__file__), '../static/tiles.txt'), 'r') as f:
            for line in f:
                count, letter, value = line.strip('\n').split(' ')
                letter_point_map[letter] = int(value)
        return letter_point_map
