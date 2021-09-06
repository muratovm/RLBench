import gym
import numpy as np

class TicTacToeEnv(gym.Env):

    def __init__(self, dim=3):
        self.dim = dim
        self.players = 0
        self.mapping = {0: "-"}
        self.signing = {}
        self.reset()


    def reset(self):
        self.board = np.zeros((self.dim,self.dim))
        self.done = False
        self.moves = 0
        self.winner = None
    
    def register_agent(self, agent):
        self.players += 1
        self.mapping[self.players] = agent.sign
        self.signing[agent.sign] = self.players
        
    def step(self, action):
        if action[0]:
            x,y = action[0]
            agent = action[1]
            element = self.signing[agent.sign]

            self.board[y,x] = element
            self.moves += 1
            self.win = self.win_condition((x,y))
            #self.filled = not all(self.board[x,y]==0 for y in range(3) for x in range(3))
            self.done = self.win or self.moves == self.dim**2
            if self.win: self.winner = agent.name

        return self.done 

    
    def render(self):
        for y in range(self.board.shape[0]):
            for x in range(self.board.shape[0]):
                print(self.mapping[self.board[y][x]], end="")
            print()

    def win_condition(self, last_move):
        x,y = last_move

        #check row and column
        row = all(e == self.board[y][x] for e in self.board[y])
        col = all(row[x] == self.board[y][x] for row in self.board)


        # check diagonals
        diag1, diag2 = False, False
        shift = self.dim - 1
        if x-y == 0: 
            diag1 = all(self.board[i][i] == self.board[y][x] for i in range(self.dim))
        if x+y == shift: 
            diag2 = all(self.board[shift-i][i] == self.board[y][x] for i in range(self.dim))

        #did someone win?
        return row or col or diag1 or diag2