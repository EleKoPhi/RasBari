import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(24,GPIO.OUT)
GPIO.output(24,GPIO.HIGH)

time.sleep(5)



