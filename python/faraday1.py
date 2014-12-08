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
    hornby.connection_open
    ('/dev/ttyACM1',115200) 
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

g_train_stopped = 0
g_train_on_crossing = 0
g_net_cars = 0

# Example function for writing to a file
def writelog(message):
   '''
      To write to a file, call this function
   '''
   print message
   with open("messagelog.log", "a") as myfile:
     myfile.write(message)
     myfile.write("\n")

def incoming_train(id):
    global g_net_cars
    global g_train_stopped
    global g_train_on_crossing
    writelog( "Train approaching the crossing")
    g_train_on_crossing = 1
    if g_net_cars > 0:
      writelog( "Car on crossing, stopping train" )
      t1.throttle(0,hornby.FORWARD)
      g_train_stopped = 1
    
def outgoing_train(id):
    global g_net_cars
    global g_train_stopped
    global g_train_on_crossing
    writelog( "Train leaving the crossing" )
    g_train_on_crossing = 0

def car(id):
    value = GPIO.input(id)
    if value:
      outgoing_car(id)
    else :
      incoming_car(id)
    
def incoming_car(id):
    global g_net_cars
    global g_train_stopped
    global g_train_on_crossing
    writelog( "Car approaching the crossing" )
    g_net_cars += 1
    if g_net_cars > 0 and g_train_on_crossing == 1:
      writelog( "Car arrives when train on crossing" )
    
def outgoing_car(id):
    global g_net_cars
    global g_train_stopped
    global g_train_on_crossing
    writelog( "Car leaving the crossing" )
    g_net_cars -= 1
    if g_net_cars < 0:
      writelog( "Imaginary cars detected" )
      g_net_cars = 0
    if g_net_cars == 0 and g_train_stopped == 1:
      writelog( "Car left crossing, resume journey" )
      t1.throttle(g_desired_speed, g_direction)
      g_train_stopped = 0
    

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
    GPIO.add_event_detect(incoming_car_sensor, GPIO.BOTH, callback=car)
    #GPIO.add_event_detect(incoming_car_sensor, GPIO.FALLING, callback=outgoing_car)
    
    outgoing_car_sensor = 18
    GPIO.setup(outgoing_car_sensor,GPIO.IN)
    #GPIO.add_event_detect(outgoing_car_sensor, GPIO.RISING, callback=outgoing_car)
else:
    print "NOT running as root.  GPIO (sensors) disabled";


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

