#!/usr/bin/python
#coding:utf8
# Paco Li: 2019-04-22
# Use REDIS to control PWM LEDS 
# tested on Raspberry Pi

import time
import traceback
import RPi.GPIO as GPIO
from gpio.sakshat import SAKSHAT
from gpio import * 
from gpio.beeper import Beeper 
import redis

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# redis parameters
HOST='localhost'
PORT=6379

#default values
FREQ = 200.0 #Hz 
DUTY_CYCLE = 100.0 #Percentage
UPDATE_INTERVAL_SECOND=0.1

# leds name and PIN, in this case I use a RGB combo LED, you can set to as many as your device supported
# the key-value of this dict is  name:pin# 
LEDS = {
        'red':22,
        'green':23,
        'blue':24
        }

class PwmLed:
    '''PWM LED class'''
    def __init__(self, name, pin, freq, duty_cycle, r):
        self.r = r
        self.pin = pin

        # init redis key-value
        self.name = name
        self.key_freq = name+":freq"
        self.key_duty = name+":duty"
        self.r.set(self.key_freq, freq)
        self.r.set(self.key_duty, duty_cycle)
        self.freq = float(self.r.get(self.key_freq))
        self.duty = float(self.r.get(self.key_duty))

        # start PWM LED with initail values
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.ChangeDutyCycle(self.duty)
        self.pwm.start(self.duty)

    def update(self):
        '''get freq and duty from redis by key, if changed, apply changes to pwm'''
        freq = float(self.r.get(self.key_freq))
        if freq != self.freq:
            print self.name, freq, self.freq
            self.pwm.ChangeFrequency(freq)
            self.freq = freq
        # duty should be checked to avoid exception
        duty = float(self.r.get(self.key_duty))
        if duty>=0.0 and duty <= 100.0 and duty != self.duty:
            print self.name, duty, self.duty
            self.pwm.ChangeDutyCycle(duty)
            self.duty = duty

    def close(self):
        self.pwm.stop()

if __name__=='__main__':
    # make arguements for all leds to init PwmLeds 
    r = redis.Redis(HOST, PORT)
    ARGS = map(lambda x: list(x) + [FREQ, DUTY_CYCLE, r], LEDS.items())
    pwmLeds = map(lambda x: PwmLed(*x), ARGS)
    # continuously update each pwm LED
    while True:
        for pl in pwmLeds:
            pl.update()
        time.sleep(UPDATE_INTERVAL_SECOND)
