#!/bin/env python
#coding:utf8

import gpio
import RPi.GPIO as GPIO
import time

SENSOR_PIN=24
LED_PIN=17


def init():
    GPIO.setwarnings(False)
    GPIO.setup(SENSOR_PIN,GPIO.IN)
    GPIO.setup(LED_PIN,GPIO.OUT)

if __name__=="__main__":
    try:
        gpio.start()
        init()
        last_state = True
        gpio.led.turn_on(0x01)
        led_on = False
        while True:
            while True:
               state = GPIO.input(SENSOR_PIN) 
               if (last_state!=state):
                   print "state switch from %d to %d"%(last_state, state)
                   #last_state = state
                   x = gpio.led.getData()
                   print x
                   x = x<<1
                   if x>0x80:
                       x=0x01
                   gpio.led.turn_on(x)

                   if led_on:
                       GPIO.output(LED_PIN, False)
                       led_on = False
                   else:
                       GPIO.output(LED_PIN, True)
                       led_on = True
                    
                   #if gpio.led.getData()>0:
                   #    gpio.led.turn_off()
                   #    GPIO.output(LED_PIN, True)
                   #else:
                   #    gpio.led.turn_on(0xff)
                   #    GPIO.output(LED_PIN, False)
                   break
               time.sleep(0.0001)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.output(LED_PIN, False)
        gpio.cease()
