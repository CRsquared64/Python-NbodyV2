from math import *

import numpy`
import numpy as np

'''
callUM THE ISSUE IS THAT THE STARS IN THE CENTER ARE TOO CLOSE TO EACHOTHER SO THEY ARE FALLING INTO ONE
ANOTHER AND THATS WHATS CAUSING THE CIRCLE GILITCH AS THEY ARE ALL SHOT OUT

CALLUM OUT

'''
#
global bodies, video_name

from nbody import Nbody
from numba import njit

video_name = "SpiralSystem"
bodies = []
n = 1000
sep = 1e2


def coord(n):
    # math credit to https://stackoverflow.com/questions/38562144/simulating-a-logarithmic-spiral-galaxy-in-python
    theta = np.radians(np.linspace(0, 360 * 5, 1000))
    a = 50
    b = 0.8
    th = np.random.randn(n)
    x = a * np.exp(b * th) * np.cos(th)
    y = a * np.exp(b * th) * np.sin(th)
    x1 = a * np.exp(b * (th)) * np.cos(th + pi)
    y1 = a * np.exp(b * (th)) * np.sin(th + pi)

    sx = np.random.normal(0, a * 0.25, n)
    sy = np.random.normal(0, a * 0.25, n)
    # show()

    x = (x + sy) + sep
    y = (y + sx) + sep

    x1 = (x1 + sx) + sep
    y1 = (y1 + sy) + sep

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


x_values = []
y_values = []
z_values = []
xv_values = []
yv_values = []
zv_vales = []
mass_values = []


x, y, x1, y1 = coord(n)
k = (n / 2)
G = 6.67430e-11  # gravitational constant

#G1 = Nbody(1 * 10 ** 22, 1 * 10 ** 22, 0, 69, 1e30, (0, 0, 0), "G1")
#G2 = Nbody(-1 * 10 ** 22, - 1 * 10 ** 22, 0, 1e6, 1e30, (0, 255, 0), "galaxy2", False)

x_values.append(1 * 10 ** 24)
y_values.append(1 * 10 ** 24)
z_values.append(0)
mass_values.append(1e30)
fx1, fy1 = galaxy_force(1 * 10 ** 22, 1 * 10 ** 22, -1 * 10 ** 22, -1 * 10 ** 22, 1e30, 1e30)
xv_values.append((fx1 / 1e30) * 1e6)
yv_values.append((fy1 / 1e30) * 1e6)
zv_vales.append(0)
x_values.append(-1 * 10 ** 24)
y_values.append(-1 * 10 ** 24)
z_values.append(0)
mass_values.append(1e30)
fx2, fy2 = galaxy_force(-1 * 10 ** 22, -1 * 10 ** 22, 1 * 10 ** 22, 1 * 10 ** 22, 1e30, 1e30)
xv_values.append((fx2 / 1e30) * 1e6)
yv_values.append((fy2 / 1e30) * 1e6)
zv_vales.append(0)



for i in range(n):
    dio = 0

    if i < k:

        mass = np.random.uniform(1e20, 1e22)
        mass_values.append(mass)
        STAR = Nbody(x[i] * 10 ** 22, y[i] * 10 ** 22, 0, 6.95700 * 10 ** 8, mass, (255, 255, 255),
                     "star", False)
        x_values.append(sep + x[i] * 10 ** 22)
        y_values.append(sep + y[i] * 10 ** 22)
        z_values.append(0)
        # calculate distance between star and black hole
        r = ((STAR.x - 1 * 10 ** 22) ** 2 + (STAR.y - 1 * 10 ** 22) ** 2) ** 0.5
        # calculate gravitational force between star and black hole
        F = G * STAR.mass * 1e30 / r ** 2
        # calculate tangential velocity
        v_tan = ((F * r / STAR.mass) ** 0.5) * 1e6
        # set initial velocities
        if r < 1e22:
            STAR.xv = 5000
            STAR.yv = 5000
            dio = dio + 1
        else:
            STAR.yv = v_tan * cos(atan2(STAR.y - 1 * 10 ** 22, STAR.x - 1 * 10 ** 22))
            STAR.xv = -v_tan * sin(atan2(STAR.y - 1 * 10 ** 22, STAR.x - 1 * 10 ** 22))
        # print(r)
        xv_values.append(STAR.xv)
        yv_values.append(STAR.yv)
        zv_vales.append(0)
        bodies.append(STAR)
    else:

        mass = np.random.uniform(1e20, 1e22)
        mass_values.append(mass)
        STAR = Nbody(x1[i] * 10 ** 22,
                     y1[i] * 10 ** 22, 0,
                     6.95700 * 10 ** 8,
                     mass,
                     (255,
                      255,
                      255),
                     "star",
                     False)
        x_values.append(sep + x1[i] * 10 ** 22)
        y_values.append(sep + y1[i] * 10 ** 22)
        z_values.append(0)
        # calculate distance between star and black hole
        r = ((STAR.x - 1 * 10 ** 22) ** 2 + (STAR.y - 1 * 10 ** 22) ** 2) ** 0.5
        # calculate gravitational force between star and black hole
        F = G * STAR.mass * 1e30 / r ** 2
        # calculate tangential velocity
        v_tan = ((F * r / STAR.mass) ** 0.5) * 1e5
        # set initial velocities
        if r < 1e21:
            STAR.xv = 5000
            STAR.yv = 5000
            dio = dio + 1
        else:
            STAR.yv = v_tan * cos(atan2(STAR.y -1 * 10 ** 22, STAR.x - 1 * 10 ** 22))
            STAR.xv = -v_tan * sin(atan2(STAR.y - 1 * 10 ** 22, STAR.x - 1 * 10 ** 22))
        xv_values.append(STAR.xv)
        yv_values.append(STAR.yv)
        zv_vales.append(0)
        bodies.append(STAR)

galaxy_2_dist = 1e3
galaxy_sep = 1e8

for i in range(n):
    dio = 0

    if i < k:

        mass = np.random.uniform(1e20, 1e22)
        mass_values.append(mass)
        STAR = Nbody(sep - x[i] * 10 ** 22, y[i] * 10 ** 22, 0, 6.95700 * 10 ** 8, mass, (255, 255, 255),
                     "star", False)
        x_values.append(sep - x[i] * 10 ** 22)
        y_values.append(sep - y[i] * 10 ** 22)
        z_values.append(0)
        # calculate distance between star and black hole
        r = ((STAR.x - -1 * 10 ** 22) ** 2 + (STAR.y - -1 * 10 ** 22) ** 2) ** 0.5
        # calculate gravitational force between star and black hole
        F = G * STAR.mass * 1e30 / r ** 2
        # calculate tangential velocity
        v_tan = ((F * r / STAR.mass) ** 0.5) * 1e6
        # set initial velocities
        if r < 1e22:
            STAR.xv = 5000
            STAR.yv = 5000
            dio = dio + 1
        else:
            STAR.yv = v_tan * cos(atan2(STAR.y - -1 * 10 ** 22, STAR.x - -1 * 10 ** 22))
            STAR.xv = -v_tan * sin(atan2(STAR.y - -1 * 10 ** 22, STAR.x - -1 * 10 ** 22))
        # print(r)
        xv_values.append(STAR.xv)
        yv_values.append(STAR.yv)
        zv_vales.append(0)
        bodies.append(STAR)
    else:

        mass = np.random.uniform(1e20, 1e22)
        mass_values.append(mass)
        STAR = Nbody(x1[i] * 10 ** 22,
                     y1[i] * 10 ** 22, 0,
                     6.95700 * 10 ** 8,
                     mass,
                     (255,
                      255,
                      255),
                     "star",
                     False)
        x_values.append(sep - x1[i] * 10 ** 22)
        y_values.append(sep - y1[i] * 10 ** 22)
        z_values.append(0)
        # calculate distance between star and black hole
        r = ((STAR.x - -1 * 10 ** 22) ** 2 + (STAR.y - -1 * 10 ** 22) ** 2) ** 0.5
        # calculate gravitational force between star and black hole
        F = G * STAR.mass * 1e30 / r ** 2
        # calculate tangential velocity
        v_tan = ((F * r / STAR.mass) ** 0.5) * 1e5
        # set initial velocities
        if r < 1e21:
            STAR.xv = 5000
            STAR.yv = 5000
            dio = dio + 1
        else:
            STAR.yv = v_tan * cos(atan2(STAR.y - -1 * 10 ** 22, STAR.x - -1 * 10 ** 22))
            STAR.xv = -v_tan * sin(atan2(STAR.y - -1 * 10 ** 22, STAR.x - -1 * 10 ** 22))
        xv_values.append(STAR.xv)
        yv_values.append(STAR.yv)
        zv_vales.append(0)
        bodies.append(STAR)

data = numpy.column_stack((x_values, y_values, z_values, xv_values, yv_values, zv_vales, mass_values))

numpy.savetxt('starting.txt', data, delimiter=' ')
print(len(bodies) + 2)
print("Too Small", dio)
