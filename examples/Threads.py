import threading
import time
import tello
import cam_data_reading
import numpy as np
from TelloMaison import Telloperso
from guidage import *
import copy
import sys
import signal

mutex = threading.Lock()
DATA_CAM = {}
THREAD_ON = True


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    THREAD_ON = False
    drone.tello.send_rc_control(0,0,0,0)
    drone.tello.emergency()
    
    sys.exit(0)


class SensorsThread(threading.Thread):
    def __init__(self, drone):
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(5)
        t = time.time()
        while THREAD_ON:
            mutex.acquire()
            try:
                data_tmp = copy.deepcopy(DATA_CAM)
            finally:
                mutex.release()
            try:
                drone.x = data_tmp["x"]
                drone.y = data_tmp["y"]
                drone.z = data_tmp["z"]
            except:
                drone.x += drone.last_v_forward_backw * (time.time()-drone.last_time_command)
                drone.y += drone.last_v_left_right * (time.time()-drone.last_time_command)
                drone.z += drone.last_v_up_dow * (time.time()-drone.last_time_command)
                drone.z = drone.tello.get_distance_tof()
            time.sleep(0.11)


class CommandThread(threading.Thread):
    def __init__(self, drone):
        threading.Thread.__init__(self)
        self.drone = drone
    
    def run(self):
        #self.drone.tkoff()
        phat = np.array([[-80], [0], [-15]])
        
        p = np.array([[drone.x], [drone.y], [drone.z]])
        Q = champ(p, n, phat)
        Q = (100/np.pi)*np.arctan(Q/100)
        #while np.linalg.norm(Q) > 3:
        while True :#drone.tello.get_distance_tof() > 30:
            p = np.array([[drone.x], [drone.y], [drone.z]])  # position drone
            Q = champ(p, n, phat)
            Q = (100/np.pi)*np.arctan(Q/100)
            print("Drone yaw", drone.yaw)
            drone.v_yaw = 0#-int(((drone.yaw - 90)))
            print("vyaw",drone.v_yaw)
            
            
            drone.v_forward_backw = 0 #int(Q[0, 0])
            drone.v_left_right = 0 #= 0#int(Q[0, 1])
            drone.v_up_dow = 0#"int(Q[0, 2]*1.5)
            drone.testrc()
            #print("Commande : ", Q)
            #print("X = ", drone.x, " , Y = ", drone.y, " , Z = ", drone.z)
            time.sleep(0.1)
            if THREAD_ON == False:
                break
        time.sleep(0.5)
        #self.drone.lnd()


class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while THREAD_ON:
            data = cam_data_reading.read()
            mutex.acquire()
            try:
                DATA_CAM = copy.deepcopy(data)
            finally:
                mutex.release()
            try:
                drone.x = data["x"]
                drone.y = data["y"]
                drone.z = data["z"]
                drone.yaw = data["yaw"]
            except:
                drone.x += drone.last_v_forward_backw * (time.time()-drone.last_time_command)
                drone.y += drone.last_v_left_right * (time.time()-drone.last_time_command)
                drone.z += drone.last_v_up_dow * (time.time()-drone.last_time_command)
                drone.z = drone.tello.get_distance_tof()
            time.sleep(0.1)


if __name__ == "__main__":
    drone = Telloperso()
    c = CommandThread(drone)
    #s = SensorsThread(drone)
    cam = CameraThread()
    
    signal.signal(signal.SIGINT, signal_handler)

    #signal.pause()
    
    c.start()
    #s.start()
    cam.start()
    
