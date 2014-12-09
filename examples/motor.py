import RPi.GPIO as GPIO
import time
import random

GPIO.setmode(GPIO.BCM)

# Try 1  5 6 7 8 9 0
# Try 1 2 3 4 5 6   9 0
# Try 1    6 
controlpins = [7,8,25,11]

seq = [
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1],
  [1,0,0,0]       ]

for pin in controlpins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin,0)

for i in range(512/4):
  for halfstep in range(8):
    #halfstep = 7-halfstep
    for pin in range(4):
      GPIO.output(controlpins[pin], seq[halfstep][pin])
    time.sleep(0.001)

GPIO.cleanup()

