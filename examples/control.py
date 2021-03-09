from djitellopy import Tello
import time
import  math as m
# see: damiafuentes/DJITelloPy


print("Create Tello object")
tello = Tello()
time.sleep(3)
print("Connect to Tello Drone")
tello.connect()
time.sleep(3)
print(f"Battery Life Pecentage: {tello.get_battery()}")

print("Takeoff - hoser!")
tello.takeoff()
print("x= ", tello.get_state_field('x'))
print("y= ", tello.get_state_field('y'))
print("z= ", tello.get_state_field('z'))
print("-------------------")
time.sleep(3)

v0 = 100 # 100cm/seconde

x, y =0,0
xhat, yhat = 100,100

dt = 0.01

angle = m.atan2(1,1)*180/m.pi
print("angle = ", angle)
dist = int(100*m.sqrt(2))
# tello.rotate_clockwise(360) #60degre/second
# time.sleep(2)
# tello.move_forward(dist)
tello.move_up(50)
print("x= ", tello.get_state_field('x'))
print("y= ", tello.get_state_field('y'))
print("z= ", tello.get_state_field('z'))
print("-------------------")
time.sleep(1)
tello.move_forward(40)
# time.sleep(1)
print("x= ", tello.get_state_field('x'))
print("y= ", tello.get_state_field('y'))
print("z= ", tello.get_state_field('z'))
print("-------------------")

time.sleep(1)

print("landing")
tello.land()
print("touchdown.... goodbye")