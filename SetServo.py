#!/usr/bin/python
#This example is using the GPIO pin directly from Raspberry Pi 3
import sys
import tty,termios
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM
from time import sleep
import argparse

def getch():
	fd=sys.stdin.fileno()
	old_settings=termios.tcgetattr(fd)
	try:
	 tty.setraw(fd)
	 ch=sys.stdin.read(1)
	finally:
	 termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
	return ch

parser=argparse.ArgumentParser(description='Servo Control Test')
parser.add_argument('integers',metavar='N',type=int,nargs='+',help='An integers for PWM channel pin number')
args=parser.parse_args()
channelPin=args.integers[0]

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


while True:
	pwm.setPWM(channelPin,0,pulseVal)
	pulseTime=float(pulseVal)/ticks*periodTime
	print('Current Pulse Width:'+str(pulseTime)+'us, Please input new pulse width')
	#ch=getch()
	#choices={'+':pulseVal+pulseDiv,'-':pulseVal-pulseDiv,'q':-1}
	#pulseVal=choices.get(ch,pulseVal)
	try:
	 pulseTime=float(raw_input())
	except:
	 print('Please input a float number!')
	if pulseTime<0:
	 break
	pulseVal=int(pulseTime*ticks/periodTime)
	#if pulseVal<0:
	# break
	if pulseVal>maxVal:
	 pulseVal=maxVal
	if pulseVal<minVal:
	 pulseVal=minVal
pulseTime=float(initVal)/ticks*periodTime
print('Setting mid pulse width:'+str(pulseTime)+'us')
pwm.setPWM(channelPin,0,initVal)
sleep(1)
pwm.setPWM(channelPin,0,0)

