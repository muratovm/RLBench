import random
import re
import numpy as np

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
        
    def choose(self, board): pass

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

class MinimaxAgent(Agent):

    def __init__(self, name, sign, depth):
        super().__init__(name, sign)
        
        self.depth = depth
        self.sign = sign
        self.op_sign = None
        self.env = None

    def assign_env(self,env):
        self.env = env

    def assign_opsign(self, opsign):
        self.op_sign = opsign
        
    def choose(self, board):
        
        options = self.possible_moves(board)

        best_option = None
        best_value = np.NINF

        alpha = np.NINF
        beta = np.inf

        for option in options:
            new_board = self.env.modify_board(board, option, self.sign)
            value = self.minimax(new_board, alpha , beta , self.depth, False)
            print(new_board)
            print("Value of this option: {}".format(value))
            if value > best_value:
                best_option = option
                best_value = value
        return best_option
 
 
    def minimax(self, board, alpha, beta, depth, is_max):
            
            #if in winning board configuration
            reward =  self.env.state_reward(board, self)
            if reward: return reward

            #otherwise if reached the end
            if depth == 0:
                return 0
                
            options = self.possible_moves(board)

            #maxing layer
            if is_max:
                value = np.NINF
                for option in options:
                    new_board = self.env.modify_board(board, option, self.sign)
                    value = max(value, self.minimax(new_board, alpha, beta, depth-1, False))
                    if beta <= alpha:
                        break
                    alpha = max(alpha, value)
                return value

            #minimizing layer
            else:
                value = np.inf
                for option in options:
                    new_board = self.env.modify_board(board, option, self.op_sign)
                    value = min(value, self.minimax(new_board, alpha, beta, depth-1, True))
                    if beta <= alpha:
                        break
                    beta = min(beta, value)
                return value

        





