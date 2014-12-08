#hornby_lower_interface.py - this modules encapsulates the functions of the Hornby Elite DCC controller.
'''
    for this module to work they would have to create a text file called  10-elite.rules
    and copy the following (all on one line)
    ATTR{idVendor}=="04d8", ATTR{idProduct}=="000a", RUN+="/sbin/modprobe -q ftdi_sio vendor=0x04d8 product=0x000a"
    then run the they would need to move the file into etc/udev/rules.d
    they have to be in the same directory has the file >>  sudo mv 10-elite.rules /etc/udev/rules.d/
'''
import os
import hornby # Use hornby_lower_interface.py as the interface for controlling trains and accessories
import time #Use python standard module time for simple timming functions
import RPi.GPIO as GPIO

# Global Settings - Not too fast, not too slow
g_desired_speed = 70
g_slow_speed = 45
g_direction = hornby.FORWARD

g_net_cars = 0

# Load the eLink connection
try:
  hornby.connection_open('/dev/ttyACM0',115200) 
except RuntimeError as e:
  try:
    hornby.connection_open('/dev/ttyACM1',115200) 
  except RuntimeError as e:
    hornby.connection_open('/dev/ttyACM2',115200) 

# set_debug(True) to show the data transmitted and received from the controller
hornby.set_debug(False)

# Check hardware and perform initialisation 
hornby.setup()

# create a train object to represent each train to be controlled
# parameter 1 = DCC addres
# The somerset Belle (small black 6-wheeler steam train) has an ID of 3
t1 = hornby.Train(3)
# Set the train to stopped
t1.throttle(0,hornby.FORWARD)

# Are we root?  If we are not root, GPIO won't work.  To stop it bombing, I
# have been using "if isroot" before GPIO calls.
isroot = (os.geteuid() == 0);

def incoming_train(id):
    print "Train approaching the crossing"
    
def outgoing_train(id):
    print "Train leaving the crossing"
    
def incoming_car(id):
    print "Car approaching the crossing"
    
def outgoing_car(id):
    print "Car leaving the crossing"
    

#------------------------------- Sensor setup below -------------------------------------#
if isroot:
    # Using BCM mode as it's ok.  You might wanna switch to Board
    GPIO.setmode(GPIO.BCM)
    print "Running as root.  GPIO enabled";
    
    incoming_train_sensor = 24
    GPIO.setup(incoming_train_sensor,GPIO.IN)
    GPIO.add_event_detect(incoming_train_sensor, GPIO.RISING, callback=incoming_train)
    
    outgoing_train_sensor = 2
    GPIO.setup(outgoing_train_sensor,GPIO.IN)
    GPIO.add_event_detect(outgoing_train_sensor, GPIO.RISING, callback=outgoing_train)
    
    incoming_car_sensor = 23
    GPIO.setup(incoming_car_sensor,GPIO.IN)
    GPIO.add_event_detect(incoming_car_sensor, GPIO.RISING, callback=incoming_car)
    
    outgoing_car_sensor = 18
    GPIO.setup(outgoing_car_sensor,GPIO.IN)
    #GPIO.add_event_detect(outgoing_car_sensor, GPIO.RISING, callback=outgoing_car)
else:
    print "NOT running as root.  GPIO (sensors) disabled";


def Motion(SP):
    print "train passed the first sensor on   " + time.strftime("%c")  
    print "train stopping"
    t1.throttle(0,hornby.FORWARD)
    time.sleep(1)
    print "what would you like to do??"
    option = raw_input("Press a) if you wish to carry on moving forward\nPress b) if you wish to reverse \n>>")
    repeat = 1
#    while repeat >= 1:
##    while True:
    if option == "a":
      
      repeat+= 1
      t1.throttle(90,hornby.FORWARD)
      
    elif option == "b":
      
      repeat+= 1
      t1.throttle(80,hornby.REVERSE)
    else:
      print "invalid option"
        
    
##    t1.throttle(30,hornby.REVERSE)
##    wait(7)
##    t1.throttle(0,hornby.REVERSE)

try:
    print '''
    \t\t\t********************************
    \t\t\t*Faraday 1 Train Crossing Code *
    \t\t\t********************************

Note: press Ctrl + C ONCE to exit
          '''
    print "Starting the journey"
    t1.throttle(g_desired_speed, g_direction)
    while 1:
      # This causes it to wait for the GPIO pin to trigger
      time.sleep(2)

    # Should never actually get here
    hornby.connection_close()
    if isroot:
      GPIO.cleanup()

except KeyboardInterrupt:
    print "Stopping the program"
    
    t1.throttle(0,hornby.FORWARD) # stopping the train
    hornby.connection_close()
    
    if isroot:
      GPIO.cleanup()
    print '''
    \t\t\t********************************
    \t\t\t      *****ENDING*****
    \t\t\t********************************
          '''

# Example function for writing to a file
def writelog(message):
   '''
      To write to a file, call this function
   '''
   with open("messagelog.log", "a") as myfile:
     myfile.write(message)
