from data_structures.gaddag import GADDAG
from game_simulator.board import Board
from game_simulator.tile_bag import TileBag
from game_simulator.player import GreedyPlayer
import os


def __initialize_dictionary(filepath):
    g = GADDAG()
    with open(os.path.join(os.path.dirname(__file__), filepath), 'r') as f:
        for line in f:
            g.add_word(line.strip('\n'))
    return g


if __name__ == '__main__':
    score_matrix = [[0, 0, 0, 0, 0, 0] for _ in range(6)]
    for i in range(6):
        for j in range(6):
            if i == j:
                score_matrix[i][j] = 'NA'
    # abridged = __initialize_dictionary('')
    scrabble = __initialize_dictionary('./static/scrabble_dictionary.txt')
    tile_bag = TileBag()
    # a_board = Board(abridged, tile_bag.map)
    s_board = Board(scrabble, tile_bag.map)
    # greedy_abridged = GreedyPlayer(abridged)
    greedy_scrabble = GreedyPlayer(scrabble)
    # initialize other players here 
    # run games and fill in table here
