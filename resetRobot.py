#!/usr/bin/python
#This example is using the GPIO pin directly from Raspberry Pi 3
import sys
import tty,termios
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM
from time import sleep
import argparse

ticks=4096.0
periodTime=20000.0 #50Hz a period time is 20000us
midTime=1500.0 #Servo Middle: 1.5ms=1500us
minVal=int(1000/periodTime*ticks) #Minimum PWM length is 1ms=1000us
maxVal=int(2000/periodTime*ticks) #Maxium PWM length is 2ms=2000us
initVal=int(midTime*ticks/periodTime)
pulseDiv=1
pulseVal=initVal

pwm=PWM() #Initialize pwm
pwm.setPWMFreq(50) #Setting Freq as 50Hz
reset_order=[3,2,1,4,5,6]
for channelPin in reset_order:
	pwm.setPWM(channelPin,0,initVal)
	sleep(1)
	pwm.setPWM(channelPin,0,0)

