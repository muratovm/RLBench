import random
import re

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

    def __repr__(self):
        return agent.name

class RandomAgent(Agent):
    
    def __init__(self, name, sign):
        super().__init__(name, sign)
        
    def choose(self, board):
        options = self.possible_moves(board)
        choice = random.choice(options)
        return choice

class UserAgent(Agent):

    def __init__(self, name, sign):
        super().__init__(name, sign)
        
    def choose(self, board):
        options = self.possible_moves(board)

        pos = None
        while not pos:
            choice = input("Choose a location in the form (x,y):")
            pattern = "^\(([0-3])\,([0-3])\)$"
            pos = re.search(pattern, choice)
            position = (int(pos[1]), int(pos[2]))

            if position not in options: 
                print("That spot is already taken")
                pos = None

        return position

