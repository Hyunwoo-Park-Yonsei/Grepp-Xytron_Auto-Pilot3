#!/usr/bin/env python
# -*- coding: utf-8 -*-



import rospy, rospkg
import numpy as np
from xycar_msgs.msg import xycar_motor
from sensor_msgs.msg import LaserScan
from ar_track_alvar_msgs.msg import AlvarMarkers
from tf.transformations import euler_from_quaternion
import math
import time
from darknet_ros_msgs.msg import BoundingBoxes


import algorithm
import u_turn2
import yolo    
#import dqn2xycar

z
def callback_Lidar(data):
    global s
    ratio = 1.4027
    angle = 15
    idx = ratio * angle

    try:
        left_center = filtering(data.ranges[-8 + int(3 * idx): 8 + int(3 * idx)])
    except:
        left_center = 0.5
    try:
        right_center = filtering(data.ranges[-8 - int(3 * idx):+8 - int(3 * idx)])
    except:
        right_center = 0.5
    try:
        left = filtering(data.ranges[-8 + int(6 * idx):+8 + int(6 * idx)])
    except:
        left = 0.5
    try:
        right = filtering(data.ranges[-8 - int(6 * idx):+8 - int(6 * idx)])
    except:
        right = 0.5
    try:
        ctr = filtering(data.ranges[:8]+ data.ranges[-8:])
    except:
        ctr = 0.5

    s = list(map(int, [left*100, left_center*100, ctr*100, right_center*100, right*100]))

def back_drive(ang, cnt, speed) :
    
    global pub,motor_msg
    
    motor_msg.angle = -ang
    motor_msg.speed = -speed
    pub.publish(motor_msg)
    time.sleep(cnt*0.05)
    

    motor_msg.angle = ang
    motor_msg.speed = -speed
    pub.publish(motor_msg)
    time.sleep(cnt/2*0.05)

def drive(Angle, Speed): 
    global pub, motor_msg
    
    motor_msg.angle = Angle
    motor_msg.speed = Speed

    pub.publish(motor_msg)

def ArParking(arData,target_id):
    global car_state
    if target_id == arData["ID"]:
        
        if arData["DZ"] == 0 :
            car_angle = 0
        else :
            car_angle = math.atan(arData["DX"]/arData["DZ"])*(180/np.pi)
    
        speed = 15
    
        if distance < 0.8:
            speed = speed*0.6
        if car_state == "go":
            
            if distance <= 0.4 and abs(yaw) <= 5:
                car_state = "stop"
            elif distance <= 0.4 and abs(yaw) > 5:
                car_state = "back"
            else:
                drive(car_angle, speed)
        elif car_state == "back":
            if abs(yaw) <= 8:
                back_drive(yaw*2, 20, 20)
            elif 8 < yaw:
                back_drive(yaw*4, 30, 20)
            elif -8 > yaw:
                back_drive(yaw*4, 30, 20)
            car_state = "go"
        elif car_state == "stop":
            speed = 0
            angle = 0
            if distance > 0.4:
                car_state = "go"
            elif 0.01 < distance < 0.35 :
                back_drive(0, 10, 20)
            else:
                car_state = "change"


        


def callback_Ar(msg):
    global arData,yaw,distance
    
    for i in msg.markers:
        arData["DX"] = i.pose.pose.position.x
        arData["DY"] = i.pose.pose.position.y
        arData["DZ"] = i.pose.pose.position.z
        arData["AX"] = i.pose.pose.orientation.x
        arData["AY"] = i.pose.pose.orientation.y
        arData["AZ"] = i.pose.pose.orientation.z
        arData["AW"] = i.pose.pose.orientation.w
        arData["ID"] = i.id
    (_, pitch, _) = euler_from_quaternion((arData["AX"], arData["AY"], arData["AZ"], arData["AW"]))
    yaw = math.degrees(pitch)
    
    arData["DX"] = float(arData["DX"])
    arData["DY"] = float(arData["DY"])
    arData["DZ"] = float(arData["DZ"])
    
    distance = math.sqrt(pow(arData["DX"],2) + pow(arData["DZ"],2))


def state_change(state,s,ar_id):
    global car_state, distance, yaw

    if state == 0 and ar_id == 1:
        state = 1
    elif state == 1 and s[0] > 220:
        state = 2
    elif s[1] < 80 and s[2] < 100 and state == 2:
        state = 3
    elif state == 3 and s[4] > 220:
        state = 4
    elif state == 4 and s[3] < 80 and s[2] < 100:
        state = 5
    elif state == 5 and s[0] > 220:
        state = 6
    elif state == 6 and s[1] < 80 and s[2] < 100:
        state = 7
    elif state == 7 and abs(s[1]-s[3]) < 10 and s[2] <60 and s[1] != 50:
        state = 8
    #elif state == 8 and  s[4] <100 and s[2] <60 and s[1] >1:
    elif state == 8 and ar_id ==2:
        state = 9
    elif state ==9 and s[2] > 200:
        state = 10
    elif state == 10 and ar_id ==4:
        state = 11
    elif state == 11 and (s[0] > 150 or s[4] > 150) and ar_id == 9:
        state = 12
    elif state == 12 and car_state == "change":
        state = 13
    elif state == 13 and ar_id ==0:
        state = 14
        car_state = "go"
    elif state == 14 and distance <=0.5 and abs(yaw) < 5:
        state = 15
    
        
    
        
    
    return state
    
def callback_Yolo(data):
    global yolo_data
    boxes = data
    for i in range(len(boxes.bounding_boxes)) :
      yolo_data = [-1,-1,-1,-1]
      area = (boxes.bounding_boxes[i].xmax - boxes.bounding_boxes[i].xmin) * (boxes.bounding_boxes[i].ymax - boxes.bounding_boxes[i].ymin)
      #print(boxes.bounding_boxes[i].Class)
      if boxes.bounding_boxes[i].Class == "pottedplant" :
          yolo_data = ["pottedplant",boxes.bounding_boxes[i].xmin, boxes.bounding_boxes[i].xmax,area]


if __name__ == '__main__':
    yolo_data = [-1,-1,-1,-1]
    s = [50,50,50,50,50]
    rospy.init_node('main')
    arData = {"DX":0.0,"DY":0.0,"DZ":0.0,"AX":0.0,"AY":0.0,"AZ":0.0,"AW":0.0, "ID":-1}
    roll, pitch, yaw = 0, 0, 0
    distance = 2
    car_state = "go"
    
    
    state = 0

    

  
  
    pub = rospy.Publisher('xycar_motor',xycar_motor)
    
    rospy.Subscriber("/scan", LaserScan, callback_Lidar, queue_size = 1)
    rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback_Ar, queue_size =1)
    rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callback_Yolo, queue_size =1)
    
    
    rate = rospy.Rate(30)
    motor_msg = xycar_motor()

    AlgorithmDrive = algorithm.Algorithm(state,s)
    UTurn = u_turn2.u_turn(state,s)
    Yolo = yolo.Yolo(s, arData["ID"],yolo_data)
    #DQN = dqn2xycar.DQN()
    
    while not rospy.is_shutdown():

        state = state_change(state,s,arData["ID"])
        if 0 < state < 9:
            AlgorithmDrive.s = s
            AlgorithmDrive.state = state
            AlgorithmDrive.algorithm_drive()
            
            motor_msg = AlgorithmDrive.motor_msg
             
        
        elif state == 9:
            #uturn
            UTurn.sensor = s
            UTurn.state = state
            UTurn.Drive()
            motor_msg = UTurn.motor_msg
            state = UTurn.state
            

      
        elif state == 10:
            #DQN.Drive()
            #motor_msg.angle = DQN.angle
            #motor_msg.speed = DQN.speed
            #DQN
            motor_msg.angle = 0
            motor_msg.speed = 10
            
        elif state == 11:
            Yolo.sensor = s
            Yolo.arID = arData["ID"]
            Yolo.yolo_data = yolo_data
            Yolo.Drive()
            motor_msg = Yolo.motor_msg

            #YOLO
            
        elif state == 12:
            ArParking(arData,9)

        elif state == 13:
            motor_msg.angle = 0
            motor_msg.speed = 0
            pub.publish(motor_msg)
            time.sleep(3)
            
            motor_msg.angle = 45
            motor_msg.speed = -25
            pub.publish(motor_msg)
            time.sleep(4)

            motor_msg.angle = -10
            motor_msg.speed = 30
            pub.publish(motor_msg)
            time.sleep(1.5)
            
            motor_msg.angle = 12
            motor_msg.speed = 20
            pub.publish(motor_msg)
            time.sleep(2)
        
        elif state == 14:
            ArParking(arData,0)
        elif state == 15:
            motor_msg.angle = 0
            motor_msg.speed = 0

        

            
            
        print("mode",Yolo.mode)
        print("yolo_target", Yolo.yolo_target)
        print("yolo_detected", Yolo.yolo_data[0])
        print("direction!! ", Yolo.direction)
        print("location and area !!!!", yolo_data[1],yolo_data[2],yolo_data[3])
        print("state",state)
        print("AR",arData["ID"])
        print("yaw", yaw)
        #print("state", state)
        print("sensor", s)
        #print("motor", motor_msg.angle, motor_msg.speed)
        #print("arData", arData)
        #print("distance", distance)
        print()
        
        
        print(motor_msg.angle, motor_msg.speed)
        pub.publish(motor_msg)
        
        rate.sleep()


