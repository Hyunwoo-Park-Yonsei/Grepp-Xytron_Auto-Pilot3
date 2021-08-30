from xycar_msgs.msg import xycar_motor


class u_turn:

    def __init__(self,state,sensor):
        self.motor_msg = xycar_motor()
        self.sensor = sensor
        self.state = state
    
    def Drive(self):
        print(self.sensor)
        if self.sensor[0] < 50:
            self.motor_msg.angle = 50
            self.motor_msg.speed = -30

        elif self.sensor[2] > 200:
            self.motor_msg.speed = 0
            self.motor_msg.angle = 0
            self.state = 10


        elif self.sensor[1] > 50:
            self.motor_msg.angle = -50
            self.motor_msg.speed = 15




