import random

class Agent:
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign
        
    def possible_moves(self,board):
        options = []
        for y in range(board.shape[0]):
            for x in range(board.shape[1]):
                if board[y][x] == 0:
                    options.append((x,y))
        return options
        
    def choose(self, board):
        options = self.possible_moves(board)
        return options[0]



class RandomAgent(Agent):
    
    def __init__(self, name, sign):
        super().__init__(name, sign)
        
    def choose(self, board):
        options = self.possible_moves(board)
        choice = random.choice(options)
        return choice