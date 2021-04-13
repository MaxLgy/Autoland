import threading
import time
import tello
import numpy as np
from TelloMaison import Telloperso
from guidage import *


class SensorsThread(threading.Thread):
    def __init__(self, drone):
        threading.Thread.__init__(self)
        self.drone = drone

    def run(self):
        time.sleep(5)
        t = time.time()
        while True:
            time.sleep(1)
            data = {}
            try:
                data["height"] = self.drone.get_height()
                data["acceleration_x"] = self.drone.get_acceleration_x()
                data["acceleration_y"] = self.drone.get_acceleration_y()
                data["acceleration_z"] = self.drone.get_acceleration_z()
            except:
                data = {}
            print(data)
            print("Sensors : ", time.time() - t)


class CommandThread(threading.Thread):
    def __init__(self, drone):
        threading.Thread.__init__(self)
        self.drone = drone
    
    def run(self):
        p = drone
        t = time.time()
        self.drone.tkoff()
        phat = np.array([[0], [0], [0]])
        while drone.z > 30:
            p = np.array([[drone.x], [drone.y], [drone.z]])  # position drone
            Q = champ(p, n, phat)
            drone.v_forward_backw = int(Q[0, 0])
            drone.v_left_right = int(Q[0, 1])
            drone.v_up_dow = int(Q[0, 2] * 3)
            drone.testrc()
            time.sleep(0.1)
        time.sleep(0.5)
        self.drone.lnd()


if __name__ == "__main__":
    drone = Telloperso()
    c = CommandThread(drone)
    s = SensorsThread(drone)
    
    c.start()
    s.start()
    
