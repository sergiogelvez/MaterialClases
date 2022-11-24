#include <iostream>
#include <string>
#include <math.h>
#include <vector>

struct Vector3
{
    double e[3] = { 0 };

    Vector3() {}
    ~Vector3() {}

    inline Vector3(double e0, double e1, double e2)
    {
        this->e[0] = e0;
        this->e[1] = e1;
        this->e[2] = e2;
    }
};

struct OrbitalEntity
{
    double e[7] = { 0 };

    OrbitalEntity() {}
    ~OrbitalEntity() {}

    inline OrbitalEntity(double e0, double e1, double e2, double e3, double e4, double e5, double e6)
    {
        this->e[0] = e0;
        this->e[1] = e1;
        this->e[2] = e2;
        this->e[3] = e3;
        this->e[4] = e4;
        this->e[5] = e5;
        this->e[6] = e6;
    }
};

int main()
{
    // Se establecen las condiciones iniciales de la simulación, las "Semillas"
    OrbitalEntity* orbital_entities;
    std::vector<Vector3> trajectories;
    int N_ASTEROIDS = 0;
    // N_ASTEROIDS es para agregar más cuerpos.
    orbital_entities = (OrbitalEntity*)malloc(sizeof(OrbitalEntity) * (9 + N_ASTEROIDS));

    orbital_entities[0] = { 0.0,0.0,0.0,        0.0,0.0,0.0,        1.989e30 }; // a star similar to the sun
    orbital_entities[1] = { 57.909e9,0.0,0.0,   0.0,47.36e3,0.0,    0.33011e24 }; // a planet similar to mercury
    orbital_entities[2] = { 108.209e9,0.0,0.0,  0.0,35.02e3,0.0,    4.8675e24 }; // a planet similar to venus
    orbital_entities[3] = { 149.596e9,0.0,0.0,  0.0,29.78e3,0.0,    5.9724e24 }; // a planet similar to earth
    orbital_entities[4] = { 227.923e9,0.0,0.0,  0.0,24.07e3,0.0,    0.64171e24 }; // a planet similar to mars
    orbital_entities[5] = { 778.570e9,0.0,0.0,  0.0,13e3,0.0,       1898.19e24 }; // a planet similar to jupiter
    orbital_entities[6] = { 1433.529e9,0.0,0.0, 0.0,9.68e3,0.0,     568.34e24 }; // a planet similar to saturn
    orbital_entities[7] = { 2872.463e9,0.0,0.0, 0.0,6.80e3,0.0,     86.813e24 }; // a planet similar to uranus
    orbital_entities[8] = { 4495.060e9,0.0,0.0, 0.0,5.43e3,0.0,     102.413e24 }; // a planet similar to neptune

    // más condiciones iniciales, tiempo inicial, final, paso de tiempo, etc
    double t_0 = 0;
    double t = t_0;

    std::cout << "Estado inicial:" << std::endl;
    for (size_t entity_idx = 0; entity_idx < 9 + N_ASTEROIDS; entity_idx++)
    {
        std::cout << "Particula " << entity_idx << ", tiempo " << t << 
        " : (" << orbital_entities[entity_idx].e[0] << "," << orbital_entities[entity_idx].e[1] << "," << orbital_entities[entity_idx].e[2] << ")" << '\n';
    }

    Vector3 pos_3;
    pos_3.e[0] = orbital_entities[3].e[0];
    pos_3.e[1] = orbital_entities[3].e[1];
    pos_3.e[2] = orbital_entities[3].e[2];
    trajectories.push_back(pos_3);

    // más condiciones iniciales, tiempo inicial, final, paso de tiempo, etc
    double dt = 86400;
    double t_end = 86400 * 365 * 10; // approximately a decade in seconds
    double BIG_G = 6.67e-11; // gravitational constant

    // Propagación de la simulación, 

    while (t < t_end) // se repite hasta que se alcanza el tiempo máximo, que es una década.
    {
        for (size_t m1_idx = 0; m1_idx < 9 + N_ASTEROIDS; m1_idx++)  // se toma una partícula de referencia, m1_idx es el índice de esa partícula
        {
            Vector3 a_g = { 0,0,0 }; // vector aceleración para una partícula

            for (size_t m2_idx = 0; m2_idx < 9 + N_ASTEROIDS; m2_idx++)
            /* se suman las fuerzas para cada partícula, m2_idx representa la partícula que afecta a la de referencia para cada ocasión */
            {
                if (m1_idx != m2_idx) // la partícula no se afecta a ella misma.
                {
                    // vector poisición generado. La distancia entre las dos partículas
                    Vector3 r_vector;
                    // acá se calcula el vector diferencia de posición.
                    r_vector.e[0] = orbital_entities[m1_idx].e[0] - orbital_entities[m2_idx].e[0];
                    r_vector.e[1] = orbital_entities[m1_idx].e[1] - orbital_entities[m2_idx].e[1];
                    r_vector.e[2] = orbital_entities[m1_idx].e[2] - orbital_entities[m2_idx].e[2];
                    
                    // se calcula la magnitud del vector r.
                    double r_mag = sqrt(r_vector.e[0] * r_vector.e[0] + r_vector.e[1] * r_vector.e[1] + r_vector.e[2] * r_vector.e[2]);
                    // se calcula la aceleración generada por la fuerza entre el par de partículas (se excluye la masa de la parícula de referencia, como con el campo eléctrico)
                    double acceleration = -1.0 * BIG_G * (orbital_entities[m2_idx].e[6]) / pow(r_mag, 2.0);
                    // acá básicamente se calculó la magnitud, ahora se calcula el conjunto de vectores unitarios de la dirección
                    Vector3 r_unit_vector = { r_vector.e[0] / r_mag,r_vector.e[1] / r_mag,r_vector.e[2] / r_mag };
                    // aceleración por vectores unitarios.
                    a_g.e[0] += acceleration * r_unit_vector.e[0];
                    a_g.e[1] += acceleration * r_unit_vector.e[1];
                    a_g.e[2] += acceleration * r_unit_vector.e[2];

                }
            }

            // se acumulan las velocidades: vxi = vxi-1 + axi * dt
            // todas las aceleraciones generadas sobre m1_idx
            orbital_entities[m1_idx].e[3] += a_g.e[0] * dt;
            orbital_entities[m1_idx].e[4] += a_g.e[1] * dt;
            orbital_entities[m1_idx].e[5] += a_g.e[2] * dt;
        // acá finalizan las operaciones para el conjunto de particulas sobre una particula m1_idx
        }
    // acá se calculan las posiciones para todas las particulas, a partir de las velocidades generadas.
        for (size_t entity_idx = 0; entity_idx < 9 + N_ASTEROIDS; entity_idx++)
        {
            orbital_entities[entity_idx].e[0] += orbital_entities[entity_idx].e[3] * dt;
            orbital_entities[entity_idx].e[1] += orbital_entities[entity_idx].e[4] * dt;
            orbital_entities[entity_idx].e[2] += orbital_entities[entity_idx].e[5] * dt;
            if (t == 0 || t == t_end - dt ) // machetin: solo imprimir las posiciones iniciales y finales y comparar
            {
                std::cout << "Particula " << entity_idx << ", tiempo " << t + dt << " : (" << orbital_entities[entity_idx].e[0] << "," << orbital_entities[entity_idx].e[1] << "," << orbital_entities[entity_idx].e[2] << ")" << '\n';
            }    
        }
    
        // una vez terminado esto, se avanza en el tiempo.
        t += dt;
        pos_3.e[0] = orbital_entities[3].e[0];
        pos_3.e[1] = orbital_entities[3].e[1];
        pos_3.e[2] = orbital_entities[3].e[2];
        trajectories.push_back(pos_3);
        // acá debería haber una estructura para guardar las posiciones para cada t.
    }
    std::cout << "Número de puntos de la trayectoria para el planeta 3: " << trajectories.size() << ", tiempo total: " << trajectories.size() * dt << std::endl; 
    auto posi = trajectories[0];
    std::cout << "Particula " << 3 << ", tiempo " << 0 << " : (" << posi.e[0] << "," << posi.e[1] << "," << posi.e[2] << ")" << '\n';
    auto posf = trajectories.end() - 1;
    std::cout << "Particula " << 3 << ", tiempo " << t << " : (" << posf->e[0] << "," << posf->e[1] << "," << posf->e[2] << ")" << '\n';
    std::cout << "******* Imprimir toda la trayectoria: *******" << '\n'; 
    int i = 0;
    for (auto ii : trajectories)
    {
        if (i == 0 || i == 1)
            std::cout << "Particula " << 3 << ", tiempo " << i * dt << " : (" << ii.e[0] << "," << ii.e[1] << "," << ii.e[2] << ")" << '\n';
        i = i + 1;
    }
    std::cout << i;
    return 0;
}