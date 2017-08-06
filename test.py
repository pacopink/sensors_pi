#!/bin/env python
#coding:utf8

import gpio

gpio.start()
gpio.beeper.beep()
gpio.led.ledsOn(8, blink=True)

gpio.cease()
