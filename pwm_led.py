#!/usr/bin/python
#coding:utf8

import time
import traceback
import RPi.GPIO as GPIO
from gpio.sakshat import SAKSHAT
from gpio import * 
from gpio.beeper import Beeper 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN=24

GPIO.setup(LED_PIN, GPIO.OUT)

#简单亮灯
if False:
    GPIO.output(LED_PIN, True)
    time.sleep(3)
    GPIO.output(LED_PIN, False)

if True:
    #PWM
    freq = 2000 #4000Hz
    p = GPIO.PWM(LED_PIN, freq)
    p.start(0)
    try:
        while True:
            for i in xrange(0,6):
                dutyCycle = i*20
                print dutyCycle
                p.ChangeDutyCycle(dutyCycle)
                #p.ChangeFrequency(2000)
                time.sleep(1)
            for i in xrange(0,5):
                dutyCycle = (5-i)*20
                print dutyCycle
                p.ChangeDutyCycle(dutyCycle)
                #p.ChangeFrequency(2000)
                time.sleep(1)

    except:
        p.stop()
