#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################
# 프로그램명 : hough_drive.py
# 작 성 자 : 자이트론
# 생 성 일 : 2020년 08월 12일
# 수 정 일 : 2021년 03월 16일
# 검 수 인 : 조 이현
# 본 프로그램은 상업 라이센스에 의해 제공되므로 무단 배포 및 상업적 이용을 금합니다.
####################################################################

import rospy, rospkg
import numpy as np
from xycar_msgs.msg import xycar_motor
from sensor_msgs.msg import LaserScan


import cv2


class Algorithm:
    def __init__(self,state,s):
        self.state = state
        self.ths = 55
        self.motor_msg = xycar_motor()
        self.motor_msg.speed = 15
        self.s = s
        
    
    def drive_right(self,sensors):
        right = sensors[4]
        steer = (right - self.ths)*1.5
        steer = min(steer, 45)
        return steer
    
    def drive_left(self,sensors):
        left = sensors[0]
        steer = (self.ths - left)*1.5
        steer = max(-45, steer)
        return steer

    def drive_left2(self,sensors):
        left = sensors[0]
        steer = (75 - left)*1.5
        steer = max(-45, steer)
        return steer

    def rotate_left(self):
        return -30
    
    def rotate_right(self):
        return 35
        
    def straight(self,sensors):
        left = sensors[0]
        right = sensors[1]
        steer = right - left
        return steer
    
    def stopping(self):
        return 0


    def algorithm_drive(self):
        #오른쪽이 양수
        steer = 0
        if self.state == 1:
            steer = self.drive_right(self.s)  
        if self.state == 2:
            steer = self.rotate_left()  
        if self.state == 3:
            steer = self.drive_left(self.s)  
        if self.state == 4:
            steer = self.rotate_right()
        if self.state == 5:
            steer = self.drive_right(self.s) 
        if self.state == 6:
            steer = self.rotate_left()  
        if self.state == 7:
            steer = self.drive_left2(self.s)
        if self.state == 8:
            steer = self.stopping()
            self.motor_msg.speed = 0
        self.motor_msg.angle = steer
        print('algorithm_drive')
                        

        



'''
global ths
ths = 55

def drive_right(sensors):
    right = sensors[4]
    steer = (right - ths)*1.5
    steer = min(steer, 45)
    return steer

def drive_left(sensors):
    left = sensors[0]
    steer = (ths - left)*1.5
    steer = max(-45, steer)
    return steer

def drive_left2(sensors):
    left = sensors[0]
    steer = (75 - left)*1.5
    steer = max(-45, steer)
    return steer

def rotate_left():
    return -30

def rotate_right():
    return 40

def straight(sensors):
    left = sensors[0]
    right = sensors[1]
    steer = right - left
    return steer

def stopping():
    return 0

def state_change(sensor):
    global state 
    if state == 1 and sensor[0] > 220:
        state = 2
    if sensor[1] < 80 and sensor[2] < 100 and state == 2:
        state = 3
    if state == 3 and sensor[4] > 220:
        state = 4
    if state == 4 and sensor[3] < 80 and sensor[2] < 100:
        state = 5
    if state == 5 and sensor[0] > 220:
        state = 6
    if state == 6 and sensor[1] < 80 and sensor[2] < 100:
        state = 7
    if state == 7 and  sensor[4] <100 and sensor[2] < 50:
        state = 8




    return state


def filtering(arr):
    total = 0
    count = 0
    for i in arr:
        if i != 0:
            total +=i
            count +=1
    return total/count

def callback(data):
    global s
    ratio = 1.4027
    angle = 15
    idx = ratio * angle


    left_center = filtering(data.ranges[-8 + int(3 * idx): 8 + int(3 * idx)])
    right_center = filtering(data.ranges[-8 - int(3 * idx):+8 - int(3 * idx)])
    left = filtering(data.ranges[-8 + int(6 * idx):+8 + int(6 * idx)])
    right = filtering(data.ranges[-8 - int(6 * idx):+8 - int(6 * idx)])
    ctr = filtering(data.ranges[:5]+ data.ranges[-5:])

    s = list(map(int, [left*100, left_center*100, ctr*100, right_center*100, right*100]))
    #print(s)
    


#    left_sensors = data.ranges[:int(9*idx)]
#    right_sensors = data.ranges[-int(9*idx):]
    
#    sensors = []
#    sensors += right_sensors
#   sensors += left_sensors

#    img = np.ones(1000*1000)
#    img = np.reshape(img,(1000,1000))
#    center = [950,500]
    
    #x.y 바꿔야함 >>>>> ||||||| (아래)
#    cv2.rectangle(img,(center[1]-5,center[0]-5),(center[1]+5,center[0]+5),(0,0,255),3)
#    angle =2*np.pi/505

#    white_img = img.copy()
#    for i,sensor in enumerate(sensors):
#        new_x = int(center[1]+np.cos(angle*i)*sensor*100)
#        new_y = int(center[0]-np.sin(angle*i)*sensor*100)

#        cv2.circle(white_img, (new_x, new_y), 4, 0, -1)
#    cv2.imshow('test', white_img)
#    cv2.waitKey(1)'''


'''

def algorithm_drive(pub,state):
    global s
    
    motor_msg = xycar_motor()
    #오른쪽이 양수
    steer = 0
    try:
      steer = drive_right(s)
    except:
      pass
    motor_msg.speed = 15
    
    if state == 1:
        steer = drive_right(s)  
    if state == 2:
        steer = rotate_left()  
    if state == 3:
        steer = drive_left(s)  
    if state == 4:
        steer = rotate_right()
    if state == 5:
        steer = drive_right(s) 
    if state == 6:
        steer = rotate_left()  
    if state == 7:
        steer = drive_left2(s)
    if state == 8:
        steer = stopping()
        motor_msg.speed = 0
        

    
    motor_msg.angle = steer
    pub.publish(motor_msg)


if __name__ == '__main__':
  global s
  state = 1
  rospy.init_node('lidar_algorithm')
  s= []
  rospy.Subscriber("/scan", LaserScan, callback, queue_size = 10)
  pub = rospy.Publisher('xycar_motor',xycar_motor)
  rate = rospy.Rate(30)
  
  while pub.get_num_connections() == 0:
      continue
  
  while not rospy.is_shutdown():
      if len(s) > 0:
        state = state_change(s)
        print(state)
        algorithm_drive(pub,state)
      
      
      rate.sleep()
'''

