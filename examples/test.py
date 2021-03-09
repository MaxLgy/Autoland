from tello import Tello
import time
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
"""
time.sleep(1)
print("Move Left X cm")
tello.move_left(50)

time.sleep(1)
print("Rotate clockwise")
tello.rotate_clockwise(90)

time.sleep(1)
print("Move forward X cm")
tello.move_forward(50)
"""

# time.sleep(1)
#print("Move forward X cm")
#tello.move_forward(500)
#
# # time.sleep(1)
# print("Rotate clockwise")
# # tello.rotate_clockwise(180)
#
# # time.sleep(1)
# print("Move forward X cm")
# # tello.move_forward(2)

# print("Prepare floor to land.... you have 1 second")
# tello.move_down(70)

time.sleep(1)

print("landing")
tello.land()
print("touchdown.... goodbye")
