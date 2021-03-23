#include "vect3D.h"
#include <cstdlib>
#include <fstream>
#include <ostream>
#include <iostream>
#include <cmath>
using namespace std;

Vect3D::Vect3D(float X,float Y,float Z) : m_x(X), m_y(Y), m_z(Z)
{

}

Vect3D::~Vect3D()
{
  
}
Vect3D Vect3D::prdvect(Vect3D *v)
{
	Vect3D vf(0,0,0);
	vf.m_x = m_y*v->m_z - m_z*v->m_y;
	vf.m_y = m_z*v->m_x - m_x*v->m_z;
	vf.m_z = m_x*v->m_y - m_y*v->m_x;
	return vf;
}
Vect3D Vect3D::sous(Vect3D *v)
{
	Vect3D vf(0,0,0);
	vf.m_x = m_x - v->m_x;
	vf.m_y = m_y - v->m_y;
	vf.m_z = m_z - v->m_z;
	return vf;
}
Vect3D Vect3D::add(Vect3D *v)
{
	Vect3D vf(0,0,0);
	vf.m_x = m_x + v->m_x;
	vf.m_y = m_y + v->m_y;
	vf.m_z = m_z + v->m_z;
	return vf;
}

void Vect3D::mult(float val)
{
	m_x = val*m_x;
	m_y = val*m_y;
	m_z = val*m_z;
}
float Vect3D::norm()
{
	float norm = sqrt((pow(m_x,2) + pow(m_y,2) + pow(m_z,2)));
	return norm;
}