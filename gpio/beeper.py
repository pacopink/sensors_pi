#!/bin/env python
#coding:utf-8
from sakshat import SAKSHAT
import threading
import time

class Beeper(threading.Thread):
    '''to make it beep and blink at the same time, this should be in another thread'''
    def __init__(self, SAKS):
        threading.Thread.__init__(self)
        self.SAKS=SAKS
        self.beep_flag = False
        self.stop = False
        self.level = 0
        self.alarm_lvl = [
                (0.06,0.000,5),
                (0.05,0.01,5),
                (0.03,0.01,5),
                (0.035,0.02,5),
                (0.02,0.02,5),
                (0.01,0.03,5),
                (0.005,0.03,5),
                ]

    def beep(self, lvl):
        self.level = lvl
        self.beep_flag = True

    def beep(self):
        self.level = 4
        self.beep_flag = True

    def run(self):
        try:
            while not self.stop:
                if self.beep_flag:
                    self.beep_flag = False
                    self.do_beep(self.level)
                time.sleep(0.05)
        finally:
            self.SAKS.buzzer.beepAction(0.01, 0.02, 0)

    def do_beep(self, level):
        if level < 0:
            level = 0
        if level >= len(self.alarm_lvl):
            level = len(self.alarm_lvl)-1 
        bb = self.alarm_lvl[level]
        print bb
        self.SAKS.buzzer.beepAction(*bb)
