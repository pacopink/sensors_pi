#!/bin/env python
#coding:utf8

import RPi.GPIO as GPIO
import time
from gpio.sakspins import *
import gpio
 
#初始化
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24,GPIO.IN)
    pass
 
#感应器侦测函数

def detct():
    #因为是仅仅试验，所以只让它循环运行100次
    nobody_count = 0
    for i in xrange(0,3600):
        #如果感应器针脚输出为True，则打印信息并执行蜂鸣器函数
        if GPIO.input(24) == True:
            nobody_count=0
            print "Someone isclosing!"
            gpio.led.writeByte(0xff)
        #否则将蜂鸣器的针脚电平设置为HIGH
        else:
            print "Noanybody!"
            #仅当连续20秒感应不到运动，灭灯
            #nobody_count+=1
            #if nobody_count>=20:
            gpio.led.writeByte(0x00)
        time.sleep(1)
 
init()
detct()
#脚本运行完毕执行清理工作
GPIO.cleanup()
