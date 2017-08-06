#!/usr/bin/python
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_1.py
# Measure distance using an ultrasonic module
#
# Author : Matt Hawkins
# Date   : 09/01/2013

# Import required Python libraries
import time
import traceback
import RPi.GPIO as GPIO
from gpio.sakshat import SAKSHAT
from gpio import * 
from gpio.beeper import Beeper 


# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 17
GPIO_ECHO    = 27

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

try:
    led.init()
    bp = Beeper()
    bp.start()
    while True:
        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()
        stop = start

        while GPIO.input(GPIO_ECHO)==0:
          start = time.time()

        while GPIO.input(GPIO_ECHO)==1:
          stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34300

        # That was the distance there and back so halve the value
        distance = distance / 2
        

        ######### echo ########
        if distance>200:
            led.writeByte(0x00)
        elif distance>150:
            led.writeByte(0x01)
        elif distance>80:
            led.writeByte(0x03)
            bp.beep(6)
        elif distance>30:
            led.writeByte(0x07)
            bp.beep(5)
        elif distance>25:
            led.writeByte(0x0f)
            bp.beep(4)
        elif distance>20:
            led.writeByte(0x1f)
            bp.beep(3)
        elif distance>15:
            led.writeByte(0x3f)
            bp.beep(2)
        elif distance>10:
            led.writeByte(0x7f)
            bp.beep(1)
        else:
            led.writeByte(0xff)
            bp.beep(0)

        
        if (distance<0.1 or distance>350):
            continue

        print "Distance : %.1f" % distance
        time.sleep(0.2)
        GPIO.output(GPIO_TRIGGER, False)
except Exception,e:
    print traceback.format_exc()
finally:
    # Reset GPIO settings
    GPIO.cleanup()
    bp.stop = True
    cease()

