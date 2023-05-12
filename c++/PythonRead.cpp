
#include <fstream>
#include <sstream>
#include <vector>
#include "nbody.cpp"
#include <cmath>

inline std::vector<Nbody> createNbodiesFromFile(const std::string& filename)
{
    std::vector<Nbody> nbodies;
    std::ifstream infile(filename);
    std::string line;

    while (std::getline(infile, line)) {
        std::istringstream iss(line);
         double x, y, z, xv, yv, zv, mass;
         int velocity_scale = 1;

        if (iss >> x >> y >> z >> xv >> yv >> zv >> mass) {
            Nbody nbody(x, y, z, mass, xv * velocity_scale, yv * velocity_scale, zv); 
            nbodies.push_back(nbody);
        }
    }

    return nbodies;
}

