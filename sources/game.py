from data_structures.gaddag import GADDAG
from game_simulator.board import Board
from game_simulator.tile_bag import TileBag
from game_simulator.player import GreedyPlayer

NUMBER_OF_TILES = 7

def __initialize_dictionary():
    g = GADDAG()
    with open('../static/scrabble_dictionary.txt', 'r') as f:
        for line in f:
            g.add_word(line.strip('\n'))
    return g

if __name__ == '__main__':
    g = __initialize_dictionary()
    board = Board(g)
    tile_bag = TileBag()
    first_ai = AIPlayer(g)
    second_ai = AIPlayer(g)

    first_ai.add_tiles(tile_bag.draw(NUMBER_OF_TILES))
    second_ai.add_tiles(tile_bag.draw(NUMBER_OF_TILES))

    first_ai.play_first(board)
    first_ai.add_tiles(tile_bag.draw(7-len(first_ai.tiles)))
    player2_move = True
    player1_move = True
    while True:
        if not player1_move and not player2_move:
            break
        pre2 = len(second_ai.tiles)
        second_ai.play(board)
        post2 = len(second_ai.tiles)
        if pre2 == post2:
            player2_move = False
        if len(tile_bag.tiles) == 0 and len(second_ai.tiles) == 0:
            break
        second_ai.add_tiles(tile_bag.draw(7 - len(second_ai.tiles)))

        print(board.board)
        print('Player 1 Score: %d' % first_ai.score)
        print('Player 1 Score: %d' % second_ai.score)

        if not player1_move and not player2_move:
            break
        pre1 = len(first_ai.tiles)
        first_ai.play(board)
        post1 = len(second_ai.tiles)
        if pre1 == post1:
            player1_move = False
        if len(tile_bag.tiles) == 0 and len(first_ai.tiles) == 0:
            break
        first_ai.add_tiles(tile_bag.draw(7 - len(first_ai.tiles)))
        print(board.board)
        print('Player 1 Score: %d' % first_ai.score)
        print('Player 1 Score: %d' % second_ai.score)

    print('Final Results')
    print(board.board)
    print('Greedy Player 1 scored %d points.' % first_ai.score)
    print('Greedy Player 2 scored %d points.' % second_ai.score)
    print('The total points scored in the game was %d' % first_ai.score + second_ai.score)

