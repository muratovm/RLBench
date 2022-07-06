from gym_omnipath.envs.rendering import *
class Board:

    def __init__(self):
        self.viewer = None

        #graphical settings
        self.scale = 15
        self.tail = 10
        self.screen_size = 30
        self.agent_dim = (2 , 2)
        self.upper_bounds = 0
        self.lower_bounds = self.screen_size

        #lines the agent cannot cross
        self.up = self.upper_bounds + self.agent_dim[0]/2
        self.down = self.lower_bounds - self.agent_dim[1]/2
        self.left = self.upper_bounds + self.agent_dim[0]/2
        self.right = self.lower_bounds - self.agent_dim[1]/2
        
        self.agent_trans = Transform()
        self.goal_trans = Transform()

        self.goal = None

    def initializer_viewer(self, agent_state):
        self.viewer = Viewer(self.screen_size*self.scale, self.screen_size*self.scale)
        self.viewer.set_bounds(0, self.screen_size, 0, self.screen_size)
        
        # initialize game field area
        l, r, t, b = self.upper_bounds, self.lower_bounds, self.upper_bounds, self.lower_bounds
        field = FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
        field.set_color(0.7, 0.7, 0.7)
        self.viewer.add_geom(field)

        l, r, t, b = -self.agent_dim[0]/2, self.agent_dim[0]/2, -self.agent_dim[1]/2,self.agent_dim[1]/2
        # initialize agent geometry
        #agent = FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
        agent = FilledPolygon([(r, t), (r, b), (l, b), (l, t)])
        self.agent_trans.set_translation(agent_state[0]- self.agent_dim[0], agent_state[1] - self.agent_dim[1],self.screen_size,self.screen_size)
        agent.add_attr(self.agent_trans)
        self.viewer.add_geom(agent)

        # initialize goal geometry
        goal = FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
        self.goal_trans.set_translation(self.goal[0], self.goal[1],self.screen_size,self.screen_size)
        goal.add_attr(self.goal_trans)
        goal.set_color(1, 1, 1)
        self.viewer.add_geom(goal)

    def set_goal(self,goal):
        self.goal = goal
        self.goal_trans.set_translation(goal[0], goal[1], self.screen_size,self.screen_size)

    def inside(self, up, down,left,right,x,y):
        if x > left and x < right and y > down and y < up:
            return True
        return False

    def bound_agent(self, state):
        #check agent is inside the field
        if not self.inside(self.up,self.down,self.left,self.right, state[0], state[1]):
            if state[1] < self.up: state[1] = self.up
            if state[0] < self.left: state[0] = self.left
            if state[1] > self.down: state[1] = self.down
            if state[0] > self.right: state[0] = self.right
        return state

    def available_locations(self, state):
        available = []
        if state[1] > self.up: available.append(state+[0,-1])
        if state[0] > self.left: available.append(state+[-1,0])
        if state[1] < self.down: available.append(state+[0,1])
        if state[0] < self.right: available.append(state+[1,0])
        return available

    def state_reward(self,state):
        
        if np.array_equal(state, self.goal):
            return 1
        return 0
        
        """
        dist_x = abs(state[0] - self.goal[0])
        dist_y = abs(state[1] - self.goal[1])
        return 1 - ((dist_x + dist_y) / (self.screen_size * 2))
        """

    def update_scene(self,state,reward):
        l, r, t, b = 0, self.agent_dim[0] / 2, self.agent_dim[0] / 2, 0
        trace = FilledPolygon([(l, b), (l, t), (r, t), (r, b)])

        red = 1 - reward
        green = reward
        blue = 0

        trace.set_color(red, green, blue)
        trans = Transform()
        trans.set_translation(state[0] + self.agent_dim[0]/4, state[1] + self.agent_dim[1]/4,self.screen_size,self.screen_size)
        trace.add_attr(trans)
        self.viewer.add_geom(trace)