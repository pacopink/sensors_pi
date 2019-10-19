#!/bin/python
#coding: utf-8
from sensor import Sensor
from ultra_sonic import USonicSensor
from redis_sensor import RedisSensor
from logger import logger
import time 
from multiprocessing.dummy import Pool
import threading

l = threading.Lock()

sensors = {
        "light": Sensor(24),
        "distance": USonicSensor(17, 27),
        }
rs = RedisSensor()

pool = Pool(4)

def refresh(x):
    k, s = x
    v = s.getInData()
    print "%s: %d"%(k,v)
    try:
        l.acquire()
        rs.updVal(k, "%d"%v)
    finally:
        if (l.locked()):
            l.release()
while True:
    pool.map(refresh, sensors.items())
    time.sleep(0.3)
    #for k,v in sensors.items():
    #    x = v.getInData()
    #    print "%s: %d"%(k,x)
    #    rs.updVal(k, "%d"%v.getInData())
    #    time.sleep(0.5)
