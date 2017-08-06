#!/bin/env python
#coding:utf8

from led import *
from beeper import *
from sakshat import SAKSHAT

beeper = None
SAKS = None
led = None
def start():
    global SAKS
    global beeper
    global led
    led = Led()
    SAKS = SAKSHAT()
    beeper = Beeper(SAKS)
    beeper.start()

def cease():
    led.writeByte(0) 
    SAKS.digital_display.off() #digital display off
    beeper.stop = True
    beeper.join()


