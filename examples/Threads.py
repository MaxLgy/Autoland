import threading
import time
import tello
import cam_data_reading

mutex = threading.Lock()
DATA_CAM = {}

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
        t = time.time()
        self.drone.takeoff()
        while time.time() - t < 30:
            if (time.time () - t) % 0.5 < 0.25:
                self.drone.send_rc_control(0,0,0,30)
            else:
                self.drone.send_rc_control(0,0,0,-30)
            #print("Command : ", time.time() - t)
            #time.sleep(0.5)
        time.sleep(0.5)
        self.drone.land()


class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            data = cam_data_reading.read()
            mutex.acquire()
            try:
                DATA_CAM = data
            finally:
                mutex.release()
            time.sleep(0.1)


if __name__ == "__main__":
    drone = tello.Tello()
    
    c = CommandThread(drone)
    s = SensorsThread(drone)
    cam = CameraThread()
    
    c.start()
    s.start()
    cam.start()
    
