from numpy import cross, array

def vct_nrm(a,b,c):
	"""Soit a,b,c trois coin de la plateforme supossée carrée, n est un vecteur normal de cette platforme"""
	V1 = a-b
	V2 = a-c
	n = cross(V1,V2)
	return n
