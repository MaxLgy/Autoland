#include <cmath>
#include <cstdlib>
#include <fstream>
#include <ostream>
#include <iostream>
#include "../include/tp1/vect3D.h"
#include "geometry_msgs/PoseStamped.h"
#include "ros/ros.h"
using namespace std;
Vect3D a(0,0,0);
Vect3D b(0,0,0);
Vect3D c(0,0,0);
Vect3D xobjectif(0,0,0);
Vect3D xdrone(0,0,0);
Vect3D Q(0,0,0);
Vect3D n(0,0,0);

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
}

void acoord(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
	a.m_x = msg->pose.position.x;
	a.m_y = msg->pose.position.y;
	a.m_z = msg->pose.position.z;
}

void bcoord(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
	b.m_x = msg->pose.position.x;
	b.m_y = msg->pose.position.y;
	b.m_z = msg->pose.position.z;
}

void ccoord(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
	c.m_x = msg->pose.position.x;
	c.m_y = msg->pose.position.y;
	c.m_z = msg->pose.position.z;
}

void posdrone(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
	xdrone.m_x = msg->pose.position.x;
	xdrone.m_y = msg->pose.position.y;
	xdrone.m_z = msg->pose.position.z;
}

void posobjectif(const geometry_msgs::PoseStamped::ConstPtr& msg)
{
	xobjectif.m_x = msg->pose.position.x;
	xobjectif.m_y = msg->pose.position.y;
	xobjectif.m_z = msg->pose.position.z;
}

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
int main(int argc,char **argv)
{
	ros::init(argc,argv,"Guidage");
	ros::NodeHandle node;
	ros::Publisher force_field_pub = node.advertise<geometry_msgs::PoseStamped>("ForceField",1000);
    ros::Subscriber suba = node.subscribe("Coorda",1000,acoord);
    ros::Subscriber subb = node.subscribe("Coordb",1000,acoord);
    ros::Subscriber subc = node.subscribe("Coordc",1000,acoord);
    ros::Subscriber subdrone = node.subscribe("Coorddrone",1000,posdrone);
    ros::Subscriber subobjectif = node.subscribe("Coordobjectif",1000,posobjectif);
    ros::Rate loop_rate(25);

    while (ros::ok())
    {
    	geometry_msgs::PoseStamped msg;
    	n = vct_nrm(a,b,c);
    	Q = champ(xdrone,xobjectif,n);

    	//edition du message de sortie
    	msg.pose.position.x = Q.m_x;
    	msg.pose.position.y = Q.m_y;
    	msg.pose.position.z = Q.m_z;
    	msg.header.frame_id = "map";
    	msg.header.stamp = ros::Time::now();


    	force_field_pub.publish(msg);
    	ros::spinOnce();
    	loop_rate.sleep();
    }
	return 0;
};
