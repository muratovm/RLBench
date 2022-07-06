import sys
import gym
from gym_omnipath.envs.rendering import *
import numpy as np

import os
import pprint
import time

class OmnipathEnv(gym.Env):


    metadata = {'render.modes': ['human']}

    def __init__(self):
        from gym_omnipath.envs.boards import Board
        from gym_omnipath.envs.agents import Automaton, Manual


        self.board = Board()
        self.agent = Automaton(self.board.scale)

        #environment initialization
        self.action_space = gym.spaces.discrete.Discrete(4)
        self.observation_space = np.zeros(2)
        self.control = False

        #parameters
        self.gamma = 1
        self.done = False
        self.info = ""

        #state values
        self.values = np.zeros((self.board.screen_size,self.board.screen_size, 2))
        #the_values = self.values[:,:,0]
        #the_values.fill(0)

        #state initialization
        init_state = np.array([self.board.screen_size // 10, 9 * self.board.screen_size // 10], dtype=np.int32)
        goal = (9 * self.board.screen_size / 10, 1 * self.board.screen_size / 10)
        
        self.board.set_goal(goal)
        self.agent.set_state(init_state)
        self.prev_state = self.agent.state
        
    def update_values(self, agent_state):
        max_reward = 0
        best_state = None
        for state in self.board.available_locations(agent_state):
            x,y = state
            future_expected = self.board.state_reward(self.agent.state) + (self.gamma * self.values[y][x][0])
            max_reward = max(future_expected, max_reward)

        x,y = agent_state
        self.values[y][x][0] = max_reward
        
        #nudge_value = (value + self.values[y][x][0]) / (self.values[y][x][1]+1)
    	#self.values[y][x] += [nudge_value,1]

    def step(self, action):
        #action: 0,1,2,3

        #get action array
        actions = self.agent.get_action(action)

	    #move the agent
        if actions[0]: #up
            self.agent.state[1] -= self.agent.speed
        if actions[1]: #left
            self.agent.state[0] -= self.agent.speed
        if actions[2]: #down
            self.agent.state[1] += self.agent.speed
        if actions[3]: #right
            self.agent.state[0] += self.agent.speed

        #make sure agent does not excape the board constraints
        self.agent.state = self.board.bound_agent(self.agent.state)
        reward = self.board.state_reward(self.agent.state)
        
        #reached goal
        if reward == 1:
            self.done = True

	    #if the agent moves, update the tail 
        if self.board.viewer != None:
            if not np.array_equal(self.prev_state, self.agent.state):
                self.board.update_scene(self.agent.state, reward)
                if self.agent.tail == 0:
                    self.board.viewer.remove_geom()
                else:
                    self.agent.tail -= 1

        self.prev_state = self.agent.state
        return (self.agent.state, reward, self.done, self.info)

    def render(self, mode='human'):
        if self.board.viewer == None:
            self.board.initializer_viewer(self.agent.state)
        self.board.agent_trans.set_translation(self.agent.state[0], self.agent.state[1],self.board.screen_size,self.board.screen_size)
        self.board.goal_trans.set_translation(self.board.goal[0], self.board.goal[1],self.board.screen_size,self.board.screen_size)
        if self.board.viewer.isopen:
            self.board.viewer.render()
        else:
            sys.exit(0)

    def reset(self):
        self.state[0] = 200
        self.state[1] = 1200

        self.prev_state[0] = self.state[0]
        self.prev_state[1] = self.state[1]

        self.done = False
    
    def set_agent_state(self, state):
        self.agent.state = self.board.bound_agent(state)

    def close(self):
        if self.board.viewer != None:
            self.board.viewer.close()

    def controllable(self):
        from gym_omnipath.envs.agents import Manual

        self.agent = Manual(self.board.scale)
        self.agent.set_state(self.prev_state)

        #for controllable
        self.board.initializer_viewer(self.agent.state)
        self.board.viewer.window.push_handlers(self.agent.keys)
    




    

