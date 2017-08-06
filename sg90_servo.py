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

SERVO_PIN=22
GPIO.setup(SERVO_PIN, GPIO.OUT, initial=False)
  
  
p = GPIO.PWM(SERVO_PIN,50) #50HZ  
p.start(0)  
time.sleep(2)  

def Reset():
    #复位
    p.ChangeDutyCycle(1.5/20)
    time.sleep(0.02)
    p.ChangeDutyCycle(0)

def Move(angle, keep=0.3):
    dc = 10*angle/180+2.5
    p.ChangeDutyCycle(dc)
    time.sleep(keep)
    p.ChangeDutyCycle(0)

def Move2(angle):
    dc = 10*angle/180+2.5
    p.ChangeDutyCycle(dc)
    time.sleep(0.02)
    p.ChangeDutyCycle(0)


  
while(False):  
  for i in range(0,181,10):  
    p.ChangeDutyCycle(2.5 + 10 * i / 180) #设置转动角度  
    time.sleep(0.02)                      #等该20ms周期结束  
    p.ChangeDutyCycle(0)                  #归零信号  
    time.sleep(0.2)  
    
  for i in range(181,0,-10):  
    p.ChangeDutyCycle(2.5 + 10 * i / 180)  
    time.sleep(0.02)  
    p.ChangeDutyCycle(0)  
    time.sleep(0.2)

TIMES=8
INTERVAL=0.1
while(True):
    for i in xrange(0,TIMES):
        Move2(180)
        time.sleep(INTERVAL)
    for i in xrange(0,TIMES):
        Move2(90)
        time.sleep(INTERVAL)
    for i in xrange(0,TIMES):
        Move2(0)
        time.sleep(INTERVAL)
    for i in xrange(0,TIMES):
        Move2(90)
        time.sleep(INTERVAL)
#Move(90)
#while(True):
#    Reset()
