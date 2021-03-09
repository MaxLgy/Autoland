from TelloMaison import Telloperso

tello = Telloperso()
print("Takeoff")
tello.tkoff()
tello.testrc()
#tello.up(20)
#tello.trn_r(180)
#tello.fwrd(100)
#tello.trn_l(90)
tello.lnd()
print('Landed')
