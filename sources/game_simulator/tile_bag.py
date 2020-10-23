import random

class Tile:

    def __init__(self, letter, point_value):
        self.letter = letter
        self.point_value = point_value

    def __str__(self):
        return self.letter


class TileBag:

    def __init__(self):
        self.tiles = self.__generate_tiles()

    def draw(self, number):
        return self.tiles.pop(number)

    def __generate_tiles(self):
        all_tiles = []
        with open('../static/tiles.txt', 'r') as f:
            for line in f:
                count, letter, value = line.strip('\n').split(' ')
                all_tiles += [Tile(letter, int(value)) for _ in range(int(count))]

        random.shuffle(all_tiles)
        return all_tiles

