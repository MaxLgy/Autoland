import os
#os.chdir('../djitellopy')
#print(os.getcwd())
import tello
import time
# import roblib
from numpy import cos,sin,pi
from guidage import *


class Telloperso():
    def __init__(self):
        self.tello = tello.Tello()
        self.tello.connect()
        print(f"Battery Life Pecentage: {self.tello.get_battery()}")
        self.x = 0  # cm
        self.y = 0  # cm
        self.z = 0  # cm
        self.theta = 0

        self.v_left_right = 0  # cm.s-1
        self.v_forward_backw = 0  # cm.s-1
        self.v_up_dow = 0  # cm.s-1
        self.last_v_left_right = 0  # cm.s-1
        self.last_v_forward_backw = 0  # cm.s-1
        self.last_v_up_dow = 0  # cm.s-1
        self.last_time_command = 0

        self.v = 50  # cm.s-1
        self.vdown = 25  # cm.s-1
        self.vrota = 60  # °.s-1
        self.offslp = 0  # s

    def tkoff(self):
        try:
            self.tello.takeoff()
            self.z = self.tello.get_distance_tof()
            self.last_time_command = time.time()
        except:
            self.tello.land()
            print("Emergency stop")
        #time.sleep(self.offslp)

        # self.z += 60

    def lnd(self):
        self.tello.land()
        ##time.sleep(self.offslp + angle/self.v)
        self.last_time_command = time.time()

    def fwrd(self,cm):
        "move for n cm between 20-500"
        self.tello.move_forward(cm)
        #time.sleep(self.offslp+cm/self.v)
        self.x += cm*cos(self.theta)
        self.y += cm*sin(self.theta)

    def trn_r(self,angle):
        "turn clockwise of and angle between 1-360"
        self.tello.rotate_clockwise(angle)
        #time.sleep(self.offslp + angle/self.vrota)
        self.theta -= angle/360*2*pi

    def trn_l(self,angle):
        "turn clockwise of and angle between 1-360"
        self.tello.rotate_counter_clockwise(angle)
        #time.sleep(self.offslp + angle/self.vrota)
        self.theta += angle/360*2*pi

    def up(self,cm):
        "Go up for n cm"
        self.tello.move_up(cm)
        #time.sleep(self.offslp + cm/self.v)
        self.z += cm

    def down(self,cm):
        "Go down for n cm"
        self.tello.move_down(cm)
        #time.sleep(self.offslp + cm/self.vdown)
        self.z -= cm
    
    def testrc(self):
        #self.tello.send_rc_control(20, 0, -20, 30)
        #send_rc_control(self,left_right_velocity: int, forward_backward_velocity: int, up_down_velocity: int, yaw_velocity: int):
        self.x += self.last_v_forward_backw * (time.time()-self.last_time_command)
        self.y += self.last_v_left_right * (time.time()-self.last_time_command)
        # self.z += self.last_v_up_dow * (time.time()-self.last_time_command)
        self.z = self.tello.get_distance_tof()
        self.tello.send_rc_control(self.v_left_right, self.v_forward_backw, self.v_up_dow, 0)
        self.last_time_command = time.time()
        self.last_v_up_dow = self.v_up_dow
        self.last_v_left_right = self.v_left_right
        self.last_v_forward_backw = self.v_forward_backw
        # time.sleep(5)

    def state_vector(self):
        return array([[self.x], [self.y], [self.z]])


    def Rotation_matrix(self):
        """Uses drone's sensors to compute the actual rotation matrix
        Returns:
            np matrix: Rotation matrix of the drone
        """
        pitch, yaw, roll = self.tello.get_pitch(), self.tello.get_yaw(), self.tello.get_roll()
        pitch = (pitch*np.pi)/180
        yaw = (yaw*np.pi)/180
        roll = (roll*np.pi)/180
        return eulermat(roll, pitch, yaw)
    
    
    def control(self, X, R, Xbar, Rbar):
        """Proportionnal controler to the drone
        Arguments:
            X, Xbar: np arrays (3, 1)
            R, Rbar: np matrices (3, 3)
        Returns:
            Dict: rc commands
        """
        x, y, z = X.flatten()
        xbar, ybar, zbar = Xbar.flatten()
        
        # height error
        e_z = 1*(zbar-z)
        
        # heading error
        e_R = np.linalg.inv(R) @ Rbar
        e_yaw = 1*arctan2(e_R[1,0],e_R[0,0])
        
        # distance error modulated by the heading error (Gaussian)
        e_dist = (1*((xbar - x)**2 + (ybar - y)**2)**0.5) * exp(-e_yaw**2)
        
        
        return {"left_right_velocity": 0, "forward_backward_velocity":e_dist, "up_down_velocity":e_z, "yaw_velocity":e_yaw}
        


if __name__ == '__main__':
    print("yes")
    print(vct_nrm(a,b,c))
    file_name = 'Mission_' + str(time.time()) + '.txt'
    with open(file_name, 'w') as f:
        f.write("# pitch,yaw,roll\n")
    
    
    
    drone = Telloperso()
    drone.tkoff()
    while drone.z>30:
        for k in range(2):
            with open(file_name, 'a') as f:
                f.write(str(drone.tello.get_pitch()) + ',' + str(drone.tello.get_yaw()) + ',' + str(drone.tello.get_roll()))
                f.write("\n")
            time.sleep(0.5)
        
        p = array([[drone.x], [drone.y], [drone.z]])  # position drone
        Q = champ(p, n, phat)
        # print("distance au sol = ", drone.tello.get_distance_tof())
        print("Q0 = ",2*Q[0,0])
        print("Q1 = ", Q[0, 1])
        print("Q2 = ", 3*Q[0, 2])
        drone.v_forward_backw = int(Q[0,0])
        drone.v_left_right = int(Q[0,1])
        drone.v_up_dow = int(Q[0,2]*3)
        drone.testrc()
        
        
    drone.v_forward_backw = 0
    drone.v_left_right = 0
    drone.v_up_dow = 0
    drone.testrc()
    print("x = ", drone.x)
    print("y = ", drone.y)
    print("z = ", drone.z)
    drone.lnd()
