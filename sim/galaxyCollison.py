from math import *

import numpy
import numpy as np
import math

#
global bodies, video_name

from nbody import Nbody
from numba import njit

video_name = "SpiralSystem"
bodies = []
n = 2000
sep = 500
particle_sep = 0
base_vel = 5


def coord(n):
    # math credit to https://stackoverflow.com/questions/38562144/simulating-a-logarithmic-spiral-galaxy-in-python
    theta = np.radians(np.linspace(0, 360 * 5, 1000))
    a = 50
    b = 1
    th = np.random.randn(n)
    x = a * np.exp(b * th) * np.cos(th)
    y = a * np.exp(b * th) * np.sin(th)
    x1 = a * np.exp(b * (th)) * np.cos(th + pi)
    y1 = a * np.exp(b * (th)) * np.sin(th + pi)

    sx = np.random.normal(0, a * 0.5, n)
    sy = np.random.normal(0, a * 0.5, n)
    # show()

    x = (x + sy) + particle_sep
    y = (y + sx) + particle_sep

    x1 = (x1 + sx) + particle_sep
    y1 = (y1 + sy) + particle_sep

    # x2 = x + x1
    # y2 = y + y1
    # z = 0
    # data = numpy.column_stack((x2, y2, z))
    # numpy.savetxt('positions.txt', data, fmt='%.6e', delimiter=' ')

    return x, y, x1, y1


def galaxy_force(x1, y1, x2, y2, g1, g2):
    G = 0.6
    r = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    F = G * g1 * g2 / r ** 2
    angle = atan2(y1 - y2, x1 - x2)
    Fx = F * cos(angle)
    Fy = F * sin(angle)
    return Fx, Fy


G = 0.6
def calculate_velocity(star_x, star_y, black_hole_x, black_hole_y):
    G = 0.6  # Gravitational constant in m^3 kg^−1 s^−2
    M = 4*10**6  # Mass of the black hole in kilograms

    # Distance from black hole
    r = math.sqrt((star_x - black_hole_x) ** 2 + (star_y - black_hole_y) ** 2)

    # Circular velocity
    v_circ = math.sqrt(G * M / r)

    # Tangential unit vector
    delta_x = star_x - black_hole_x
    delta_y = star_y - black_hole_y
    tangential_vector = [-delta_y, delta_x]
    magnitude = math.sqrt(tangential_vector[0] ** 2 + tangential_vector[1] ** 2)
    unit_tangential_vector = [tangential_vector[0] / magnitude, tangential_vector[1] / magnitude]

    # Velocity components
    xv = v_circ * unit_tangential_vector[0]
    yv = v_circ * unit_tangential_vector[1]
    return xv, yv



x_values = []
y_values = []
z_values = []
xv_values = []
yv_values = []
zv_vales = []
mass_values = []

x, y, x1, y1 = coord(n)
k = (n / 2)

# G1 = Nbody(1 * 10 ** 22, 1 * 10 ** 22, 0, 69, 1e30, (0, 0, 0), "G1")
# G2 = Nbody(-1 * 10 ** 22, - 1 * 10 ** 22, 0, 1e6, 1e30, (0, 255, 0), "galaxy2", False
b_hole_mass = 4*10**6
g1 = Nbody(0, 0, 0, 1, b_hole_mass, (0, 0, 0), "b")
x_values.append(g1.x)
y_values.append(g1.y)
z_values.append(0)
xv_values.append(0)
yv_values.append(0)
zv_vales.append(0)
mass_values.append(g1.mass)
g2 = Nbody(sep, sep, 0, 1, b_hole_mass, (0, 0, 0), "b")
x_values.append(g2.x)
y_values.append(g2.y)
z_values.append(0)
xv_values.append(0)
yv_values.append(0)
zv_vales.append(0)
mass_values.append(g2.mass)
bodies.append(g1)
bodies.append(g2)
for i in range(n):
    dio = 0

    if i < k:

        mass = 1
        mass_values.append(mass)
        STAR = Nbody(x[i], y[i], 0, 6.95700 * 10 ** 8, mass, (255, 255, 255),
                     "star", False)
        x_values.append(particle_sep + x[i])
        y_values.append(particle_sep + y[i])
        z_values.append(0)
        xv, yv = calculate_velocity(x[i], y[i], 0, 0)  # Calculate velocity based on position
        xv_values.append(xv)
        yv_values.append(yv)
        zv_vales.append(0)
        bodies.append(STAR)
    else:

        mass = 1
        mass_values.append(mass)
        STAR = Nbody(x1[i], y1[i], 0, 6.95700 * 10 ** 8, mass, (255, 255, 255),
                     "star", False)
        x_values.append(particle_sep + x1[i])
        y_values.append(particle_sep + y1[i])
        z_values.append(0)
        xv, yv = calculate_velocity(x1[i], y1[i], 0, 0)  # Calculate velocity based on position
        xv_values.append(xv)
        yv_values.append(yv)
        zv_vales.append(0)
        bodies.append(STAR)

galaxy_2_dist = 1e3
galaxy_sep = 1e8

x, y, x1, y1 = coord(n)
for i in range(n):
    dio = 0

    if i < k:

        mass = 1
        mass_values.append(mass)
        STAR = Nbody(sep - x[i], sep - y[i], 0, 6.95700 * 10 ** 8, mass, (255, 255, 255),
                     "star", False)
        x_values.append(sep -   x[i])
        y_values.append(sep - y[i])
        z_values.append(0)
        xv, yv = calculate_velocity(sep - x[i], sep - y[i], sep, sep)  # Calculate velocity based on position
        xv_values.append(xv)
        yv_values.append(yv)
        zv_vales.append(0)
        bodies.append(STAR)
    else:

        mass = 1
        mass_values.append(mass)
        STAR = Nbody(x1[i], y1[i], 0, 6.95700 * 10 ** 8, mass, (255, 255, 255),
                     "star", False)
        x_values.append(sep - x1[i])
        y_values.append(sep - y1[i])
        z_values.append(0)
        xv, yv = calculate_velocity(sep - x1[i], sep - y1[i], sep, sep)  # Calculate velocity based on position
        xv_values.append(xv)
        yv_values.append(yv)
        zv_vales.append(0)
        bodies.append(STAR)
data = numpy.column_stack((x_values, y_values, z_values, xv_values, yv_values, zv_vales, mass_values))

numpy.savetxt('starting.txt', data, delimiter=' ')
print(len(bodies))
print("Too Small", dio)
