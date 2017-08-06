#!/bin/env python
#coding:utf8
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
DS = 6
SHCP = 19
STCP = 13

#x should be within (0~8)
def translate_leds_to_byte(x):
    byte=0
    for i in xrange(0,x):
        byte = (byte<<1)+0x01
    return byte

def translate_led_to_byte(x):
    byte=0x01<<x
    return byte
 
class Led(object):
    def __init__(self):
        GPIO.setup(DS, GPIO.OUT)
        GPIO.setup(SHCP, GPIO.OUT)
        GPIO.setup(STCP, GPIO.OUT)
        GPIO.output(DS, GPIO.LOW)
        GPIO.output(SHCP, GPIO.LOW)
        GPIO.output(STCP, GPIO.LOW)

        self.byte = 0
 
    @staticmethod
    def writeBit(data):
        GPIO.output(DS, data)
        GPIO.output(SHCP, GPIO.LOW)
        GPIO.output(SHCP, GPIO.HIGH)
 
    #写入8位LED的状态
    @staticmethod
    def writeByte(data):
        for i in range (0, 8):
            Led.writeBit((data >> i) & 0x01)
        #状态刷新信号
        GPIO.output(STCP, GPIO.LOW)
        GPIO.output(STCP, GPIO.HIGH)

    def turn_on(self, data):
        self.byte = data
        Led.writeByte(self.byte)
    def turn_off(self):
        self.byte = 0x00
        Led.writeByte(self.byte)

    def getData(self):
        return self.byte

    def doBlink(self, data):
        self.byte = data
        for i in xrange(0,5):
            Led.writeByte(data)
            time.sleep(0.1)
            Led.writeByte(0x00)
            time.sleep(0.1)
        Led.writeByte(data)

    def on(self, byte, blink=False):
        if blink:
            self.doBlink(byte)
        else:
            self.turn_on(byte)

    def ledsOn(self, x, blink=False):
        byte = translate_leds_to_byte(x)
        self.on(byte, blink)

    def ledOn(self, x, blink=False):
        '''to contrl led on or blink for 1 second, x should be within [0,8]'''
        byte = translate_led_to_byte(x)
        self.on(byte, blink)

if __name__=="__main__":
    try:
        led = Led()
        while True:
            #以下一组8个编码由一组二进制转换而成：
            #00000001,00000010,00000100,00001000,00010000,00100000,01000000,10000000
            #分别对应8个LED点亮状态
            for i in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
               led.doBlink(i)
               print led.getData()
               time.sleep(0.5)
            #LED组全开
            led.writeByte(0xff)
            led.on(8, True)
            time.sleep(1)
     
    except KeyboardInterrupt:
        print "except"
        #LED组全关
        led.writeByte(0x00)
        GPIO.cleanup()
