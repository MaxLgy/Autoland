import threading
import time
import tello
import cam_data_reading
import numpy as np
from TelloMaison import Telloperso
from guidage import *
import copy

mutex = threading.Lock()
DATA_CAM = {}

class SensorsThread(threading.Thread):
    def __init__(self, drone):
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(5)
        t = time.time()
        while True:
            mutex.acquire()
            try:
                data_tmp = copy.deepcopy(DATA_CAM)
            finally:
                mutex.release()
            drone.x = data_tmp["x"]
            drone.y = data_tmp["y"]
            drone.z = data_tmp["z"]
            time.sleep(0.1)


class CommandThread(threading.Thread):
    def __init__(self, drone):
        threading.Thread.__init__(self)
        self.drone = drone
    
    def run(self):
        self.drone.tkoff()
        phat = np.array([[0], [0], [0]])
        while drone.tello.get_distance_tof() > 30:
            p = np.array([[drone.x], [drone.y], [drone.z]])  # position drone
            Q = champ(p, n, phat)
            drone.v_forward_backw = int(Q[0, 0])
            drone.v_left_right = int(Q[0, 1])
            drone.v_up_dow = int(Q[0, 2] * 3)
            drone.testrc()
            time.sleep(0.1)
        time.sleep(0.5)
        self.drone.lnd()


class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            data = cam_data_reading.read()
            mutex.acquire()
            try:
                DATA_CAM = copy.deepcopy(data)
            finally:
                mutex.release()
            time.sleep(0.1)


if __name__ == "__main__":
    drone = Telloperso()
    c = CommandThread(drone)
    s = SensorsThread(drone)
    cam = CameraThread()
    c.start()
    s.start()
    cam.start()
    
