#!/bin/bash python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 14:24:43 2014
 
@author: pi
"""
 
import RPi.GPIO as gpio
import time
PIN=24
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
time.sleep(1)
data=[]
def delay(i): #20*i usdelay
    a=0
    for j in range(i):
        a+1
j=0
#start work
gpio.setup(PIN,gpio.OUT)
#gpio.output(PIN,gpio.HIGH)
#delay(10)
gpio.output(PIN,gpio.LOW)
time.sleep(0.02)
gpio.output(PIN,gpio.HIGH)

for i in xrange(0, 100):
    data.append(0)
#below will generate a 40us delay to trigger the sensor
i=0
while i<28:
    i+=1

  
#wait to response
gpio.setup(PIN,gpio.IN)

while gpio.input(PIN)==1:
    continue
print "XXX"
 
time_out=100
time_edge=4
bit=0 
while gpio.input(PIN)==0:
    data[bit]=1
    continue
 
bit=1
k=0
while gpio.input(PIN)==1:
    k+=1
    if k>time_out:break
if k>time_edge:
    data[bit]=1
else:
    data[bit]=0

bit=2 
while gpio.input(PIN)==0:
    data[bit]=1
    continue
 
bit=3
k=0
while gpio.input(PIN)==1:
    k+=1
    if k>time_out:break
if k>time_edge:
    data[bit]=1
else:
    data[bit]=0

print data

while gpio.input(PIN)==0:
    continue

while gpio.input(PIN)==1:
    continue
#get data
 
while j<40:
    k=0
    m=0
    while gpio.input(PIN)==0:
        m+=1
        if m>1000:
            print "L_TO"
            break
    while gpio.input(PIN)==1:
        k+=1
        if k>100:
            print "TKO"
            break
    if k<4:
        data.append(0)
    else:
        data.append(1)
    j+=1
 
print "Sensor is working"
#get temperature
humidity_bit=data[0:8]
humidity_point_bit=data[8:16]
temperature_bit=data[16:24]
temperature_point_bit=data[24:32]
check_bit=data[32:40]
 
humidity=0
humidity_point=0
temperature=0
temperature_point=0
check=0
 
 
 
for i in range(8):
    humidity+=humidity_bit[i]*2**(7-i)
    humidity_point+=humidity_point_bit[i]*2**(7-i)
    temperature+=temperature_bit[i]*2**(7-i)
    temperature_point+=temperature_point_bit[i]*2**(7-i)
    check+=check_bit[i]*2**(7-i)
 
tmp=humidity+humidity_point+temperature+temperature_point
if check==tmp:
    print "temperature is ", temperature,"wet is ",humidity,"%"
else:
    print "something is worong the humidity,humidity_point,temperature,temperature_point,check is",humidity,humidity_point,temperature,temperature_point,check
