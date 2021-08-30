#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
from env.xycarRL import *
from rosModule import *

class DQN():
    def __init__(self):
        self.state = 0
        self.xycar = learning_xycar(False)
        self.ros_module = rosmodule()
    
        self.hidden_layer = self.ros_module.get_hidden_size()
        self.lidar_cnt = self.ros_module.get_use_lidar_cnt()
        self.xycar.set_lidar_cnt(lidar_cnt)
        self.xycar.set_hidden_size(hidden_layer)
    
        self.state_select = {
            "car sensor" : True,
            "car yaw" : False,
            "car position" : False,
            "car steer" : True
        }
    
        self.xycar.state_setup(self.state_select)
        self.xycar.ML_init("DQN")
    
        self.view_epi = self.ros_module.get_view_epi()
        self.xycar.load_model(view_epi)
    
        time.sleep(0.5)
    
        self.angle = 0
        self.max_angle = 30
        self.handle_weights = 6.6

    
        self.state = []
        
        if self.state_select["car sensor"]:
            self.use_lidar_cnt = rospy.get_param('~use_lidar_cnt', 5)
            for _ in range(use_lidar_cnt):
                self.state.append(0.0)
    
        if self.state_select["car yaw"]:
            self.state.append(0.0)
            self.state.append(0.0)
    
        if self.state_select["car position"]:
            self.state.append(0.0)
            self.state.append(0.0)
    
        if state_select["car steer"]:
            self.state.append(0.0)
        self.max_speed = 20
        self.state = np.array(self.state)
        self.speed = 0
        
        self.action = xycar.get_action_viewer(state)
        self.start_time = time.time()

    def next_state_rtn(self,laser_msg, angle):
        ratio = 213.33
        #ratio = 350
        increment = 0.71287129
        idx = [125,63,0,-63,-125]
        #idx = [0, 44, 89, 134, 179]
        current_ipt = []
        for i in range(len(idx)):
            #real_idx = int(round(float(idx[i]) / increment))
            if idx[i] == -125: 
                tmp = [laser_msg[idx[i]], laser_msg[idx[i]+2], laser_msg[idx[i]+4]]
            elif idx[i] == 125:
                tmp = [laser_msg[idx[i]-4], laser_msg[idx[i]-2], laser_msg[idx[i]]]
            else:
                tmp = [laser_msg[idx[i]-2], laser_msg[idx[i]], laser_msg[idx[i]+2]]
            current_ipt.append(max(tmp))
    
       
        current_ipt.append(angle)
        rtn = np.array(current_ipt)
        
    
        for j in range(len(current_ipt)-1):
            rtn[j] *= ratio
            #rtn[j] /= -1645
        print(rtn)
        return rtn
        
        
    
    def Drive(self):
            

        if (time.time() - self.start_time) > 0.2:
            action = self.xycar.get_action_viewer(state)
            self.start_time = time.time()

        if self.action == 2:
            self.angle += self.handle_weights
            self.speed = -15
        elif action == 0:
            self.angle -= self.handle_weights
            self.speed = -15
        elif self.action == 1:
            self.angle = 0
            self.speed = -15
        elif self.action == 5:
            self.angle += self.handle_weights
            self.speed = 20
        elif self.action == 3:
            self.angle -= self.handle_weights
            self.speed = 20
        elif self.action == 4:
            self.angle = 0
            self.speed = 20
        elif self.action == 6:
            self.angle = 0
            self.speed = 0
        print("action: ",action)
        self.angle = max(-self.max_angle, min(self.angle, self.max_angle))
        self.ros_module.auto_drive(int(float(self.angle)*(5.0/3.0)), min(self.speed, self.max_speed))
            #min(speed, max_speed)
        next_state = self.next_state_rtn(self.ros_module.get_laser_msg(), self.angle)

        self.state = next_state

