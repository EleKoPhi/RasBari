from TxTMethoden import *
from gobal_variables import *
import time


class stepper:
    nr_of_stepper = 0

    def __init__(self):
        stepper.nr_of_stepper += 1
        self.ID = "stepper_" + str(self.nr_of_stepper)
        self.Initial_data = getStepper_ini(self.ID)
        self.DIR = int(self.Initial_data["direction_pin"])
        self.ENA = int(self.Initial_data["enable_pin"])
        self.PUL = int(self.Initial_data["pull_pin"])
        self.StepSize = int(self.Initial_data["microstepsize"])
        self.range = 0
        self.position_is = 0

        self.initialize_steprange()

    def one_step(self, direction, speed):

        if direction == forwards:
            print("one step forwards")
            self.position_is += 1

        if direction == backwards:
            print("one step backwards")
            self.position_is -= 1

        time.sleep(speed)

    def initialize_steprange(self):

        while self.range != 10:  # TODO check right roll switch here
            self.one_step(backwards, 0.2)
            self.range += 1

        while self.range != 0:  # TODO check left roll switch here
            self.one_step(forwards, 0.2)
            self.range -= 1

        self.position_is = 0

    def move_slider(self, percentage_position):

        position_should = int(self.range * (percentage_position / 100))

        while position_should != self.position_is:

            if position_should > self.position_is:
                self.one_step(forwards)

            if position_should < self.position_is:
                self.one_step(backwards)


a = stepper()

