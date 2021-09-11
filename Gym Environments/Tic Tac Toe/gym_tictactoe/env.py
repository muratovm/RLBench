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
        #if there's a valid action
        reward = 0
        if action[0]:
            x,y = action[0]
            agent = action[1]
            element = self.signing[agent.sign]

            #if the slot was not taken before
            if self.board[y,x] == 0:
                self.board[y,x] = element
                self.moves += 1
                self.win = self.win_move((x,y))
                self.done = self.win or self.moves == self.dim**2
                if self.win: 
                    self.winner = agent.name
                    reward = 1

            else:
                reward = -1

        return reward, self.done 

    
    def render(self):
        for y in range(self.board.shape[0]):
            for x in range(self.board.shape[0]):
                print(self.mapping[self.board[y][x]], end="")
            print()


    def state_reward(self, board):
        return int(self.win_board(board))

    def win_move(self, last_move):
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


    def win_board(self, board):

        wins_conditions = np.ones(2*(self.dim+1))
        counter = 0

        #check rows
        for i in range(len(board)):
            if board[i][0] != 0:
                first = board[i][0]
                for j in range(len(board[0])):
                    if board[i][j] == first: continue
                    else: 
                        wins_conditions[counter] = 0 
                        break
            else:
                wins_conditions[counter] = 0
            counter += 1

        #check cols
        for j in range(len(board[0])):
            if board[0][j] != 0:
                first = board[0][j]
                for i in range(len(board)):
                    if board[i][j] == first: continue
                    else: 
                        wins_conditions[counter] = 0 
                        break
            else:
                wins_conditions[counter] = 0 
            counter += 1

        # check diagonals
        for i in range(self.dim):
            if board[0][0] != 0:
                if board[i][i] == board[0][0]: continue
                else:
                    wins_conditions[counter] = 0 
                    break
            else:
                wins_conditions[counter] = 0 
        counter += 1

        for i in range(self.dim):
            if board[0][self.dim-1] != 0:
                if board[i][self.dim-1-i] == board[0][self.dim-1]: continue
                else: 
                    wins_conditions[counter] = 0 
                    break
            else:
                wins_conditions[counter] = 0 
        counter += 1

        #print(counter)
        #print(wins_conditions)
        #print(np.ones(2*(self.dim+1)))
        return any(wins_conditions)
        



