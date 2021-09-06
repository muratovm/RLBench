class Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self.axis_data[event.axis] = round(event.value, 2)

        up = False
        down = False
        left = False
        right = False

        if self.axis_data.get(0) != None:
            if self.axis_data.get(0) > 0:
                right = True
            if self.axis_data.get(0) < 0:
                down = True
        if self.axis_data.get(1) != None:
            if self.axis_data.get(1) > 0:
                left = True
            if self.axis_data.get(1) < 0:
                up = True

        return up, down, left, right
