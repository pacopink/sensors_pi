#!/bin/env python
#coding:utf8

import os,sys
import time, datetime

#调用dht11_reader获取一次温湿度测量值
CMD="./dht11_reader 24 1 1"
def get_data_from_sensor():
    with os.popen(CMD, 'r') as p:
        x = p.read()
        x = x.strip()
        return x

last = 0
INTERVAL=10 #5min记录一次
while True:
    now = int(time.time())
    if now%INTERVAL<3 and now-last>=INTERVAL:
        #sys.stdout.write("%s,%s\n"%(time.strftime("%Y%m%d%H%M%S", time.localtime(now)), get_data_from_sensor()))
        sys.stdout.write("%d,%s\n"%(int(now), get_data_from_sensor()))
        sys.stdout.flush()
        last = now
    time.sleep(0.1)
