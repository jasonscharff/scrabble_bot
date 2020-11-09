from abc import ABC
from .board import Board
from .player_utils import PlayerUtils
import random

class Player(ABC):

    def __init__(self):
        self.score = 0
        self.tiles = []

    def add_tiles(self, tiles):
        self.tiles += tiles

    def finalize_move(self, board, move, points_earned):
        board.play(word=move.word,
                   starting_coordinate=move.starting_coordinate,
                   direction=move.direction)

        self.score += points_earned
        for letter in move.word:
            for tile in self.tiles:
                if tile.letter == letter:
                    self.tiles.remove(tile)
                    break
    def perdict_move(self, board, move):
        board.play(word=move.word,
                   starting_coordinate=move.starting_coordinate,
                   direction=move.direction)
    

class AllKnowingPlayer(Player):

    def __init__(self, scrabble_dictionary):
        super().__init__()
        self.scrabble_dictionary = scrabble_dictionary


    def play_first(self, board, opponentRack):
        middle_spot = len(board.board) // 2
        rack = list(map(lambda x: x.letter, self.tiles))

        all_moves = []
        for direction in [Board.Direction.HORIZONTAL, Board.Direction.VERTICAL]:
            all_moves += PlayerUtils.identify_moves_from_hook(
                scrabble_dictionary=self.scrabble_dictionary,
                board=board, rack=rack,
                hook_letter=None,
                hook_coordinates=(middle_spot, middle_spot),
                prefix_length=len(board.board) - middle_spot,
                suffix_length=len(board.board) - middle_spot,
                direction=direction
            )

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)
        
        if len(scored_moves) == 0:
            return
        
        sorted_moves = sorted(scored_moves, key = lambda x: x[1])
        
        i =  len(sorted_moves)-1
        min = 100
    
        best_move = sorted_moves[i][0]
        points_earned = sorted_moves[i][1]
        
         #limit = how many of your potential moves you want to check
        limit = len(sorted_moves)-5
        
        #for all of your potentials check which one of your opponent's countermove returns the lowest score 
        while i >= limit: 
            #tempMove is your potential move
            tempMove = sorted_moves[i]
            #print("try this move: ", tempMove)
            #tempBoard should be a copy of board where making changes to tempBoard does not effect board
            tempBoard = copy.copy(board)
            
            #place your potential move on the temporary board
            self.perdict_move(board=tempBoard, move=tempMove[0])
            
            #print(tempBoard)
            
            #check all the moves your opponent can make on the temporary board
            all_moves2 = PlayerUtils.identify_all_moves(board=tempBoard,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, opponentRack)))
            scored_moves2 = PlayerUtils.score_moves(tempBoard, moves=all_moves2)
            
            if len(scored_moves) == 0:
                return
            
            #get the best move your opponent can make on the temporary board
            best_move2, points_earned2 = max(scored_moves2, key=lambda x: x[1])
            #print("best move for opponent = ", best_move2, points_earned2)
            
            #update your move to be the best move you can make if the score of your opponents countermove is the lowest
            if (points_earned2 < min): 
                #print("opponents score is lower than: ", min )
                min = points_earned2
                best_move = tempMove[0]
                points_earned = tempMove[1]
                
            else:
                #print("opponents score is bigger or equal to: ", min )
                i -= 1
                continue;
            i -= 1
        #print("best move = ", best_move)

        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

    def play(self, board, opponentRack):
        all_moves = PlayerUtils.identify_all_moves(board=board,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, self.tiles)))

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return
        
        sorted_moves = sorted(scored_moves, key = lambda x: x[1])
        
        i =  len(sorted_moves)-1
        min = 100
        best_move = sorted_moves[i][0]
        points_earned = sorted_moves[i][1]
        
        #limit = how many of your potential moves you want to check
        limit = len(sorted_moves)-5
        
        #for all of your potentials check which one of your opponent's countermove returns the lowest score 
        while i >= limit: 
            #tempMove is your potential move
            tempMove = sorted_moves[i]
            #print("try this move: ", tempMove)
            
            #print(board)
            #tempBoard should be a copy of board where making changes to tempBoard does not effect board
            tempBoard = copy.copy(board)
            
            #print("should be same as last")
            #print(tempBoard)
            
            #place your potential move on the temporary board
            self.perdict_move(board=tempBoard, move=tempMove[0])
            
            #print(tempBoard)
            
            #check all the moves your opponent can make on the temporary board
            all_moves2 = PlayerUtils.identify_all_moves(board=tempBoard,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, opponentRack)))
            scored_moves2 = PlayerUtils.score_moves(tempBoard, moves=all_moves2)
            
            if len(scored_moves2) == 0:
                continue
            
            #get the best move your opponent can make on the temporary board
            best_move2, points_earned2 = max(scored_moves2, key=lambda x: x[1])
            #print("best move for opponent = ", best_move2, points_earned2)
            
            #update your move to be the best move you can make if the score of your opponents countermove is the lowest
            if (points_earned2 < min): 
                #print("opponents score is lower than: ", min )
                min = points_earned2
                best_move = tempMove[0]
                points_earned = tempMove[1]
                
            else:
                #print("opponents score is bigger or equal to: ", min )
                i -= 1
                continue;
            i -= 1
        #print("best move = ", best_move)
        
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)
class GreedyPlayer(Player):

    def __init__(self, scrabble_dictionary):
        super().__init__()
        self.scrabble_dictionary = scrabble_dictionary


    def play_first(self, board):
        middle_spot = len(board.board) // 2
        rack = list(map(lambda x: x.letter, self.tiles))

        all_moves = []
        for direction in [Board.Direction.HORIZONTAL, Board.Direction.VERTICAL]:
            all_moves += PlayerUtils.identify_moves_from_hook(
                scrabble_dictionary=self.scrabble_dictionary,
                board=board, rack=rack,
                hook_letter=None,
                hook_coordinates=(middle_spot, middle_spot),
                prefix_length=len(board.board) - middle_spot,
                suffix_length=len(board.board) - middle_spot,
                direction=direction
            )

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = max(scored_moves, key=lambda x: x[1])
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

    def play(self, board):
        all_moves = PlayerUtils.identify_all_moves(board=board,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, self.tiles)))

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = max(scored_moves, key=lambda x: x[1])
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

class RandomPlayer(Player):

    def __init__(self, scrabble_dictionary):
        super().__init__()
        self.scrabble_dictionary = scrabble_dictionary


    def play_first(self, board):
        middle_spot = len(board.board) // 2
        rack = list(map(lambda x: x.letter, self.tiles))

        all_moves = []
        for direction in [Board.Direction.HORIZONTAL, Board.Direction.VERTICAL]:
            all_moves += PlayerUtils.identify_moves_from_hook(
                scrabble_dictionary=self.scrabble_dictionary,
                board=board, rack=rack,
                hook_letter=None,
                hook_coordinates=(middle_spot, middle_spot),
                prefix_length=len(board.board) - middle_spot,
                suffix_length=len(board.board) - middle_spot,
                direction=direction
            )

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = random.choice(scored_moves)
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

    def play(self, board):
        all_moves = PlayerUtils.identify_all_moves(board=board,
                                                   scrabble_dictionary=self.scrabble_dictionary,
                                                   rack=list(map(lambda x: x.letter, self.tiles)))

        scored_moves = PlayerUtils.score_moves(board, moves=all_moves)

        if len(scored_moves) == 0:
            return

        best_move, points_earned = random.choice(scored_moves)
        self.finalize_move(board=board, move=best_move, points_earned=points_earned)

