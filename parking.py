#!/usr/bin/env python

from ultra_sonic import USonicSensor
import redis

ECHO_PIN=17
TRIGGER_PIN=27


DISTANCE_THRESHOLD = 15

REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_AUTH=''

def set_red(r):
    r.set("red:freq", 100)
    r.set("red:duty", 100.0)
    r.set("blue:freq", 100)
    r.set("blue:duty", 0.0)
    r.set("green:freq", 100)
    r.set("green:duty", 0.0)

def set_green(r):
    r.set("red:freq", 100)
    r.set("red:duty", 0.0)
    r.set("blue:freq", 100)
    r.set("blue:duty", 0.0)
    r.set("green:freq", 100)
    r.set("green:duty", 100.0)


if __name__=="__main__":
    import sys
    import time
    sensor = USonicSensor(ECHO_PIN, TRIGGER_PIN)
    r = redis.Redis(REDIS_HOST, REDIS_PORT, password = REDIS_AUTH if len(REDIS_AUTH)>0 else None)
    is_red = None
    while True:
        # get distance per second, if far enough, the parking slot is free, light green otherwise light red
        time.sleep(1.0)
        dist = sensor.getDistance()
        print "distance = %d cm"%(dist)
        if dist<20:
            if is_red is None or not is_red:
                set_red(r)
                is_red = True
        else:
            if is_red is None or is_red:
                set_green(r)
                is_red = False



