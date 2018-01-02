#======================================
#Lobot Servo Control Board LSC series
#======================================

import logging
import serial
import numpy as np

logger=logging.getLogger(__name__)

SERVO_NUM_LIMIT=32 #Limit the servo number is less than 32. This is NOT a MUST limit. The upper limit is 255
SPEED_LOWER_BOUND=100 #Setting action speed lower down level in ms, default 500ms
SPEED_UPPER_BOUND=600000 #Setting action speed upper level in ms, default is 10min
FRAME_HEAD=chr(0x55)+chr(0x55) #Two 0x55 to notify the board to receive data
CMD_SERVO_MOVE=0x03
CMD_ACTION_GROUP_RUN=0X06
CMD_ACTION_GROUP_STOP=0X07
CMD_ACTION_GROUP_SPEED=0X0B
CMD_GET_BATTERY_VOLTAGE=0X0F

class LSC_board(object):
	baudRate=9600
	serialPort="/dev/ttyS0"
	serialComm=serial.Serial(serialPort,baudRate)
	
	@classmethod
	def __init__(self,baudrate=9600, serialport="/dev/ttyS0"):
	 	self.baudRate=baudrate
	 	self.serialPort=serialport
	 	logger.debug("Setting serial communication @Baud rate="+str(self.baudRate)+"\nSerial Port:"+self.serialPort)
	 	
	#MultiServoMove is to move multiple servoes at the same time @ speed the caller assign. If the caller does NOT assign, default value is 1000ms(1s)
	#If success, the function will return 1. Otherwise will return:
	#-1: as input data error.
	#-2: Servo are beyond the limit
	#Parameters:
	#self: the object itself. Do NOT need to set in caller
	#speed: integer for the time all servo finish their movement. The time is measure in ms. Default value is 1000(1s)
	#servoData: a Nx2 matrix like the following:
	#	    [[servo ID 1, Move target 1],
	#	     [servo ID 2, Move target 2],
	#	     [...,...],
	#   	     [servo ID N, Move target N]]
	#servo ID #: means the ID number of servo (please refer to the board)
	#Move target #: means what position you want to move the servo to. value should be limited to a specific servo. Actually this is a pulsewidth value for PWM
	#controlled servoes. The pulse width is measured in ms. 
	#If you ONLY want to control 1 servo, you can call SingleServoMove(speed,[ID,Move Target]). If you want to use MultiServoMove function, you have to call like this:
	#returnVal=MultiServoMove(speed,[[ID,Move Target]])	
	def MultiServoMove(self,speed=1000,servoData=np.matrix([[],[]])):
	 if servoData.size==0:
	 	logger.debug("servoData is empty! No action done.")
	  	return -1
	 if servoData.ndim!=2:
	  	logger.debug("servoData MUST be an Nx2 matrix!")
	  	return -1
	 N=len(servoData)
	 if N>SERVO_NUM_LIMIT: 
	 	logger.debug("Servo number should be less than 32")
	 	return -2
	 
	 cmdString=FRAME_HEAD+chr(N*3+5)
	 print("Totally "+str(N)+"Servos")
	 if speed<SPEED_LOWER_BOUND:
	 	logger.debug("Speed setting too low! Using lower bound instead")
	 	actionSpeed=SPEED_LOWER_BOUND
	 if speed>SPEED_UPPER_BOUND:
	 	logger.debug("Speed setting is too slow! Using upper bound instead")
	 	actionSpeed=SPEED_UPPER_BOUND
	 actionSpeed=speed
	 cmdString+=chr(CMD_SERVO_MOVE)+chr(N)+chr(actionSpeed&0xFF)+chr(actionSpeed>>8)
	 
	 for servo in servoData:
	 	servoID=servo[0,0]
	 	if servoID>255:
	 		logger.debug("servo ID should be 0~255")
	 		return -2
	 	
	 	cmdString+=chr(servoID)
	 	angle=servo[0,1]
	 	cmdString+=chr(angle&0xFF)+chr(angle>>8)
	 outputString=""
	 for c in cmdString:
	 	outputString+=hex(ord(c))+":"
	 print(outputString)
	 
	 self.serialComm.write(cmdString)
	 return 1

	 	
	 
