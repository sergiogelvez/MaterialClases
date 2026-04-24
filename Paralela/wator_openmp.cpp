/**
 * Simulación Wa-Tor con paralelización OpenMP
 * =============================================
 *
 * Implementa el modelo depredador-presa de Dewdney (1984) sobre una
 * grilla toroidal. La paralelización usa la estrategia de "listas de
 * candidatos" con doble buffer:
 *
 *   Fase 1 — Movimiento tentativo (paralelo):
 *       Cada entidad elige su destino y se registra como candidata.
 *
 *   Fase 2 — Resolución de conflictos (paralelo):
 *       Si hay más de un candidato por celda, se elige uno al azar.
 *       Los perdedores se devuelven a su posición original.
 *
 *   Fase 3 — Confirmación (paralelo):
 *       Se copian los ganadores a la grilla limpia, se confirman
 *       reproducciones y se eliminan tiburones sin energía.
 *
 * Compilación:
 *   g++ -std=c++17 -O2 -fopenmp -o wator.o wator_openmp.cpp
 *
 * Ejecución:
 *   ./wator                     (usa valores por defecto)
 *   ./wator 500 500 1000 4      (filas columnas generaciones hilos)
 *
 * Semestre:  2026-1
 */

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <mutex>
#include <random>
#include <string>
#include <vector>

#include <omp.h>

// ============================================================================
// Constantes y parámetros de simulación
// ============================================================================

struct Parameters {
    int rows           = 500;
    int cols           = 500;
    int max_gen        = 1000;
    int num_threads    = 4;

    int initial_fish   = 50000;
    int initial_sharks = 5000;

    int fish_breed     = 3;    // generaciones para que un pez se reproduzca
    int shark_breed    = 10;   // generaciones para que un tiburón se reproduzca
    int starve_time    = 4;    // energía inicial del tiburón (muere si llega a 0)
};

// ============================================================================
// Tipos de celda y estructuras de datos
// ============================================================================

enum class CellType : uint8_t { EMPTY, FISH, SHARK };

/**
 * Celda de la grilla de lectura.
 */
struct Cell {
    CellType type   = CellType::EMPTY;
    int      age    = 0;      // generaciones vivas (para reproducción)
    int      energy = 0;      // solo relevante para tiburones
};

/**
 * Candidato que desea ocupar una celda en la grilla de escritura.
 * Almacena su posición original para poder devolverlo en caso de
 * perder el conflicto.
 */
struct Candidate {
    CellType type;
    int      age;
    int      energy;
    int      orig_row;
    int      orig_col;
    bool     bred;      // ¿intentó reproducirse en este movimiento?
};

/**
 * Celda de la grilla de escritura: contiene una lista de candidatos
 * y un mutex para inserción segura desde múltiples hilos.
 */
struct WriteCell {
    std::vector<Candidate> candidates;
    std::mutex             mtx;

    WriteCell() { candidates.reserve(5); }

    // Necesarios porque std::mutex no es copiable ni movible
    WriteCell(const WriteCell&)            : WriteCell() {}
    WriteCell& operator=(const WriteCell&) { return *this; }
    WriteCell(WriteCell&&) noexcept        : WriteCell() {}
    WriteCell& operator=(WriteCell&&) noexcept { return *this; }
};

// Alias para las grillas
using ReadGrid  = std::vector<std::vector<Cell>>;
using WriteGrid = std::vector<std::vector<WriteCell>>;

// ============================================================================
// Funciones auxiliares
// ============================================================================

/**
 * Coordenada toroidal: asegura que el índice "envuelva" la grilla.
 */
inline int wrap(int coord, int limit) {
    return (coord % limit + limit) % limit;
}

/**
 * Direcciones Von Neumann (arriba, abajo, izquierda, derecha).
 */
static constexpr int DR[] = {-1, 1, 0, 0};
static constexpr int DC[] = {0, 0, -1, 1};

/**
 * Obtiene los vecinos de tipo deseado (EMPTY o FISH) en la grilla de lectura.
 * Retorna un vector de pares (fila, columna).
 */
std::vector<std::pair<int,int>> get_neighbors_of_type(
    const ReadGrid& grid, int row, int col,
    CellType target, const Parameters& params)
{
    std::vector<std::pair<int,int>> result;
    result.reserve(4);
    for (int d = 0; d < 4; ++d) {
        int nr = wrap(row + DR[d], params.rows);
        int nc = wrap(col + DC[d], params.cols);
        if (grid[nr][nc].type == target) {
            result.emplace_back(nr, nc);
        }
    }
    return result;
}

/**
 * Elige un elemento al azar de un vector, usando el generador provisto.
 */
template <typename T, typename RNG>
const T& choose_random(const std::vector<T>& vec, RNG& rng) {
    std::uniform_int_distribution<int> dist(0, static_cast<int>(vec.size()) - 1);
    return vec[dist(rng)];
}

// ============================================================================
// Inicialización
// ============================================================================

void initialize_grid(ReadGrid& grid, const Parameters& params) {
    grid.assign(params.rows, std::vector<Cell>(params.cols));

    // Generar posiciones aleatorias para colocar peces y tiburones
    std::vector<std::pair<int,int>> positions;
    positions.reserve(params.rows * params.cols);
    for (int i = 0; i < params.rows; ++i)
        for (int j = 0; j < params.cols; ++j)
            positions.emplace_back(i, j);

    std::mt19937 rng(12345);
    std::shuffle(positions.begin(), positions.end(), rng);

    int idx = 0;
    for (int k = 0; k < params.initial_fish && idx < (int)positions.size(); ++k, ++idx) {
        auto [r, c] = positions[idx];
        std::uniform_int_distribution<int> age_dist(0, params.fish_breed - 1);
        grid[r][c] = {CellType::FISH, age_dist(rng), 0};
    }
    for (int k = 0; k < params.initial_sharks && idx < (int)positions.size(); ++k, ++idx) {
        auto [r, c] = positions[idx];
        std::uniform_int_distribution<int> age_dist(0, params.shark_breed - 1);
        std::uniform_int_distribution<int> nrg_dist(1, params.starve_time);
        grid[r][c] = {CellType::SHARK, age_dist(rng), nrg_dist(rng)};
    }
}

void clear_write_grid(WriteGrid& wgrid, const Parameters& params) {
    #pragma omp parallel for collapse(2) schedule(static)
    for (int i = 0; i < params.rows; ++i)
        for (int j = 0; j < params.cols; ++j)
            wgrid[i][j].candidates.clear();
}

// ============================================================================
// Fase 1: Movimiento tentativo
// ============================================================================

/**
 * Registra un candidato en la celda destino de la grilla de escritura.
 * Usa un lock_guard sobre el mutex de la celda para evitar data races.
 */
void register_candidate(WriteGrid& wgrid, int dest_r, int dest_c,
                         const Candidate& cand)
{
    std::lock_guard<std::mutex> guard(wgrid[dest_r][dest_c].mtx);
    wgrid[dest_r][dest_c].candidates.push_back(cand);
}

/**
 * Procesa el movimiento tentativo de un pez.
 */
void tentative_move_fish(const ReadGrid& grid, WriteGrid& wgrid,
                         int i, int j, const Parameters& params,
                         std::mt19937& rng)
{
    const Cell& cell = grid[i][j];
    int new_age = cell.age + 1;
    bool will_breed = (new_age >= params.fish_breed);

    auto empty = get_neighbors_of_type(grid, i, j, CellType::EMPTY, params);

    if (!empty.empty()) {
        auto [nr, nc] = choose_random(empty, rng);
        // Registrar el pez en la celda destino
        register_candidate(wgrid, nr, nc,
            {CellType::FISH, will_breed ? 0 : new_age, 0, i, j, will_breed});
    } else {
        // No puede moverse: se queda en su lugar
        register_candidate(wgrid, i, j,
            {CellType::FISH, new_age, 0, i, j, false});
    }
}

/**
 * Procesa el movimiento tentativo de un tiburón.
 */
void tentative_move_shark(const ReadGrid& grid, WriteGrid& wgrid,
                          int i, int j, const Parameters& params,
                          std::mt19937& rng)
{
    const Cell& cell = grid[i][j];
    int new_age    = cell.age + 1;
    int new_energy = cell.energy;
    bool will_breed = (new_age >= params.shark_breed);

    // Prioridad: buscar peces vecinos para comer
    auto fish_neighbors = get_neighbors_of_type(grid, i, j, CellType::FISH, params);

    if (!fish_neighbors.empty()) {
        // Comer: moverse hacia un pez, recuperar energía
        auto [nr, nc] = choose_random(fish_neighbors, rng);
        new_energy = params.starve_time;
        register_candidate(wgrid, nr, nc,
            {CellType::SHARK, will_breed ? 0 : new_age, new_energy, i, j, will_breed});
    } else {
        // No hay peces: buscar celda vacía
        auto empty = get_neighbors_of_type(grid, i, j, CellType::EMPTY, params);
        new_energy -= 1;  // pierde energía al moverse sin comer

        if (new_energy <= 0) {
            // El tiburón muere: no se registra en ninguna celda
            return;
        }

        if (!empty.empty()) {
            auto [nr, nc] = choose_random(empty, rng);
            register_candidate(wgrid, nr, nc,
                {CellType::SHARK, will_breed ? 0 : new_age, new_energy, i, j, will_breed});
        } else {
            // No puede moverse: se queda
            register_candidate(wgrid, i, j,
                {CellType::SHARK, new_age, new_energy, i, j, false});
        }
    }
}

// ============================================================================
// Fase 2: Resolución de conflictos
// ============================================================================

/**
 * Resuelve los conflictos en la grilla de escritura y produce la nueva
 * grilla de lectura.
 *
 * Para cada celda con candidatos:
 *   - Si hay un solo candidato, gana directamente.
 *   - Si hay varios, se elige uno al azar.
 *     - Si entre los candidatos hay un tiburón y un pez (el tiburón
 *       intentó comer, el pez intentó moverse ahí), se da prioridad
 *       al tiburón.
 *     - Los perdedores se devuelven a su celda original sin reproducirse.
 */
void resolve_conflicts(const WriteGrid& wgrid, ReadGrid& new_grid,
                       const Parameters& params)
{
    #pragma omp parallel
    {
        std::mt19937 rng(777 + omp_get_thread_num());

        #pragma omp for collapse(2) schedule(static)
        for (int i = 0; i < params.rows; ++i) {
            for (int j = 0; j < params.cols; ++j) {
                const auto& candidates = wgrid[i][j].candidates;

                if (candidates.empty()) {
                    // Celda vacía
                    new_grid[i][j] = {CellType::EMPTY, 0, 0};
                    continue;
                }

                if (candidates.size() == 1) {
                    // Sin conflicto: el único candidato gana
                    const auto& c = candidates[0];
                    new_grid[i][j] = {c.type, c.age, c.energy};

                    // Si se reprodujo, colocar cría en la posición original
                    if (c.bred) {
                        int oi = c.orig_row, oj = c.orig_col;
                        if (oi != i || oj != j) {
                            // La cría hereda tipo con edad 0 y energía
                            // inicial (para tiburones)
                            int cria_energy = (c.type == CellType::SHARK)
                                              ? params.starve_time : 0;
                            new_grid[oi][oj] = {c.type, 0, cria_energy};
                        }
                    }
                    continue;
                }

                // --- Múltiples candidatos: resolver conflicto ---

                // Separar tiburones y peces
                std::vector<int> shark_idx, fish_idx;
                for (int k = 0; k < (int)candidates.size(); ++k) {
                    if (candidates[k].type == CellType::SHARK)
                        shark_idx.push_back(k);
                    else
                        fish_idx.push_back(k);
                }

                int winner_idx = -1;

                if (!shark_idx.empty()) {
                    // Prioridad a los tiburones (están cazando)
                    winner_idx = choose_random(shark_idx, rng);
                } else {
                    // Solo peces: elegir al azar
                    std::uniform_int_distribution<int> dist(
                        0, static_cast<int>(candidates.size()) - 1);
                    winner_idx = dist(rng);
                }

                // Colocar al ganador
                const auto& winner = candidates[winner_idx];
                new_grid[i][j] = {winner.type, winner.age, winner.energy};

                // Si el ganador se reprodujo, colocar cría
                if (winner.bred) {
                    int oi = winner.orig_row, oj = winner.orig_col;
                    if (oi != i || oj != j) {
                        int cria_energy = (winner.type == CellType::SHARK)
                                          ? params.starve_time : 0;
                        new_grid[oi][oj] = {winner.type, 0, cria_energy};
                    }
                }

                // Devolver perdedores a su posición original
                for (int k = 0; k < (int)candidates.size(); ++k) {
                    if (k == winner_idx) continue;
                    const auto& loser = candidates[k];
                    int oi = loser.orig_row, oj = loser.orig_col;
                    // No se reproduce (movimiento falló)
                    new_grid[oi][oj] = {loser.type, loser.age, loser.energy};
                }
            }
        }
    }
}

// ============================================================================
// Conteo de poblaciones
// ============================================================================

struct Census {
    int fish   = 0;
    int sharks = 0;
};

Census count_population(const ReadGrid& grid, const Parameters& params) {
    int total_fish = 0, total_sharks = 0;

    #pragma omp parallel for collapse(2) schedule(static) \
        reduction(+:total_fish, total_sharks)
    for (int i = 0; i < params.rows; ++i) {
        for (int j = 0; j < params.cols; ++j) {
            if (grid[i][j].type == CellType::FISH)
                ++total_fish;
            else if (grid[i][j].type == CellType::SHARK)
                ++total_sharks;
        }
    }
    return {total_fish, total_sharks};
}

// ============================================================================
// Bucle principal de simulación
// ============================================================================

void run_simulation(const Parameters& params) {
    // Grilla de lectura (generación actual)
    ReadGrid grid;
    initialize_grid(grid, params);

    // Grilla de escritura (candidatos)
    WriteGrid wgrid(params.rows, std::vector<WriteCell>(params.cols));

    // Nueva grilla de lectura (resultado de resolución)
    ReadGrid new_grid(params.rows, std::vector<Cell>(params.cols));

    // Registro de poblaciones para estadísticas
    std::vector<Census> history;
    history.reserve(params.max_gen + 1);

    // Censo inicial
    auto initial = count_population(grid, params);
    history.push_back(initial);
    std::cout << "Generación 0: peces=" << initial.fish
              << " tiburones=" << initial.sharks << "\n";

    omp_set_num_threads(params.num_threads);

    auto t_start = std::chrono::high_resolution_clock::now();

    for (int gen = 1; gen <= params.max_gen; ++gen) {

        // --- Limpiar grilla de escritura ---
        clear_write_grid(wgrid, params);

        // --- Limpiar nueva grilla ---
        #pragma omp parallel for collapse(2) schedule(static)
        for (int i = 0; i < params.rows; ++i)
            for (int j = 0; j < params.cols; ++j)
                new_grid[i][j] = {CellType::EMPTY, 0, 0};

        // --- Fase 1: movimientos tentativos ---
        #pragma omp parallel
        {
            std::mt19937 rng(gen * 1000 + omp_get_thread_num());

            #pragma omp for collapse(2) schedule(static)
            for (int i = 0; i < params.rows; ++i) {
                for (int j = 0; j < params.cols; ++j) {
                    const Cell& cell = grid[i][j];
                    if (cell.type == CellType::FISH)
                        tentative_move_fish(grid, wgrid, i, j, params, rng);
                    else if (cell.type == CellType::SHARK)
                        tentative_move_shark(grid, wgrid, i, j, params, rng);
                }
            }
        }

        // --- Fase 2: resolución de conflictos y escritura ---
        resolve_conflicts(wgrid, new_grid, params);

        // --- Intercambiar grillas ---
        std::swap(grid, new_grid);

        // --- Censo ---
        auto census = count_population(grid, params);
        history.push_back(census);

        if (gen % 100 == 0 || gen == params.max_gen) {
            std::cout << "Generación " << gen
                      << ": peces=" << census.fish
                      << " tiburones=" << census.sharks << "\n";
        }

        // Si ambas poblaciones se extinguen, terminar
        if (census.fish == 0 && census.sharks == 0) {
            std::cout << "Ambas poblaciones se extinguieron en generación "
                      << gen << ".\n";
            break;
        }
    }

    auto t_end = std::chrono::high_resolution_clock::now();
    double elapsed = std::chrono::duration<double>(t_end - t_start).count();

    std::cout << "\nTiempo total: " << elapsed << " s ("
              << params.num_threads << " hilos)\n";

    // --- Guardar historial en CSV ---
    std::ofstream csv("wator_population.csv");
    csv << "generacion,peces,tiburones\n";
    for (int g = 0; g < (int)history.size(); ++g) {
        csv << g << "," << history[g].fish << "," << history[g].sharks << "\n";
    }
    csv.close();
    std::cout << "Historial guardado en wator_population.csv\n";
}

// ============================================================================
// Punto de entrada
// ============================================================================

int main(int argc, char* argv[]) {
    Parameters params;

    if (argc >= 4) {
        params.rows    = std::stoi(argv[1]);
        params.cols    = std::stoi(argv[2]);
        params.max_gen = std::stoi(argv[3]);
    }
    if (argc >= 5) {
        params.num_threads = std::stoi(argv[4]);
    }

    // Ajustar población inicial proporcionalmente si la grilla cambió
    int default_total = 500 * 500;
    int actual_total  = params.rows * params.cols;
    if (actual_total != default_total) {
        double ratio = static_cast<double>(actual_total) / default_total;
        params.initial_fish   = static_cast<int>(50000 * ratio);
        params.initial_sharks = static_cast<int>(5000 * ratio);
    }

    std::cout << "=== Simulación Wa-Tor con OpenMP ===\n"
              << "Grilla:      " << params.rows << " x " << params.cols << "\n"
              << "Generaciones: " << params.max_gen << "\n"
              << "Hilos:        " << params.num_threads << "\n"
              << "Peces:        " << params.initial_fish << "\n"
              << "Tiburones:    " << params.initial_sharks << "\n"
              << "fish_breed:   " << params.fish_breed << "\n"
              << "shark_breed:  " << params.shark_breed << "\n"
              << "starve_time:  " << params.starve_time << "\n"
              << "====================================\n\n";

    run_simulation(params);

    return 0;
}
