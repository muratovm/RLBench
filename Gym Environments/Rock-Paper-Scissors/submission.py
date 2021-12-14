
import numpy as np
import collections
import logging, sys


def counter(action):
    action = int(action)
    counters = {0:1,1:2,2:0}
    return counters[action]

def wipe_file(file_name):
    open(file_name, 'w').close()
    
    
def write_file(file_name, text, nl=False):
    file = open(file_name, 'a')
    file.write(text)
    if nl: file.write("\n")
    file.close()
    
def reinforcement_table(observation, configuration):
    #0-18 pattern match
    #19 recent state frequency
    global strategies
    
    #metascoring
    global patternScores
    global patternUsed
    
    #pattern matching
    global sequences
    global pairings
    
    #reinforcement learning
    global state #[my_state, opponent_state, my_move, opponent_move]
    global frequencies
    
    if observation.step == 998:
        write_file("debug.txt", str(patternUsed),True)
    
    
    if observation.step <= 0: #initialize the state space
        
        strategies = [0]*24
        patternScores = np.zeros((len(strategies)), dtype=np.int16)
        patternUsed = np.zeros((len(strategies)), dtype=np.int16)
        
        #pattern matching
        pairings = {'00': '0', '01':'1', '02':'2',
                    '10': '3', '11':'4', '12':'5',
                    '20': '6', '21':'7', '22':'8'}
        
        #reinforcement learning
        frequencies = np.zeros((3,3,3), dtype=np.float32)
        state = np.zeros((4), dtype=np.int16)
        sequences = ["","",""]
        
        #logging
        #wipe_file("debug.txt")
        
        return int(state[2])
    
    else:
        #update state to include last opponent move
        state[3] = observation.lastOpponentAction
        
        
        
        for i in range(len(strategies)):
            reward = int(state[3] == strategies[i]) - int(state[3] == counter(strategies[i]))
            patternScores[i]*=0.8
            patternScores[i]+=reward*3
        
        
        #PATTERN MATCHING 0-6
        #--------------------------------------------------------------------------------
        #record sequences
        sequences[0] += pairings[str(state[2])+str(state[3])] #ourmoves
        sequences[1] += str(state[2]) #my moves
        sequences[2] += str(state[3]) #your moves

        limit = min(5, len(sequences[0]))
        #go through the 6 metastrategies
        for i in range(len(sequences)):
            seq = sequences[i]
            j = limit
            while j >= 1 and not seq[-j:] in seq[:-1]: j -=1
            if j>0:
                loc = seq.rfind(sequences[i][-j:],0,-1)
                strategies[0+2*i] = int(sequences[2][loc+j])          #if you continue playing like that I'm winning
                strategies[1+2*i] = counter(sequences[1][loc+j])      #if you're on to me I'll counter it
        
        #FREQUENCY MATCHING 7
        #--------------------------------------------------------------------------------
        #update frequence of occurance of (my_state, opponent_state, opponent_move)
        frequencies*= 0.8
        frequencies[state[0]][state[1]][state[3]] += 1
        
        #predict move based on maximum value in (my_move, opponent_move) column
        predicted_opponent_move = np.argmax(frequencies[state[2]][state[3]], axis = 0)
        strategies[7] = predicted_opponent_move
        
        
        #RANDOM 8
        #--------------------------------------------------------------------------------
        strategies[8] = int(np.random.randint(3))
        
        
        #COUNTER ALL OF MY STRATEGIES 
        #--------------------------------------------------------------------------------
        for i in range(8,8*3):
            strategies[i] = counter(strategies[i-6])   #if you know this strategy I'll counter it again
        
        
        #choose the best strategy
        strategy_num = np.argmax(patternScores, axis=0)
        output = strategies[strategy_num]
        patternUsed[strategy_num] += 1
        
        #update state for next iteration
        state = np.array([state[2], state[3], counter(output), -1])
        return int(state[2])
    