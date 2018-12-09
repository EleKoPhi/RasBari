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
        self.errorFlag = noError

        self.initialize_steprange()

    def one_step(self, direction, speed):

        if direction == forwards:
            print("one step forwards")
            self.position_is -= 1

        if direction == backwards:
            print("one step backwards")
            self.position_is += 1

        time.sleep(speed)

    def initialize_steprange(self):

        self.range = 0

        while self.range != 10:  # TODO check right roll switch here
            self.one_step(backwards, 0.2)



        while self.range != 0:  # TODO check left roll switch here
            self.one_step(forwards, 0.2)
            self.range += 1

        self.position_is = 0
        print(self.range)

        #for i in range(5):
        #    self.one_step(backwards,0.2)

        print(self.position_is)

    def move_slider(self, percentage_position,speed):

        position_should = int(self.range * (percentage_position / 100))

        while position_should != self.position_is:

            if self.errorFlag == Error:
                break

            elif position_should > self.position_is:
                self.one_step(forwards,speed)

            elif position_should < self.position_is:
                self.one_step(backwards,speed)

            else: print("error during slider movement - wrong input")




a = stepper()
a.move_slider(20,1)

