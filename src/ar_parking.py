#!/usr/bin/env python
import rospy, math
import numpy
import time
from ar_track_alvar_msgs.msg import AlvarMarkers
from tf.transformations import euler_from_quaternion
from xycar_msgs.msg import xycar_motor


msg = xycar_motor()



class ArParking():
    def __init__(self,arData):
        self.car_state = "go"
        self.arData = arData
        

    def Drive(self):
        if arData["DZ"] == 0 :
            car_angle = 0
        else :
            car_angle = math.atan(arData["DX"]/arData["DZ"])*(180/numpy.pi)
    
        speed = 10
    
        if distance < 0.8:
            speed = speed*0.6
        if car_state == "go":
            drive(car_angle, speed)
            if distance <= 0.45 and abs(yaw) <= 5:
                car_state = "stop"
            elif distance <= 0.45 and abs(yaw) > 5:
                car_state = "back"
        elif car_state == "back":
            if abs(yaw) <= 4.5:
                back_drive(yaw*2, 20, 20)
            elif 5 < yaw:
                back_drive(yaw*yaw, 35, 20)
            elif -5 > yaw:
                back_drive(-yaw*yaw, 35, 20)
                car_state = "go"
        else:
            speed = 0
            angle = 0
            if distance > 0.45:
                car_state = "go"
            elif 0.01 < distance < 0.30 :
                back_drive(0, 10, 20)
      

    
    
    r.sleep()
    
    