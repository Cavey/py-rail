import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)

# Try 1  5 6 7 8 9 0
# Try 1 2 3 4 5 6   9 0
# Try 1    6 
sensor = 24

# The function MUST be declared before the callback
def Trigger(var_1):
  print "Train approaching"

GPIO.setup(sensor, GPIO.IN)

GPIO.add_event_detect(sensor, GPIO.RISING, callback=Trigger)

# Keep this process open so we can monitor GPIO.
while 1:
    time.sleep(1)


GPIO.cleanup()

