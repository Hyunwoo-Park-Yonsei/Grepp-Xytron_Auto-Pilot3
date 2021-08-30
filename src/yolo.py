#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xycar_msgs.msg import xycar_motor


class Yolo:

    def __init__(self, sensor, arID, yolo_data):
        self.motor_msg = xycar_motor()
        self.sensor = sensor
        self.yolo_data = yolo_data
        self.arID = arID
        self.mode = 0
        self.yolo_target = "0"
        self.direction = 0
        self.ths = 35
    
    def directing(self):
        min_x = self.yolo_data[1]
        max_x = self.yolo_data[2]
        if abs(max_x-320) > abs(min_x -320):
            self.direction = 1
        elif abs(max_x -320) < abs(min_x -320):
            self.direction = -1


    def drive_right(self):
        right = self.sensor[4]
        steer = (right - self.ths)*1.5
        steer = min(steer, 50)
        return int(steer)
    
    def drive_left(self):
        left = self.sensor[0]
        steer = (self.ths - left)*1.5
        steer = max(-50, steer)
        return int(steer)
        
    def mode_change(self):
        if self.mode == 0 and 50 < self.sensor[2] < 80:
            self.mode = 1
            
        elif self.mode ==1:
            if self.sensor[2] > 200 and abs(self.sensor[1] - self.sensor[3] < 18):
                self.mode = 2
                
            if self.arID == 5:
                self.yolo_target = "bicycle"
            elif self.arID == 6:
                self.yolo_target = "pottedplant"
                
        elif self.mode ==2:
            if self.yolo_data[0] == self.yolo_target and (self.yolo_data[2] - self.yolo_data[1])> 70 and self.yolo_data[3] > 15000:
                self.mode = 3
                self.directing()
            elif self.yolo_data[0] != self.yolo_target and (self.yolo_data[2] - self.yolo_data[1])> 70 and self.yolo_data[3] > 15000:
                self.mode = 3
                self.directing()
                self.direction *= -1
                
        elif self.mode ==3:
            if self.yolo_data[0] == self.yolo_target and self.yolo_data[3] > 7000:
                self.mode = 4
                self.directing()

            elif self.yolo_data[0] != self.yolo_target and self.yolo_data[3] > 7000:
                self.mode = 4
                self.directing()
                self.direction *= -1



            
            
    def Drive(self):
        if self.yolo_data[0] == self.yolo_target and self.yolo_data[3] > 7000:
            self.directing()
        if self.yolo_data[0] != self.yolo_target and self.yolo_data[3] > 7000:
            self.directing()
            self.direction *= -1
        self.mode_change()
        if self.mode == 0:
            self.motor_msg.speed = 15
            self.motor_msg.angle = 0
        elif self.mode == 1:
            self.motor_msg.angle = -50
            self.motor_msg.speed = 10
        elif self.mode == 2:
            self.motor_msg.speed = 10
            self.motor_msg.angle = 0
            
        elif self.mode == 3:
            if self.direction == 1:
                self.motor_msg.angle = self.drive_right()*2
                self.motor_msg.speed = 10
            elif self.direction == -1:
                self.motor_msg.angle = self.drive_left()*2
                self.motor_msg.speed = 10
                
        elif self.mode ==4:
            if self.direction == 1:
                self.motor_msg.angle = self.drive_right()*2
                self.motor_msg.speed = 10
            elif self.direction == -1:
                self.motor_msg.angle = self.drive_left()*2
                self.motor_msg.speed = 10
                
        elif self.mode ==5:
            self.motor_msg.angle = 0
            self.motor_msg.speed = 0


            


