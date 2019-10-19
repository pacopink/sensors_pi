#!/bin/env python
#coding:utf8

import gpio
import time
import sys
from sensor import Sensor
from logger import logger

SENSOR_PIN=int(sys.argv[1])
print(SENSOR_PIN)

if __name__=="__main__":
    light = Sensor(SENSOR_PIN)
    lastStat = light.getInData()
    while True:
        stat = light.getInData()
        if (lastStat!=stat):
            logger.debug("light stat:%d", stat)
            lastStat = stat
        time.sleep(0.05)

