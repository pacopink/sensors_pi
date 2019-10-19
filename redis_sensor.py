#!/bin/env python
#coding:utf8

import redis

class RedisSensor:
    def __init__(self, host="localhost", port=6379, prefix="sensor_"):
        self.prefix=prefix 
        self.r = redis.Redis(host, port)
        self.r.ping()

    def updVal(self, key, val, ttl=10):
        kk = self.prefix+key
        self.r.set(kk, val)
        self.r.expire(kk, ttl)

    def getVal(self):
        return self.r.get(self.key)

    def getAllSensors(self):
        keys = self.r.keys(self.prefix+"*")
        vals = map(lambda k:self.r.get(k), keys)
        h = dict()
        for k,v in zip(keys, vals):
            h[k.replace(self.prefix,"")] = v #get rid of prefix
        return h

class RedisValMonitor:
    def __init__(self, r, key):
        self.r = r
        self.key = key
        self.val = r.get(key)

    def getVal(self):
        return self.val

    def setVal(self, val):
        self.r.set(self.key, val)
        self.val = val

    def runWithVal(self, callback, if_change=False):
        val = self.r.get(self.key)
        #skip if there is no change in this key
        if if_change and val == self.val:
            return
        self.val = val
        callback(self.val)


if __name__=="__main__":
    from logger import logger
    rs1 = RedisSensor()
    rs1.updVal("light", "1")
    rs1.updVal("sound", "2")
    rs1.updVal("dist", "3")
    logger.debug(rs1.getAllSensors())
