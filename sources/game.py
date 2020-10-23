from data_structures.gaddag import GADDAG
from game_simulator.board import Board
from game_simulator.tile_bag import TileBag
from game_simulator.player import AIPlayer


def __initialize_dictionary():
    g = GADDAG()
    with open('../static/scrabble_dictionary.txt', 'r') as f:
        for line in f:
            g.add_word(line.strip('\n'))
    return g

if __name__ == '__main__':
    board = Board()
    tile_bag = TileBag()
    g = __initialize_dictionary()
    first_ai = AIPlayer(g)
    first_ai.add_tiles(tile_bag.draw(7))
    first_ai.play_first(board)
