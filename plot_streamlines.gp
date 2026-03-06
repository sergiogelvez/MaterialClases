set terminal pngcairo size 1200,900 enhanced font 'Arial,12'
set output 'streamlines.png'
set title 'Streamlines — RK4' font ',16'
set xlabel 'x'
set ylabel 'y'
set size ratio -1
set grid
set key off
set object 1 circle at 0,0 size 1.0 fc rgb '#cccccc' fs solid
plot 'streamlines.csv' using 1:2 with lines lw 1.2 lc rgb '#2060c0'
