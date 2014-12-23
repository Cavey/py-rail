#hornby_lower_interface.py - this modules encapsulates the functions of the Hornby Elite DCC controller.
'''
    for this module to work they would have to create a text file called  10-elite.rules
    and copy the following (all on one line)
    ATTR{idVendor}=="04d8", ATTR{idProduct}=="000a", RUN+="/sbin/modprobe -q ftdi_sio vendor=0x04d8 product=0x000a"
    then run the they would need to move the file into etc/udev/rules.d
    they have to be in the same directory has the file >>  sudo mv 10-elite.rules /etc/udev/rules.d/
'''
import hornby # Use hornby_lower_interface.py as the interface for controlling trains and accessories
import time #Use python standard module time for simple timming functions
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

try:
  hornby.connection_open('/dev/ttyACM0',115200) #<<<<<< must be changed to the right device + baud rate changed for the elink
except RuntimeError as e:
  try:
    hornby.connection_open('/dev/ttyACM1',115200) #<<<<<< must be changed to the right device + baud rate changed for the elink
  except RuntimeError as e:
    hornby.connection_open('/dev/ttyACM2',115200) #<<<<<< must be changed to the right device + baud rate changed for the elink


# set_debug(True) to show the data transmitted and received from the controller
# Try not to worry if it goes wierd
hornby.set_debug(False)

# Check hardware and perform initialisation 
hornby.setup()

# create a train object to represent each train to be controlled
# parameter 1 = DCC addres
# The somerset Belle (small black 6-wheeler steam train) has an ID of 3

try:
    print '''
    \t\t\t********************************
    \t\t\t*   Railway Test Program Demo  *
    \t\t\t********************************

press Ctrl + C ONCE to exit
          '''
    for i in range(3,5):
        print "Testing train "+ str(i)
        t1 = hornby.Train(i)
        # Make sure it's stopped
        t1.throttle(0,hornby.FORWARD)
        try:
          sound_on(t1)
          horn1(t1)
          aux1_on(t1)
          aux1_off(t1)
          guards_whistle(t1)
          t1.throttle(55, hornby.FORWARD)
          time.sleep(2)
          t1.throttle(0,  hornby.FORWARD)
        except ValueError:
          print

    # close the connection with a Hornby Elite DCC controller 
    hornby.connection_close()

    print '''
    \t\t\t********************************
    \t\t\t      *****ENDING*****
    \t\t\t********************************
      '''

except KeyboardInterrupt:
    print "Stopping the program"
    
    t1.throttle(0,hornby.FORWARD) # stopping the train
    hornby.connection_close()
    
    print '''
    \t\t\t********************************
    \t\t\t      *****ENDING*****
    \t\t\t********************************
          '''

