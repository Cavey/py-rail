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
# example functions for South West Digital's Class 108 (55488) decoder
# F0 Lights on
def lights_on(t):
  t.function(0,hornby.ON)
# F0 Lights off
def lights_off(t):
  t.function(0,hornby.OFF)
# F1 Sound on
def sound_on(t):
  t.function(1,hornby.ON)
# F1 Sound off
def sound_off(t):
  t.function(1,hornby.OFF)
# F2 Horn 1
def horn1(t):
  t.function(2,hornby.ON)
  time.sleep(.1)
  t.function(2,hornby.OFF)
# F3 Horn 2
def horn2(t):
  t.function(3,hornby.ON)
  time.sleep(.1)
  t.function(3,hornby.OFF)
# F4 Brake
def brake(t):
  t.function(4,hornby.ON)
  time.sleep(.1)
  t.function(4,hornby.OFF)
# F5 Buzzer x 2
def buzzer2(t):
  t.function(5,hornby.ON)
  time.sleep(.1)
  t.function(5,hornby.OFF)
# F6 Buzzer x 1
def buzzer1(t):
  t.function(6,hornby.ON)
  time.sleep(.1)
  t.function(6,hornby.OFF)
# F7 Aux 1 on
def aux1_on(t):
  t.function(7,hornby.ON)
# F7 Aux 1 off
def aux1_off(t):
  t.function(7,hornby.OFF)
# F8 Aux 2 on
def aux2_on(t):
  t.function(8,hornby.ON)
# F8 Aux 2 off 
def aux2_off(t):
  t.function(8,hornby.OFF)
# F9 Directional Gear Change
def gear_change(t):
  t.function(9,hornby.ON)
  time.sleep(.1)
  t.function(9,hornby.OFF)
# F10 Guards Whistle
def guards_whistle(t):
  t.function(10,hornby.ON)
  time.sleep(.1)
  t.function(10,hornby.OFF)

# Accessory - station signal Go
def station_signal_go(a) :
  a.activate()
# Accessory - station signal Stop
def station_signal_stop(a) :
  a.deactivate()

# helper function - wait a given number of seconds
def wait(secs):
  print "Wait {0:d} seconds".format(secs)
  time.sleep(secs)

''' Open a serial connection with the Hornby Elite DCC controller they would have to download pyserial (before hand)
   they would have to run the command dmesg
'''
try:
  hornby.connection_open('/dev/ttyACM0',115200) #<<<<<< must be changed to the right device + baud rate changed for the elink
except RuntimeError as e:
  try:
    hornby.connection_open('/dev/ttyACM1',115200) #<<<<<< must be changed to the right device + baud rate changed for the elink
  except RuntimeError as e:
    hornby.connection_open('/dev/ttyACM2',115200) #<<<<<< must be changed to the right device + baud rate changed for the elink


# set_debug(True) to show the data transmitted and received from the controller
hornby.set_debug(True)

hornby.setup()

# create a train object to represent each train to be controlled
# parameter 1 = DCC addres
t1 = hornby.Train(3)

# Are we root?  If we are not root, GPIO won't work.
isroot = (os.geteuid() == 0);


#------------------------------- Sensor setup below -------------------------------------#
'''setting the mode of the board
   setting the pin I'm using then telling the GPIO to take the info from the specified pin & the direction of its flow
'''
if isroot:
    GPIO.setmode(GPIO.BCM)
    SP = 7
    GPIO.setup(SP,GPIO.IN)
    print "Running as root.  GPIO enabled";
else:
    print "NOT running as root.  GPIO (sensors) disabled";

def Motion(SP):
    print "train passed the first sensor on   " + time.strftime("%c")  
    print "train stopping"
    t1.throttle(0,hornby.FORWARD)
    time.sleep(1)
    print "what would you like to do??"
    option = raw_input("Press a) if you wish to carry on movinf forward\nPress b) if you wish to reverse \n>>")
    repeat = 1
#    while repeat >= 1:
##    while True:
    if option == "a":
      
      repeat+= 1
      t1.throttle(90,hornby.FORWARD)
      
    elif option == "b":
      
      repeat+= 1
      t1.throttle(80,hornby.REVERSE)
##      else:
##        print "invalid option"
        
    
##    t1.throttle(30,hornby.REVERSE)
##    wait(7)
##    t1.throttle(0,hornby.REVERSE)

try:
    print '''
    \t\t\t********************************
    \t\t\t*Sytel Railway Automation Demo*
    \t\t\t********************************

loading sensor....
press Ctrl + C to exit
          '''
    t1.throttle(0,hornby.FORWARD)
    speed = raw_input("\nplease enter the speed you wish the train to travel  ")
    try:
      val = int(speed)
      t1.throttle(val,hornby.FORWARD)
    except ValueError:
      print

    # needed otherwise the signal will still be transmitted and the loco will continue to move
    if isroot:
      GPIO.add_event_detect(SP, GPIO.RISING, callback=Motion)
    while 1:
        time.sleep(4)


    # close the connection with a Hornby Elite DCC controller 
    hornby.connection_close()
    if isroot:
      GPIO.cleanup()

    print '''
    \t\t\t********************************
    \t\t\t      *****ENDING*****
    \t\t\t********************************
      '''

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
