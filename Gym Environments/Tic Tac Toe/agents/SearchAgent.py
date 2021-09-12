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

        for option in options:
            new_board = self.env.modify_board(board, option, self.sign)
            value = self.minimax(new_board, self.depth, False)
            if value > best_value:
                best_option = option
                best_value = value
        return best_option

    def minimax(self, board, depth, is_max):

        winner = self.env.win_board(board)

        if winner:
            sign = self.env.mapping[winner]
            if sign == self.sign:
                return self.env.state_reward(board)
            else:
                return -1 * self.env.state_reward(board)


        if depth == 0 or self.env.board_filled(board):
            return 0
            
        options = self.possible_moves(board)

        if is_max:
            value = np.NINF
            for option in options:
                new_board = self.env.modify_board(board, option, self.sign)
                value = max(value, self.minimax(new_board, depth-1, False))
            return value


        else:
            value = np.inf
            for option in options:
                new_board = self.env.modify_board(board, option, self.op_sign)
                value = min(value, self.minimax(new_board, depth-1, True))
            return value

        





