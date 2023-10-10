#pragma once
#include <iostream>
#include <cmath>
#include <vector>
#include <iostream>
#include <vector>
#include <numeric>
#include <cmath>
#include <chrono>


using namespace std;

 const  double G = 0.6;//6.67428e-11;
 const  double AU = 149.6e6 * 1000;
 const double scale = 1; // 1.5e-22;
 const double timestep = 0.01; // (3600 * 24 * 365 * 2000000000) * 2000000000;//(3600 * 24 * 365 * 2090000000) * 100000000;
 const int b_bass_mass = 4000000;

class Nbody
{
public:
	 double mass;
	 double x;
	 double y;
	 double z;
	 double xv;
	 double yv;
	 double zv;

	 

	Nbody( double xpos,  double ypos,  double zpos,  double mass,  double xv,  double yv,  double zv)
	{
		this->mass = mass;
		this->x = xpos;
		this->y = ypos;
		this->z = zpos;
		this->xv = xv;
		this->yv = yv;
		this->zv = zv;
	}
	Nbody() : x(0), y(0), z(0), mass(0), xv(0), yv(0), zv(0) {};
		


public:

	 double force_x;
	 double force_y;
	 double force_z;

	 bool merged = false;
	 double bmass = 4000000;
	 


public:
	double fastPow(double a, double b) {       //thanks to https://martin.ankerl.com/2007/10/04/optimized-pow-approximation-for-java-and-c-c/
		union {
			double d;
			int x[2];
		} u = { a };
		u.x[1] = (int)(b * (u.x[1] - 1072632447) + 1072632447);
		u.x[0] = 0;
		return u.d;
	}
	vector< double> force(Nbody other)
	{
		 double obj_dist_x, obj_dist_y, obj_dist_z, dist, force;
		auto start_time = std::chrono::high_resolution_clock::now();
		obj_dist_x = other.x - x;
		obj_dist_y = other.y - y;
		obj_dist_z = other.z - z;

		dist = std::sqrt(obj_dist_x * obj_dist_x + obj_dist_y * obj_dist_y + obj_dist_z * obj_dist_z);
		
		force = G * mass * other.mass / ((dist * dist) + 1e-8);
		//std::cout << dist * dist << std::endl;


		std::vector<double> force_vector(3);
		force_vector[0] = force * obj_dist_x / dist;
		force_vector[1] = force * obj_dist_y / dist;
		force_vector[2] = force * obj_dist_z / dist;

		//double force_x = force_vector[0]; I return these in pytohn but i can leave it as a vector
		//double force_y = force_vector[1];
		//double force_z = force_vector[2]; 
		auto end_time = std::chrono::high_resolution_clock::now();
		auto elapsed_time = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
		//std::cout << "Force time: " << elapsed_time.count() << " microseconds" << std::endl;
		return force_vector;
	}


	void position(Nbody* bodies, int num_bodies) {
		double fx = 0.0, fy = 0.0, fz = 0.0;
		
		//auto start_time = std::chrono::high_resolution_clock::now();
		for (int i = 0; i < num_bodies; i++) {
			if (&bodies[i] != this) {
				vector<double> force_vector = force(bodies[i]);
				fx += force_vector[0];

				fy += force_vector[1];

				fz += force_vector[2];
				if (mass >= b_bass_mass && merged==false) {
					merge(bodies[i]);

				}
			}
		}
		if (merged == false) {
			xv += fx / mass * timestep; // Update velocity
			yv += fy / mass * timestep;
			zv += fz / mass * timestep;
			//std::cout << xv << std::endl;
			x += xv * timestep; // Update position
			y += yv * timestep;
			z += zv * timestep;
			//auto end_time = std::chrono::high_resolution_clock::now();
			//auto elapsed_time = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);

			//std::cout << "Position time: " << elapsed_time.count() << " microseconds" << std::endl;
		}
		else {
			x += xv * timestep;
			y += yv * timestep;
			z += zv * timestep;
			merged = true;
		}
		
	}

	void merge(Nbody& other) {
		double range = 25;
		double distance = std::sqrt((other.x - x) * (other.x - x) +
			(other.y - y) * (other.y - y));

		if (distance <= range && other.mass >= b_bass_mass && !merged && !other.merged) {
			// Merge the bodies
			mass += other.mass;
			xv += other.xv;
			yv += other.yv;
			zv += other.zv;

			other.mass = 0;
			other.xv = 0;
			other.yv = 0;
			other.zv = 0;
			other.x = 0;
			other.y = 0;

			std::cout << "Merged! " << mass << std::endl;
			std::cout << other.mass << std::endl;

			merged = true;
			other.merged = true;
		}
	}


};

