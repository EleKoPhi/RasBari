import sys
sys.path.insert(0,"/home/pi/RasBari")
from TxTMethoden import *
from gobal_variables import *
import time
import RPi.GPIO as GPIO

class stepper:
    
    nr_of_stepper = 0

    def __init__(self):
        self.taster_flag = no_taster_on
        stepper.nr_of_stepper += 1
        self.ID = "stepper_" + str(self.nr_of_stepper)
        self.Initial_data = get_stepper_ini(self.ID)
        self.DIR = int(self.Initial_data["direction_pin"])
        self.ENA = int(self.Initial_data["enable_pin"])
        self.PUL = int(self.Initial_data["pull_pin"])
        self.pin_taster_links = int(self.Initial_data["taster_links_pin"])
        self.pin_taster_rechts = int(self.Initial_data["taster_rechts_pin"])
        self.StepSize = int(self.Initial_data["microstepsize"])
        self.range = 0
        self.position_is = 0
        self.errorFlag = noError
        
        GPIO.setwarnings(False)
        GPIO.setup([self.pin_taster_links,self.pin_taster_rechts],GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin_taster_rechts,GPIO.RISING,callback=self.flag_changer)
        GPIO.add_event_detect(self.pin_taster_links,GPIO.RISING,callback=self.flag_changer)
        
        GPIO.setup(self.PUL,GPIO.OUT)
        GPIO.setup(self.DIR,GPIO.OUT)
        
        self.initialize_steprange()

        del self.Initial_data
        
    def flag_changer(self,channel):
        
        if GPIO.input(self.pin_taster_links)==pin_high:
            self.taster_flag=taster_left_on
            
        if GPIO.input(self.pin_taster_rechts)==pin_high:
            self.taster_flag=taster_right_on

    def one_step(self,speed):

        GPIO.output(self.PUL,GPIO.HIGH)
        time.sleep((1/speed)*0.0001)
        GPIO.output(self.PUL,GPIO.LOW)
        time.sleep((1/speed)*0.0001)

    def initialize_steprange(self):

        self.range = 0
        self.position_is = 0
        self.set_direction(right)
        
        while self.taster_flag!=taster_right_on:
            self.one_step(1)
        self.set_direction(left)
        time.sleep(1)
        while self.taster_flag!=taster_left_on:
            self.one_step(1)
            self.range +=1
            
        self.set_direction(right)
        time.sleep(1)
        
        for i in range(50):
            self.one_step(0.1)
            self.position_is+=1


    def set_direction(self, direction):

        if direction == left:
            GPIO.output(self.DIR,GPIO.LOW)
        if direction == right:
            GPIO.output(self.DIR,GPIO.HIGH)
        
           
    def move_slider(self, percentage_position,speed):

        position_should = int(self.range * (percentage_position / 100))

        if position_should != self.position_is:

            if position_should>self.position_is:
                self.set_direction(right)

                while(position_should!=self.position_is):
                    self.one_step(speed)
                    self.position_is+=1

            if position_should<self.position_is:
                self.set_direction(left)

                while(position_should!=self.position_is):
                    self.one_step(speed)
                    self.position_is-=1
  
# stepper test

"""a = stepper()
time.sleep(1)
a.move_slider(30,1)
time.sleep(1)
a.move_slider(40,1)
time.sleep(1)
a.move_slider(0,1)
time.sleep(1)
print("done")"""



