from roblib import *  # available at https://www.ensta-bretagne.fr/jaulin/roblib.py
import sys

fig = figure()
ax = Axes3D(fig)

m,g,b,d,l=10,9.81,2,1,1
I=array([[10,0,0],[0,10,0],[0,0,20]])
α=array([[0,0,0,0]]).T
dt = 0.01  
B=array([[b,b,b,b],[-b*l,0,b*l,0],[0,-b*l,0,b*l],[-d,d,-d,d]])

file_name = str(sys.argv[1])


def draw_quadri(x): # vecteur d'état x,y,z, angles d'Euler
    ax.clear()
    clean3D(ax,-30,30,-30,30,0,30)
    draw_quadrotor3D(ax,x,α,5*l)    # we infate the robot, just to see something


data = np.loadtxt(file_name, delimiter=',')

for angles in data:
    phi = angles[0]
    theta = angles[1]
    psi = angles[2]    
    
    y = array([[0],[0],[0],[phi],[theta],[psi],[0],[0],[0],[0],[0],[0]])
    
    draw_quadri(y)
    time.sleep(1)
