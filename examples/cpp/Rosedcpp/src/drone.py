from tf import TransformListener
from time import sleep
import rospy
import sys
import numpy as np
import copy
import rospy
import geometry_msgs.msg
from geometry_msgs.msg import Pose, PoseStamped
import tf
from math import pi
from std_msgs.msg import String
from TelloMaison import Telloperso
import os
#os.chdir('../djitellopy')
#print(os.getcwd())
import tello
import time
# import roblib
from numpy import cos,sin,pi
vx = 0
vy = 0
vz = 0

def callback(data):
    drone.v_forward_backw = data.position.x
    drone.v_left_right = data.position.y
    drone.v_up_dow = data.position.z

def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Dronecontrol', anonymous=True)
    rospy.Subscriber('Control', Pose, callback)
    # spin() simply keeps python from exiting until this node is stopped
    drone.testrc()
    rospy.spin()

if __name__ == '__main__':
    drone = Telloperso()
    drone.tkoff()
    listener()
    drone.v_forward_backw = 0
    drone.v_left_right = 0
    drone.v_up_dow = 0
    drone.testrc()
    print("x = ", drone.x)
    print("y = ", drone.y)
    print("z = ", drone.z)
    drone.lnd()
