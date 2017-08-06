#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 16:01:59 2014

@author: pi
"""

import time
def delay(i):
    k=0
    for j in xrange(0,i):
        k+=1
n=5000
j=0

def dummy(i, j):
    k=i
    m=j
a=time.time()
dummy(1,2)
c=time.time()
print c-a

a=time.time()
i=0
while i<3:
    i+=1
c=time.time()
d=c-a
print d

a=time.time()
for i in xrange(0,n):
    j+=1
c=time.time()
d=c-a
print d

a=time.time()
delay(n)
c=time.time()
d=c-a
print d


def dummy_delay(c):
    for i in xrange(0,c):
        pass

def time_delay_cycle(cycle=10):
    a=time.time()
    dummy_delay(n)
    c=time.time()
    d=c-a
    print d

time_delay_cycle(1)
