
from pyglet.window import key
import time

class Agent:
    def __init__(self,scale):
        self.scale = scale
        self.speed = 1
        self.tail = 10
        self.init_state = None
        self.state = None

    def set_state(self, state):
        #set initial value
        if self.init_state is None:
            self.init_state = state
        self.state = state

    def new_state_action(self,state):
        shift = state - self.state
        if shift[1] != 0: # y axis
            if shift[1] == 1: #down
                action = 2
            else: #up
                action = 0
        else: #x axis
            if shift[0] == 1: #right
                action = 3
            else: # left
                action = 1
        return action


    def reset(self):
        if not self.init_state is None:
            self.state = self.init_state


class Automaton(Agent):
    def __init__(self,scale):
        super().__init__(scale)

    def get_action(self, action):
        actions = [False,False,False,False]
        actions[action] = True
        return actions


class Manual(Agent):
    def __init__(self,scale):
        super().__init__(scale)
        self.keys = key.KeyStateHandler()

    def get_action(self,action):
        actions = [self.keys[key.W],self.keys[key.A],self.keys[key.S],self.keys[key.D]]
        if self.keys[key.LSHIFT]:
            self.speed = 3
        else:
            self.speed = 1
        time.sleep(1/30)
        return actions


    