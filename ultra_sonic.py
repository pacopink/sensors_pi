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
#
# Import required Python libraries
import time
import traceback
import RPi.GPIO as GPIO
from sensor import Sensor

class USonicSensor(Sensor):

    def getInData(self):
        return self.getDistance()

    def getDistance(self, retry=3):
        GPIO.output(self.pin_o, False)
        time.sleep(0.01)
        GPIO.output(self.pin_o, True)
        time.sleep(0.00001) #Send 10us pulse to trigger
        start = 0.0
        stop = start
        GPIO.output(self.pin_o, False)

        while GPIO.input(self.pin_i)==0:
            start = time.time()

        while GPIO.input(self.pin_i)==1:
            stop = time.time()

        # Calculate pulse length
        elapsed = stop-start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        # That was the distance there and back so halve the value
        distance = int(elapsed*34300/ 2)
        if (distance>0 and distance<600):
            return distance
        else:
            if retry>1:
                return self.getDistance(retry-1)
            else:
                return distance



if __name__=="__main__":
    import sys
    if len(sys.argv)<3:
        print "usage: %s [echo_pin] [trigger_pin]"%sys.argv[0]
        sys.exit(1)
    sensor = USonicSensor(int(sys.argv[1]), int(sys.argv[2]))
    while True:
        print sensor.getDistance()

