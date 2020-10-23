from data_structures.gaddag import GADDAG
from game_simulator.board import Board
from game_simulator.tile_bag import TileBag


def __initialize_dictionary():
    g = GADDAG()
    with open('../static/scrabble_dictionary.txt', 'r') as f:
        for line in f:
            g.add_word(line.strip('\n'))
    return g

if __name__ == '__main__':
    b = Board()
    tile_bag = TileBag()
    g = __initialize_dictionary()
