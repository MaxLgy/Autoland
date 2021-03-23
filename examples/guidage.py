from numpy import cross, array , vdot
from numpy.linalg import norm
import matplotlib.pyplot as plt
from roblib import *
def vct_nrm(a,b,c):
	"""Soit a,b,c trois coin de la plateforme supossée carrée, n est un vecteur normal de cette platforme"""
	V1 = a-b
	V2 = a-c
	n = cross(V1,V2).T
	return n/norm(n)

def champ(p,n,phat):
	calc1 = cross(n.T,(p-phat).T)
	pt_attract = 0.1*(phat-p)
	Q = 0.2*cross(n.T,calc1)+pt_attract.T
	return Q

def draw_shampoing(p):
	#ax.scatter(p[0],p[1],p[2]) #p
	Q = champ(p,n,phat)
	Q = Q.flatten() 
	p = p.flatten()
	ax.plot([p[0],p[0]+Q[0]],[p[1],p[1]+Q[1]],[p[2],p[2]+Q[2]],'g-') #champ au point p 

a = array([[0,0,0]])	
b = array([[1,0,0]])
c = array([[0,1,0]])

n = vct_nrm(a,b,c)
print("vecteur normal = ",n)
phat = array([[0],[0],[0]]) #position point d'attérissage
p = array([[0.1],[0.1],[0.5]]) #position drone
Q = champ(p,n,phat)
print("n.Q",vdot(n, Q))
print("valeur du champ au point",Q)

a = a.flatten()	
b = b.flatten()
c = c.flatten()


fig   = figure()
ax    = Axes3D(fig)
for x in arange(0,1,0.1):
	for y in arange(0,1,0.1):
		for z in arange(0,3,0.25):
			draw_shampoing(array([[x,y,z]]).T)


phat = phat.flatten()
ax.scatter(phat[0],phat[1],phat[2]) #phat
n = n.flatten()
ax.plot([phat[0],phat[0]+3*n[0]],[phat[1],phat[1]+3*n[1]],[phat[2],phat[2]+3*n[2]]) #vecteur normal à partir de phat
ax.plot([a[0],b[0],c[0],a[0]],[a[1],b[1],c[1],a[1]],[a[2],b[2],c[2],a[2]]) #platforme
pause(10)
"""
plt.figure()
plt.xlim((-3,3))
plt.ylim((-3,3))
plt.plot(phat[0,0],phat[1,0],'ob')
plt.plot(p[0,0],p[1,0],'or')
plt.plot([p.flatten()[0],p.flatten()[0]+Q.flatten()[0]],[p.flatten()[1],p.flatten()[1]+Q.flatten()[1]])
plt.show()"""
