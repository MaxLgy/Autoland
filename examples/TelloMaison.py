import os
#os.chdir('../djitellopy')
#print(os.getcwd())
import tello
import time
from numpy import cos,sin,pi

class Telloperso():
    def __init__(self):
        self.tello = tello.Tello()
        self.tello.connect()
        self.x = 0
        self.y = 0
        self.z = 0
        self.theta = 0
        self.v = 50 #cm.s-1
        self.vdown = 25 #cm.s-1
        self.vrota = 60 #°.s-1
        self.offslp = 0 #s

    def tkoff(self):
        try:
            self.tello.takeoff()
        except:
            self.tello.land()
            print("Emergency stop")
        #time.sleep(self.offslp)
        self.z += 60

    def lnd(self):
        self.tello.land()
        ##time.sleep(self.offslp + angle/self.v)

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
        self.tello.send_rc_control(0,0,0,50)
        time.sleep(5)


