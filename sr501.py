#!/bin/env python
#coding:utf8

import RPi.GPIO as GPIO
import time
from gpio.sakspins import *
import gpio

PIN_NUM=22
 
#初始化
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_NUM,GPIO.IN)
 
#感应器侦测函数

def detect2Redis(redis_host, redis_port, interval, redis_key):
    import redis
    r = redis.Redis(redis_host, redis_port)
    ttl = int(interval*2)
    if ttl<2:
        ttl=2
    
    last_st = 0
    while True:
        st = 0
        if GPIO.input(PIN_NUM)==True:
            st = 1
        if (st!=last_st):
            last_st = st
            print "%s - %d"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), st)
        r.set(redis_key, str(st))
        r.expire(redis_key, ttl)
        time.sleep(interval)

def detct():
    #因为是仅仅试验，所以只让它循环运行100次
    nobody_count = 0
    for i in xrange(0,3600):
        #如果感应器针脚输出为True，则打印信息并执行蜂鸣器函数
        if GPIO.input(PIN_NUM) == True:
            nobody_count=0
            print "Someone detected!"
            #gpio.led.writeByte(0xff)
        #否则将蜂鸣器的针脚电平设置为HIGH
        else:
            print "No body!"
            #仅当连续20秒感应不到运动，灭灯
            #nobody_count+=1
            #if nobody_count>=20:
            #gpio.led.writeByte(0x00)
        time.sleep(1)
 
if __name__=="__main__":
    try:
        init()
        #detct()
        detect2Redis("localhost", 6379, 0.1, "SR501")
    except Exception,e:
        print e
        pass
    finally:
        #脚本运行完毕执行清理工作
        GPIO.cleanup()
