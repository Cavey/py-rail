import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)

# Try 1  5 6 7 8 9 0
# Try 1 2 3 4 5 6   9 0
# Try 1    6 
pir_sensor = 23
hall_sensor = 25

# The function MUST be declared before the callback
def PIR(var_1):
  value = GPIO.input(var_1)
  print "PIR Triggered "+str(value)

def Hall(var_1):
  print "Hall Triggered"

GPIO.setup(pir_sensor, GPIO.IN)
GPIO.setup(hall_sensor, GPIO.IN)

#GPIO.add_event_detect(pir_sensor, GPIO.FALLING, callback=PIR)
GPIO.add_event_detect(pir_sensor, GPIO.BOTH, callback=PIR)
# GPIO.add_event_detect(hall_sensor, GPIO.RISING, callback=Hall)

# Keep this process open so we can monitor GPIO.
while 1:
  #value = GPIO.input(sensor)
  #print value
  time.sleep(1)


GPIO.cleanup()

