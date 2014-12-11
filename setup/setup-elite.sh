#!/bin/bash
#run as root to set up /etc/udev/rules.d/10-elite.rules

echo 'ATTR{idVendor}=="04d8", ATTR{idProduct}=="000a", RUN+="/sbin/modprobe -q ftdi_sio vendor=0x04d8 product=0x000a"' > /etc/udev/rules.d/10-elite.rules

