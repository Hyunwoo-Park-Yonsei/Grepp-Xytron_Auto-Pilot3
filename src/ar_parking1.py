#!/usr/bin/env python
import rospy, math
import numpy
import time
from ar_track_alvar_msgs.msg import AlvarMarkers
from tf.transformations import euler_from_quaternion
from xycar_msgs.msg import xycar_motor
msg = xycar_motor()

def back_drive(ang, cnt, speed) :
    
    global pub
    
    for c in range(cnt):
      msg.angle = -ang
      msg.speed = -speed
      pub.publish(msg)
      time.sleep(0.1)
    
    for c in range(cnt/2):
      msg.angle = ang
      msg.speed = -speed
      pub.publish(msg)
      time.sleep(0.1)


def drive(Angle, Speed): 
    global pub
    
    msg.angle = Angle
    msg.speed = Speed

    pub.publish(msg)


arData = {"DX":0.0,"DY":0.0,"DZ":0.0,"AX":0.0,"AY":0.0,"AZ":0.0,"AW":0.0, "ID":0}
roll, pitch, yaw = 0, 0, 0

def callback(msg):
    global arData
    
    for i in msg.markers:
        arData["DX"] = i.pose.pose.position.x
        arData["DY"] = i.pose.pose.position.y
        arData["DZ"] = i.pose.pose.position.z
        arData["AX"] = i.pose.pose.orientation.x
        arData["AY"] = i.pose.pose.orientation.y
        arData["AZ"] = i.pose.pose.orientation.z
        arData["AW"] = i.pose.pose.orientation.w
        arData["ID"] = i.id

rospy.init_node('ar_info_print')
rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback, queue_size =1)
pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
car_state = "go"
r = rospy.Rate(30)
while not rospy.is_shutdown():
    (roll, pitch, yaw) = euler_from_quaternion((arData["AX"], arData["AY"], arData["AZ"], arData["AW"]))
    
    real_pitch = yaw
    
    roll = math.degrees(roll)
    yaw = math.degrees(pitch)
    pitch = math.degrees(real_pitch)


    arData["DX"] = float(arData["DX"])
    arData["DY"] = float(arData["DY"])
    arData["DZ"] = float(arData["DZ"])
    
    distance = math.sqrt(pow(arData["DX"],2) + pow(arData["DZ"],2))
    
    speed = 0
    
    angle = 0
    
    if arData["DZ"] == 0 :
      car_angle = 0
    else :
      car_angle = math.atan(arData["DX"]/arData["DZ"])*(180/numpy.pi)

    speed = 20

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
    
    print("car_angle:",car_angle)
    print("distance:", distance)
    print("car_state:",car_state)
    print(arData["ID"])
    print("car_yaw:", yaw)
    
    
    r.sleep()
    
    