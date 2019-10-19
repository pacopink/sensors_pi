#!/usr/bin/python
#coding:utf8
# Paco Li: 2019-04-22
# Use REDIS to control PWM LEDS freq and duty_cycle
# tested on Raspberry Pi import time
import time, traceback

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

import redis
# redis parameters
HOST='localhost'
PORT=6379

#default values
FREQ = 200.0 #Hz 
DUTY_CYCLE = 100.0 #Percentage
UPDATE_INTERVAL_SECOND=0.1

# leds name and PIN, in this case I use a RGB combo LED, 
# you can set as many as your device supported
# the key-value of this dict is  name:pin# 
LEDS = {
        'red':22,
        'green':23,
        'blue':24
        }

class PwmLed:
    '''PWM LED class'''
    def __init__(self, r, freq, duty_cycle, name, pin):
        # save redis connection, will be used later
        self.r = r
        # init redis key-value
        self.name = name
        self.key_freq = name+":freq"
        self.key_duty = name+":duty"
        self.r.set(self.key_freq, freq)
        self.r.set(self.key_duty, duty_cycle)
        self.freq = float(self.r.get(self.key_freq))
        self.duty = float(self.r.get(self.key_duty))
        # start PWM LED with initail values
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, self.freq)
        self.pwm.ChangeDutyCycle(self.duty)
        self.pwm.start(self.duty)

    def update(self):
        '''get freq and duty from redis by key, apply changes to pwm if any change'''
        try:
            freq = float(self.r.get(self.key_freq))
            if freq != self.freq:
                print self.name, freq, self.freq
                self.pwm.ChangeFrequency(freq)
                self.freq = freq
            # duty should be checked to ensure valid value range
            duty = float(self.r.get(self.key_duty))
            if duty>=0.0 and duty <= 100.0 and duty != self.duty:
                print self.name, duty, self.duty
                self.pwm.ChangeDutyCycle(duty)
                self.duty = duty
        except Exception,e:
            traceback.print_exc()

    def close(self):
        self.pwm.stop()
        self.r.delete(self.key_freq)
        self.r.delete(self.key_duty)

if __name__=='__main__':
    r = redis.Redis(HOST, PORT) # make a redis connection
    # init a PWM LED set
    pwmLeds = map(lambda x: PwmLed(r, FREQ, DUTY_CYCLE, *x), LEDS.items())
    # continuously update each pwm LED
    try:
        while True:
            time.sleep(UPDATE_INTERVAL_SECOND)
            for pl in pwmLeds:
                pl.update()
    except Exception,e:
        print e
        traceback.print_exc()
        map(lambda pl: pl.close(), pwmLeds)
