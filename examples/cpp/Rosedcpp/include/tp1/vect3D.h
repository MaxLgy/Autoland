#ifndef __VECT3D_H__
#define __VECT3D_H__
#include <stdio.h>
#include <math.h>

class Vect3D
{
	public: 
		Vect3D(float X, float Y,float Z);
		~Vect3D();
		Vect3D prdvect(Vect3D *v);
		Vect3D sous(Vect3D *v);
		Vect3D add(Vect3D *v);
		void mult(float val);
		float norm();
		float m_x,m_y,m_z;
};
#endif