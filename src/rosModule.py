#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import LaserScan
from xycar_msgs.msg import xycar_motor

class rosmodule:
    laser_msg = None
    ack_msg = xycar_motor()
    ack_msg.header.frame_id = 'odom'

    def __init__(self):
        rospy.init_node('dqn2xycar1', anonymous = True)
        self.launch_data_read()
		
        rospy.Subscriber('/scan', LaserScan, self.lidar_callback)
        self.ackerm_publisher = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
   
    def auto_drive(self, steer_val, car_run_speed):
        self.ack_msg.header.stamp = rospy.Time.now()
        self.ack_msg.angle = steer_val
        self.ack_msg.speed = car_run_speed
        self.ackerm_publisher.publish(self.ack_msg) 
    
    def lidar_callback(self, data):
        self.laser_msg = data.ranges

    def launch_data_read(self):
        self.hidden_size = []
        hidden_size_str = rospy.get_param('~hidden_size', '[]')
        self.view_epi = rospy.get_param('~view_epi', 0)
        self.use_lidar_cnt = rospy.get_param('~use_lidar_cnt', 5)
        hidden_size_str_list = hidden_size_str.replace('[','').replace(']','').split(",")

        for i in hidden_size_str_list:
            self.hidden_size.append(int(i))

    def get_use_lidar_cnt(self):
        return self.use_lidar_cnt  

    def get_laser_msg(self):
        return self.laser_msg
		
    def get_view_epi(self):
        return self.view_epi
		
    def get_output_size(self):
        return self.output_size
		
    def get_pth_path(self):
        return self.LoadPath_main
		
    def get_hidden_size(self):
        return self.hidden_size
		
    def get_ros_shutdown_chk(self):
        return not rospy.is_shutdown()
