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


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    drone.tello.send_rc_control(0,0,0,0)
    drone.tello.emergency()
    
    sys.exit(0)


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
        self.drone.tkoff()
        #while np.linalg.norm(Q) > 3:
        while drone.tello.get_distance_tof() > 30:
            if drone.platform_coords:
                phat = np.array([[drone.platform_coords["x"] - 40*np.cos((np.pi/180)*drone.platform_coords["yaw"])], [drone.platform_coords["y"]], [drone.platform_coords["z"] + 20]])
            else:
                phat = np.array([[0], [0], [0]])
            p = np.array([[drone.x], [drone.y], [drone.z]])
            
            
            Q = champ(p, n, phat, v_d)
            Q = (100/np.pi)*np.arctan(Q/100)
            
            if drone.reversed:
                Q[0, 0] = - Q[0, 0]
                Q[0, 1] = - Q[0, 1]
            
            if 75 < drone.yaw < 105:
                drone.v_forward_backw = int(Q[0, 0])
                drone.v_left_right = int(Q[0, 1])
                drone.v_up_dow = int(Q[0, 2]*1.5)
            else:
                drone.v_forward_backw = 0
                drone.v_left_right = 0
                drone.v_up_dow = 0
                
            if drone.cam_timeout:
                drone.v_forward_backw = 0
                drone.v_left_right = 0
                drone.v_yaw = 60
            else:
                drone.v_yaw = -int(((drone.yaw - 90)))
            
            print(drone.yaw)
            drone.testrc()
            time.sleep(0.1)
        time.sleep(0.5)
        self.drone.lnd()
        raise Exception("Atterrissage avec succes !")


class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        received_in_row = 0
        while True:
            data = cam_data_reading.read()
            mutex.acquire()
            try:
                DATA_CAM = copy.deepcopy(data)
            finally:
                mutex.release()
            try:
                if data["id"] == 1 or data["id"] == 100:
                    drone.x = data["x"]
                    drone.y = data["y"]
                    drone.z = data["z"]
                    drone.yaw = data["yaw"]
                    if data["id"] == 1:
                        drone.reversed = False
                    else:
                        drone.reversed = True
                elif data["id"] == 101:
                    drone.platform_coords = {"x": data["x"], "y": data["y"], "z": data["z"], "yaw": data["yaw"]}
            except:
                drone.x += drone.last_v_forward_backw * (time.time()-drone.last_time_command)
                drone.y += drone.last_v_left_right * (time.time()-drone.last_time_command)
                drone.z += drone.last_v_up_dow * (time.time()-drone.last_time_command)
                drone.z = drone.tello.get_distance_tof()
            if data:
                received_in_row = 0
                drone.cam_timeout = False
            else:
                received_in_row += 1
            if received_in_row > 10:
                drone.cam_timeout = True
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
    
