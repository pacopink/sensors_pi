#!/bin/env python
#coding:utf8

import RPi.GPIO as GPIO
class Sensor(object):
    def __init__(self, pin_in, pin_out=None):
        self.pin_i = pin_in
        self.pin_o = pin_out
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_i, GPIO.IN)
        if pin_out is not None:
            GPIO.setup(self.pin_o, GPIO.OUT)
    def getInData(self):
        return GPIO.input(self.pin_i)
