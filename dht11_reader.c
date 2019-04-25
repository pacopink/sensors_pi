//
//mydht11.c
//
#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>

typedef unsigned char uint8;
typedef unsigned int  uint16;
typedef unsigned long uint32;

//以32微秒为分界点，持续高电平时间超过这个时间的表示1，否则是0
#define HIGH_TIME 32 

int pinNumber; //GPIO PIN#, will be set from argv[1]
uint32 databuf;
uint8 *r1 = (uint8*)(&databuf)+3; //湿度整数部分
uint8 *r2 = (uint8*)(&databuf)+2; //湿度小数部分DHT11这个恒为0
uint8 *t1 = (uint8*)(&databuf)+1; //温度整数部分
uint8 *t2 = (uint8*)(&databuf);   //温度小数部分DHT11这个恒为0
uint8 crc;  //循环校验和

//等待一个目标电平
//为了避免无限循环等待，增加计数器，保证2ms左右一定会返回，
//如果是超时返回，CRC检测会发现错误
uint8 waitFor(uint8 target) 
{
    static int wait_counter;
    wait_counter = 0;
    while(digitalRead(pinNumber)!=target) {
        wait_counter++;
        delayMicroseconds(1);
        if (wait_counter>=2000) { 
            return 0;
        }
    }
    return 1;
}

uint8 readSensorData(void)
{
    uint8 i;

    pinMode(pinNumber,OUTPUT); // set mode to output
    digitalWrite(pinNumber, LOW); // output a low level 
    delay(20);
    digitalWrite(pinNumber, HIGH); // output a high level 
    pinMode(pinNumber, INPUT); // set mode to input

    delayMicroseconds(27);
    if(digitalRead(pinNumber)==LOW)  {
        //SENSOR ANS
        waitFor(HIGH);

        for(i=0;i<32;i++) {
            waitFor(LOW);
            waitFor(HIGH);
            delayMicroseconds(HIGH_TIME);
            databuf<<=1;
            if(digitalRead(pinNumber)==1) {
                databuf|=1;
            }
        }

        for(i=0;i<8;i++) {
            waitFor(LOW);
            waitFor(HIGH);
            delayMicroseconds(HIGH_TIME);
            if(digitalRead(pinNumber)==1) {
                crc<<=1;  
                crc|=1;
            } else {
                crc<<=1;  
            }
        }
        //校验结果，如果正确返回1，结果有效
        if (((*r1+*r2+*t1+*t2)&0xff) == crc) {
            return 1;
        } else { 
            return 0;
        }
    } else {
        return 0;
    }
}

//做10次获取尝试,任一次成功都返回
int readSensorCycle() {
    uint8 retry = 10;
    for(;retry>0; retry--) {
        if (readSensorData()) {
            //如果成功，立即返回
            return 1;
        }
        //如果失败，等100ms再重试
        delay(100);
    }
    return 0;
}


int main (int argc, char* argv[])
{
    int interval = 10;
    int times = 0;
    int count = 0;
    if (argc != 4) {
        printf("Usage: %s [pin#] [interval sec] [times]\n", argv[0]);
        return 1;
    }
    if (-1 == wiringPiSetupGpio()) {
        printf("Setup wiringPi failed!");
        return 1;
    }

    pinNumber = atoi(argv[1]);
    interval = atoi(argv[2]);
    times = atoi(argv[3]);

    pinMode(pinNumber, OUTPUT); // set mode to output
    digitalWrite(pinNumber, HIGH); // output a high level 

    while(1) {
        pinMode(pinNumber,OUTPUT); // set mode to output
        digitalWrite(pinNumber, HIGH); // output a high level 
        if(readSensorCycle())
        {
            count++;
            //printf("%d.%d,%d.%d\n", *r1, *r2, *t1, *t2);
            printf("%d,%d\n", *r1, *t1);
            if (times > 0  && count>=times) {
                return 0;
            }
            delay(interval*1000);
        } else {
            printf("failed: %d,%d\n", *r1, *t1);
        }
        databuf=0;
        crc=0;
    }
    return 1;
}
