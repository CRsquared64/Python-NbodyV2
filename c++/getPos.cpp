#include "Nbody.cpp"
#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

inline void simulate_n_bodies(Nbody bodies[], int num_bodies, int num_cycles) {
    double x_val;
    double y_val;
    double z_val;
    double starting_cycle = 2700;
    std::cout << "Simulating Positions for " << num_cycles << std::endl;
    for (int cycle = starting_cycle; cycle < num_cycles; cycle++) {
        if (cycle % 10 == 0) {
            std::cout << "Starting New Cycle " << cycle << std::endl;
        }

        std::stringstream ss;
        ss << "c_positions/Nbodypositions_" << cycle << ".txt";
        std::ofstream outfile(ss.str());
        for (size_t i = 0; i < num_bodies; i++) {
            std::vector<Nbody> relevantBodies;
            for (size_t j = 0; j < num_bodies; j++) {
                if (i != j) {
                    relevantBodies.push_back(bodies[j]);
                }
            }
            bodies[i].position(&relevantBodies[0], relevantBodies.size());
            x_val = bodies[i].x * scale;
            y_val = bodies[i].y * scale;
            z_val = bodies[i].z * scale;
            //std::cout << x_val << std::endl;
            outfile << x_val << " " << y_val << " " << z_val << "\n";
        }
        outfile.close();

        if (cycle % 100 == 0) {
            std::ofstream finalFile("latest_checkpoint.txt");
            std::cout << "Saving Checkpoint" << std::endl;
            for (size_t i = 0; i < num_bodies; i++) {
                x_val = bodies[i].x * scale;
                y_val = bodies[i].y * scale;
                z_val = bodies[i].z * scale;
                double xv_val = bodies[i].xv * scale;
                double yv_val = bodies[i].yv * scale;
                double zv_val = bodies[i].zv * scale;
                double mass_val = bodies[i].mass;
                finalFile << x_val << " " << y_val << " " << z_val << " " << xv_val << " " << yv_val << " " << zv_val << " " << mass_val << "\n";
            }
            finalFile.close();
        }
    }
}




