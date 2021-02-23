import os
os.chdir('./drivers')
#print(os.getcwd())
import tello
import time
import numpy as np


class Drone(tello.Tello):
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
        
