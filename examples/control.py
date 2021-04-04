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
time.sleep(3)
x0, y0, z0 = 0,0,100
t0 = time.time()
tello.send_rc_control(0, 20, 0, 0) # send_rc_control(self, left_right_velocity: int, forward_backward_velocity: int, up_down_velocity: int, yaw_velocity: int):
time.sleep(3)
t = time.time()
tello.send_rc_control(0, 0, 0, 0)
x, y, z = 20 * (t-t0) + x0, 0 * (t-t0) + y0, -0 * (t-t0) + z0
print("x= ", x)  # tello.get_state_field('x'))
print("y= ", y)  # tello.get_state_field('y'))
print("z= ", z)  # tello.get_state_field('z'))
print("pitch= ", tello.get_state_field('pitch'))
print("roll= ", tello.get_state_field('roll'))
print("yaw= ", tello.get_state_field('yaw'))
print("-------------------")
time.sleep(3)

v0 = 100  # 100cm/seconde

x, y = 0, 0
xhat, yhat = 100, 100

dt = 0.01

angle = m.atan2(1,1)*180/m.pi
print("angle = ", angle)
dist = int(100*m.sqrt(2))
# tello.rotate_clockwise(360) # 60 degre /second
# time.sleep(2)
# tello.move_forward(dist)
# tello.move_up(50)
print("x= ", x)# tello.get_state_field('x'))
print("y= ", y)#tello.get_state_field('y'))
print("z= ", z)#tello.get_state_field('z'))
print("pitch= ", tello.get_state_field('pitch'))
print("roll= ", tello.get_state_field('roll'))
print("yaw= ", tello.get_state_field('yaw'))
print("-------------------")
# time.sleep(1)
# tello.move_forward(40)
# time.sleep(1)
print("x= ", x)# tello.get_state_field('x'))
print("y= ", y)#tello.get_state_field('y'))
print("z= ", z)#tello.get_state_field('z'))
print("pitch= ", tello.get_state_field('pitch'))
print("roll= ", tello.get_state_field('roll'))
print("yaw= ", tello.get_state_field('yaw'))
print("-------------------")

# time.sleep(1)

print("landing")
tello.land()
print("touchdown.... goodbye")