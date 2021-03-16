#include <cmath>
#include <cstdlib>
#include <fstream>
#include <ostream>
#include <iostream>
#include "vect3D.h"
using namespace std;

Vect3D vct_nrm(Vect3D a,Vect3D b, Vect3D c)
{
	Vect3D V1 = a.sous(&b);
	Vect3D V2 = a.sous(&c);
	Vect3D n = V1.prdvect(&V2);
	float norm_n = n.norm();
	n.m_x = n.m_x/norm_n;
	n.m_y = n.m_y/norm_n;
	n.m_z = n.m_z/norm_n;
	return n;
};
Vect3D champ(Vect3D p,Vect3D phat, Vect3D n)
{	
	float intensitee_point = 0.1;
	float intensitee_ligne = 0.2; 
	Vect3D sub1 = p.sous(&phat);
	Vect3D sub2 = phat.sous(&p);
	Vect3D prodvect1 = n.prdvect(&sub1);
	Vect3D forceligne = n.prdvect(&prodvect1);
    sub2.mult(intensitee_point);
    forceligne.mult(intensitee_ligne);
	Vect3D Q = forceligne.add(&sub2);
	return Q;
};
int main()
{
	Vect3D v1(0,0,0);
	Vect3D v2(1,0,0);
	Vect3D v3(0,1,0);
	Vect3D n = vct_nrm(v1,v2,v3);
	cout<<n.m_x<<endl;
	cout<<n.m_y<<endl;
	cout<<n.m_z<<endl;
	Vect3D p(0.1,0.1,0.5);
	Vect3D phat(0,0,0);
	Vect3D Q = champ(p,phat,n);
	cout <<Q.m_x <<endl; 
	cout <<Q.m_y <<endl;
	cout <<Q.m_z <<endl; 
	cout <<Q.norm()<<endl; 
	return 0;
};
