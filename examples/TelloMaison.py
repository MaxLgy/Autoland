import os
#os.chdir('../djitellopy')
#print(os.getcwd())
import tello
import time
# import roblib
from numpy import cos,sin,pi


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
            self.z = 100
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
        self.z += self.last_v_up_dow * (time.time()-self.last_time_command)
        self.tello.send_rc_control(self.v_left_right, self.v_forward_backw, self.v_up_dow, 0)
        self.last_time_command = time.time()
        self.last_v_up_dow = self.v_up_dow
        self.last_v_left_right = self.v_left_right
        self.last_v_forward_backw = self.v_forward_backw
        # time.sleep(5)

    def state_vector(self):
        return array([[self.x], [self.y], [self.z]])

    def Rotation_matrix(self):
        φ = self.tello.get_state_field('pitch')
        θ = self.tello.get_state_field('roll')
        ψ = self.tello.get_state_field('yaw')
        return eulermat(φ,θ,ψ)


if __name__ == '__main__':
    drone = Telloperso()
    drone.tkoff()
    drone.v_forward_backw = 20
    drone.v_left_right = 0
    drone.v_up_dow = 0
    drone.testrc()
    time.sleep(3)
    drone.v_forward_backw = 0
    drone.v_left_right = 0
    drone.v_up_dow = 0
    drone.testrc()
    print("x = ", drone.x)
    print("y = ", drone.y)
    print("z = ", drone.z)
    drone.lnd()
