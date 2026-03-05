/*

g++ -O2 -std=c++17 -o streamlines_rk4 streamlines_rk4.cpp -lm
./streamlines_rk4
gnuplot plot_streamlines.gp 

*/


#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <functional>
#include <string>
#include <omp.h>

// ---------------------------------------------------------------------------
// Estructura para vectores 2D
// ---------------------------------------------------------------------------
struct Vec2 {
    double x, y;
    Vec2(double x = 0.0, double y = 0.0) : x(x), y(y) {}
    Vec2 operator+(const Vec2& o) const { return {x + o.x, y + o.y}; }
    Vec2 operator*(double s)       const { return {x * s,   y * s};   }
    double norm() const { return std::sqrt(x * x + y * y); }
};

// Tipo para el campo de velocidad: dado un punto, retorna el vector velocidad
using CampoVelocidad = std::function<Vec2(double, double)>;

// ---------------------------------------------------------------------------
// Integrador Runge-Kutta 4 para un paso
//   Resuelve:  d(pos)/dt = V(pos.x, pos.y)
// ---------------------------------------------------------------------------
Vec2 rk4_paso(const Vec2& pos, double dt, const CampoVelocidad& V)
{
    Vec2 k1 = V(pos.x,              pos.y);
    Vec2 k2 = V(pos.x + 0.5*dt*k1.x, pos.y + 0.5*dt*k1.y);
    Vec2 k3 = V(pos.x + 0.5*dt*k2.x, pos.y + 0.5*dt*k2.y);
    Vec2 k4 = V(pos.x +     dt*k3.x, pos.y +     dt*k3.y);

    return {
        pos.x + (dt / 6.0) * (k1.x + 2.0*k2.x + 2.0*k3.x + k4.x),
        pos.y + (dt / 6.0) * (k1.y + 2.0*k2.y + 2.0*k3.y + k4.y)
    };
}

// ---------------------------------------------------------------------------
// Genera una streamline completa desde un punto semilla
//   - semilla:    punto de inicio
//   - dt:         paso de integración
//   - max_pasos:  número máximo de pasos
//   - V:          campo de velocidad
//   - dominio:    límites [xmin, xmax, ymin, ymax]
//   - vel_min:    velocidad mínima para detener la integración
// ---------------------------------------------------------------------------
std::vector<Vec2> generar_streamline(
    const Vec2&           semilla,
    double                dt,
    int                   max_pasos,
    const CampoVelocidad& V,
    double xmin, double xmax,
    double ymin, double ymax,
    double vel_min = 1e-8)
{
    std::vector<Vec2> linea;
    Vec2 pos = semilla;
    linea.push_back(pos);

    for (int i = 0; i < max_pasos; ++i) {
        Vec2 vel = V(pos.x, pos.y);

        // Detener si la velocidad es prácticamente cero
        if (vel.norm() < vel_min) break;

        pos = rk4_paso(pos, dt, V);

        // Detener si sale del dominio
        if (pos.x < xmin || pos.x > xmax ||
            pos.y < ymin || pos.y > ymax)
            break;

        linea.push_back(pos);
    }
    return linea;
}

// ---------------------------------------------------------------------------
// Exporta las streamlines a un archivo CSV (compatible con gnuplot, Python, etc.)
//   Cada streamline está separada por una línea en blanco.
// ---------------------------------------------------------------------------
void exportar_csv(const std::string& nombre_archivo,
                  const std::vector<std::vector<Vec2>>& streamlines)
{
    std::ofstream archivo(nombre_archivo);
    if (!archivo.is_open()) {
        std::cerr << "Error: no se pudo abrir " << nombre_archivo << "\n";
        return;
    }

    archivo << "# x, y  (streamlines separadas por líneas en blanco)\n";
    for (const auto& linea : streamlines) {
        for (const auto& p : linea) {
            archivo << p.x << ", " << p.y << "\n";
        }
        archivo << "\n";  // separador entre streamlines
    }
    archivo.close();
    std::cout << "Archivo generado: " << nombre_archivo
              << " (" << streamlines.size() << " streamlines)\n";
}

// ===========================================================================
//  Campos de velocidad de ejemplo
// ===========================================================================

// 2) Vórtice centrado en el origen
Vec2 vortice(double x, double y) {
    double r2 = x*x + y*y + 1e-12;  // evitar singularidad
    return {-y / r2, x / r2};
}

// 3) Punto de silla (saddle point)
Vec2 punto_silla(double x, double y) {
    return {x, -y};
}

// 4) Dipolo (fuente + sumidero)
Vec2 dipolo(double x, double y) {
    double d = 0.5;  // semi-distancia entre fuente y sumidero
    // Fuente en (-d, 0), sumidero en (+d, 0)
    double r1_2 = (x + d)*(x + d) + y*y + 1e-12;
    double r2_2 = (x - d)*(x - d) + y*y + 1e-12;
    double Q = 1.0;  // intensidad
    return {
        Q * ((x + d)/r1_2 - (x - d)/r2_2),
        Q * (y/r1_2       - y/r2_2)
    };
}

// 5) Cilindro en flujo potencial (flujo alrededor de un cilindro de radio R)
Vec2 flujo_cilindro(double x, double y) {
    double R = 1.0;
    double U = 1.0;  // velocidad del flujo libre
    double r2 = x*x + y*y + 1e-12;
    double r4 = r2 * r2;
    double R2 = R * R;
    return {
        U * (1.0 - R2 * (x*x - y*y) / r4),
        U * (-2.0 * R2 * x * y / r4)
    };
}

// ===========================================================================
//  main: genera semillas en una grilla y traza streamlines
// ===========================================================================
int main()
{
    // --- Parámetros ---
    const double dt        = 0.02;
    const int    max_pasos = 2000;

    // Dominio
    const double xmin = -4.0, xmax = 4.0;
    const double ymin = -3.0, ymax = 3.0;

    // Seleccionar el campo de velocidad
    CampoVelocidad campo = vortice;

    // Generar semillas: línea vertical en x = xmin
    const int n_semillas = 100;

    const double cx = 0.0, cy = 0.0;
    const double radio = 2.5;

    /* std::vector<Vec2> semillas;
    for (int i = 0; i < n_semillas; ++i) {
        double y = ymin + (ymax - ymin) * i / (n_semillas - 1);
        semillas.push_back({0, y});
    } */

    omp_set_num_threads(omp_get_max_threads());


    // semillas en forma de circulo
    std::vector<Vec2> semillas;
    for (int i = 0; i < n_semillas; ++i) {
        double theta = 2.0 * M_PI * i / n_semillas;
        semillas.push_back({cx + radio * std::cos(theta),
                            cy + radio * std::sin(theta)});
    }

    // Agregar algunas semillas adicionales en una grilla dispersa
    for (double sx = -3.0; sx <= 3.0; sx += 1.5) {
        for (double sy = -2.0; sy <= 2.0; sy += 1.0) {
            semillas.push_back({sx, sy});
        }
    }

    // --- Trazar streamlines ---
    /* std::vector<std::vector<Vec2>> streamlines;
    for (const auto& s : semillas) {
        auto linea = generar_streamline(s, dt, max_pasos, campo, xmin, xmax, ymin, ymax);
        if (linea.size() > 1) {
            streamlines.push_back(std::move(linea));
        }
    } */

    // --- Trazar streamlines OMP ---
    std::vector<std::vector<Vec2>> streamlines(semillas.size());

    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < (int)semillas.size(); ++i) {
        streamlines[i] = generar_streamline(semillas[i], dt, max_pasos, campo, xmin, xmax, ymin, ymax);
        std::cout << " " << omp_get_thread_num() << " ";
    }



    // --- Exportar ---
    exportar_csv("streamlines.csv", streamlines);

    // --- Generar script gnuplot ---
    {
        std::ofstream gp("plot_streamlines.gp");
        gp << "set terminal pngcairo size 1200,900 enhanced font 'Arial,12'\n";
        gp << "set output 'streamlines.png'\n";
        gp << "set title 'Streamlines — RK4' font ',16'\n";
        gp << "set xlabel 'x'\n";
        gp << "set ylabel 'y'\n";
        gp << "set size ratio -1\n";
        gp << "set grid\n";
        gp << "set key off\n";

        // Dibujar cilindro si aplica
        gp << "set object 1 circle at 0,0 size 1.0 fc rgb '#cccccc' fs solid\n";

        gp << "plot 'streamlines.csv' using 1:2 with lines lw 1.2 lc rgb '#2060c0'\n";
        gp.close();
        std::cout << "Script gnuplot generado: plot_streamlines.gp\n";
        std::cout << "  Ejecute: gnuplot plot_streamlines.gp\n";
    }

    return 0;
}
