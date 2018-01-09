from lobot import LSC_board as lsc
import numpy as np
lscboard=lsc()
servo=np.matrix([[1,1500],[2,1500],[3,1500],[4,1500],[5,1500],[6,1500]])
#servo=np.matrix([[4,500]])
lscboard.MultiServoMove(speed=10000,servoData=servo)
