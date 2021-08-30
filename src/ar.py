#!/usr/bin/env python
import rospy, math
import numpy
import time
from ar_track_alvar_msgs.msg import AlvarMarkers
from tf.transformations import euler_from_quaternion




class Ar:
    def __init__(self):
        self.arData = {"DX":0.0,"DY":0.0,"DZ":0.0,"AX":0.0,"AY":0.0,"AZ":0.0,"AW":0.0, "ID":0}
        self.roll, self.pitch, self.yaw = 0, 0, 0
        
    

r = rospy.Rate(10)


while not rospy.is_shutdown():
    (_, pitch, _) = euler_from_quaternion((arData["AX"], arData["AY"], arData["AZ"], arData["AW"]))
    yaw = math.degrees(pitch)
    print(arData["ID"])
    r.sleep()
