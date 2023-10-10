#include "Nbody.cpp"
#include "getPos.cpp"
#include "PythonRead.cpp"
#include <chrono>
int main() {
    auto start_time = std::chrono::high_resolution_clock::now();
    std::vector<Nbody> nbodies = createNbodiesFromFile("latest_checkpoint.txt");
    Nbody* nbodyArray = &nbodies[0]; 

    constexpr int num_bodies = 4002;
    constexpr int num_cycles = 4000; 



    simulate_n_bodies(nbodyArray, num_bodies, num_cycles);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto elapsed_time = std::chrono::duration_cast<std::chrono::minutes>(end_time - start_time);
    std::cout << "Completed in " << elapsed_time.count() << " Minutes" << std::endl;

    return 0;
}