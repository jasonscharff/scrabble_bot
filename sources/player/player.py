from abc import ABC

class Player(ABC):

    def __init__(self):
        self.score = 0
        self.tiles = []

    def add_tiles(self, tiles):
        self.tiles.append(tiles)

    def play(self, current_board):
        pass
class AIPlayer(Player):

    def __init__(self, words):
        super().__init__()
        self.words = words

    def play(self, current_board):
        pass




