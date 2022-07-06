import torch 
import torch.nn as nn

class SmartAgent(nn.Module):
    
    def __init__(self, name, sign):
        super(SmartAgent, self).__init__()
        self.name = name
        self.sign = sign
        
        self.trajectory = [] #element: [board, position, value]
        
        self.board_encoder = nn.Conv2d(1, 8, 3, stride=1)
        self.action_encoder = nn.Linear(6, 9)
        
        empty = torch.zeros((1,1,3,3))
        units = self.board_encoder(empty).numel()
        
        self.encoding_parser = nn.Linear(8, 9)
        
        self.row_layer = nn.Linear(9, 3)
        self.col_layer = nn.Linear(9, 3)
        
        self.reward_layer = nn.Linear(18, 1)
        
        #layers = [self.c_1, self.l_1]
        #self.model = nn.Sequential(*layers)
    
    def possible_moves(self,board):
        options = []
        for y in range(board.shape[0]):
            for x in range(board.shape[1]):
                if board[y][x] == 0:
                    options.append((x,y))
        return options
    
    
    def board_to_embed(self, board):
        #process the board
        board = torch.tensor(board, dtype=torch.float32)
        board = torch.reshape(board, (1,1,3,3))
        
        out = self.board_encoder(board)
        out = out.reshape((1,-1))
        out = self.encoding_parser(out)
        
        return out
    
    def board_to_prediction(self, board):
        out = self.board_to_embed(board)
        
        o_row = self.row_layer(out)
        o_col = self.col_layer(out)
        
        
        return [o_row,o_col]
        
    def action_to_reward(self, board, row, col):
        board_out = self.board_to_embed(board)
        
        #process the action
        row_input = torch.zeros(1,3)
        col_input = torch.zeros(1,3)
        
        row_input[0][row] = 1
        col_input[0][col] = 1

        comb = torch.cat((row_input, col_input), 1)
        action_out = self.action_encoder(comb)
        
        comb = torch.cat((board_out, action_out), 1)
        reward = self.reward_layer(comb)
        
        return reward
    
    def best_reward_move(self, board):
        moves = self.possible_moves(board)
        #print(moves)
        options = []
        
        for move in moves:
            reward = self.action_to_reward(board, move[0], move[1])
            options.append([move, reward])
            
        if options:
            best = max(options, key=lambda x: x[1][0].item())
            best_move = best[0]
            #print(best_move)
            #print("============")
            #for thing in options:
            #    print(thing)

            return best_move
        
        return None

    def forward(self, board, row = None, col = None):
        if row != None and col != None:
            return self.action_to_reward(board, row, col)
        
        predicted_move = self.board_to_prediction(board)
        
        return predicted_move
    
    def learn_trajectory(self):
        
        for i in range(len(self.trajectory)-1, 0, -1):        
            board, position, reward = self.trajectory[i]
    
        self.trajectory = []
