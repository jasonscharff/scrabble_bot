from data_structures.gaddag import GADDAG
from game_simulator.board import Board
from game_simulator.tile_bag import TileBag
from game_simulator.player import GreedyPlayer, AllKnowingPlayer, RandomPlayer
import os
NUMBER_OF_TILES = 7


def __initialize_dictionary(filepath):
    g = GADDAG()
    with open(os.path.join(os.path.dirname(__file__), filepath), 'r') as f:
        for line in f:
            g.add_word(line.strip('\n'))
    return g


def game(dictionary, first_ai, second_ai, first, second):
    tile_bag = TileBag()
    board = Board(dictionary, tile_bag.map)
    first_ai.add_tiles(tile_bag.draw(NUMBER_OF_TILES))
    second_ai.add_tiles(tile_bag.draw(NUMBER_OF_TILES))

    if p1.split(' ')[0] == 'All-knowing':
        first_ai.play_first(board, second_ai.tiles)
    else:
        first_ai.play_first(board)
    first_ai.add_tiles(tile_bag.draw(NUMBER_OF_TILES - len(first_ai.tiles)))

    player2_move = True
    player1_move = True
    while True:
        if not player1_move and not player2_move:
            break
        pre2 = len(second_ai.tiles)
        if p2.split(' ')[0] == 'All-knowing':
            second_ai.play(board, first_ai.tiles)
        else:
            second_ai.play(board)
        post2 = len(second_ai.tiles)
        if pre2 == post2:
            player2_move = False
        else:
            player2_move = True
        if len(tile_bag.tiles) == 0 and len(second_ai.tiles) == 0:
            break
        second_ai.add_tiles(tile_bag.draw(NUMBER_OF_TILES - len(second_ai.tiles)))

        if not player1_move and not player2_move:
            break
        pre1 = len(first_ai.tiles)
        if p1.split(' ')[0] == 'All-knowing':
            first_ai.play(board, second_ai.tiles)
        else:
            first_ai.play(board)
        post1 = len(first_ai.tiles)
        if pre1 == post1:
            player1_move = False
        else:
            player1_move = True
        if len(tile_bag.tiles) == 0 and len(first_ai.tiles) == 0:
            break
        first_ai.add_tiles(tile_bag.draw(7 - len(first_ai.tiles)))

    if first_ai.score > second_ai.score:
        return first
    else:
        return second


if __name__ == '__main__':
    win_counts = {}

    players = ['greedy child', 'greedy expert', 'greedy scrabble',
               'random child', 'random expert', 'random scrabble',
                'All-knowing child', 'All-knowing expert', 'All-knowing scrabble']
    completed = set()

    scrabble = __initialize_dictionary('./static/scrabble_dictionary.txt')
    print('read scrabble dictionary')
    child = __initialize_dictionary('./static/child_dictionary.txt')
    print('read child dictionary')
    expert = __initialize_dictionary('./static/expert_dictionary.txt')
    print('read expert dictionary')

    for i in range(len(players)):
        for j in range(len(players)):
            print("Matchup: {} {}".format(i, j))
            p1 = players[i]
            p2 = players[j]
            if p1 == p2:
                break
            if (p1, p2) in completed:
                break
            else:
                completed.add((p1, p2))
                completed.add((p2, p1))
            key1 = p1+' vs '+p2
            key2 = p2+' vs '+p1
            win_counts[key1] = 0
            win_counts[key2] = 0
            for _ in range(100):
                # create player 1
                if p1.split(' ')[0] == 'greedy':
                    if p1.split(' ')[1] == 'child':
                        player1 = GreedyPlayer(child)
                    if p1.split(' ')[1] == 'expert':
                        player1 = GreedyPlayer(expert)
                    if p1.split(' ')[1] == 'scrabble':
                        player1 = GreedyPlayer(scrabble)
                if p1.split(' ')[0] == 'random':
                    if p1.split(' ')[1] == 'child':
                        player1 = RandomPlayer(child)
                    if p1.split(' ')[1] == 'expert':
                        player1 = RandomPlayer(expert)
                    if p1.split(' ')[1] == 'scrabble':
                        player1 = RandomPlayer(scrabble)
                if p1.split(' ')[0] == 'All-knowing':
                    if p1.split(' ')[1] == 'child':
                        player1 = AllKnowingPlayer(child)
                    if p1.split(' ')[1] == 'expert':
                        player1 = AllKnowingPlayer(expert)
                    if p1.split(' ')[1] == 'scrabble':
                        player1 = AllKnowingPlayer(scrabble)
                # create player 2
                if p2.split(' ')[0] == 'greedy':
                    if p2.split(' ')[1] == 'child':
                        player2 = GreedyPlayer(child)
                    if p1.split(' ')[1] == 'expert':
                        player2 = GreedyPlayer(expert)
                    if p1.split(' ')[1] == 'scrabble':
                        player2 = GreedyPlayer(scrabble)
                if p2.split(' ')[0] == 'random':
                    if p2.split(' ')[1] == 'child':
                        player2 = RandomPlayer(child)
                    if p2.split(' ')[1] == 'expert':
                        player2 = RandomPlayer(expert)
                    if p2.split(' ')[1] == 'scrabble':
                        player2 = RandomPlayer(scrabble)
                if p2.split(' ')[0] == 'All-knowing':
                    if p2.split(' ')[1] == 'child':
                        player2 = AllKnowingPlayer(child)
                    if p2.split(' ')[1] == 'expert':
                        player2 = AllKnowingPlayer(expert)
                    if p2.split(' ')[1] == 'scrabble':
                        player2 = AllKnowingPlayer(scrabble)
                winner = game(scrabble, player1, player2, p1, p2)
                if winner == p1:
                    win_counts[key1] += 1
                else:
                    win_counts[key2] += 1
    for key in win_counts.keys():
        print('%s:%d' % (key, win_counts[key]))

