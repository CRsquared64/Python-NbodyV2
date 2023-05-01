import random
from math import *
from pylab import *
import numpy as np

import nbody
global bodies, video_name

video_name = "SpiralSystem"
bodies = []
n = 400

def coord(
        n):  # math credit to https://stackoverflow.com/questions/38562144/simulating-a-logarithmic-spiral-galaxy-in
    # -python
    theta = np.radians(np.linspace(0, 360 * 5, 1000))
    a = 0.5
    b = 0.6
    th = np.random.randn(n)
    x = a * exp(b * th) * cos(th)
    y = a * exp(b * th) * sin(th)
    x1 = a * exp(b * (th)) * cos(th + pi)
    x1 = a * exp(b * (th)) * cos(th + pi)
    y1 = a * exp(b * (th)) * sin(th + pi)

    sx = np.random.normal(0, a * 0.25, n)
    sy = np.random.normal(0, a * 0.25, n)
    plot(x + sy, y + sx, "*")
    plot(x1 + sx, y1 + sy, "*")


    x = x + sy
    y = y + sx

    x1 = x1 + sx
    y1 = y1 + sy

    return x, y, x1, y1


B_HOLE = nbody.Nbody(0, 0, 0,1.2 * 10 **7, 8.26 * 10 ** 36, (0, 0, 255), "Black hole")
bodies.append(B_HOLE)
x, y, x1, y1, = coord(n)
k = (n / 2)
for i in range(n):
    if i < k:
        STAR = nbody.Nbody(x[i] * 10 ** 22, y[i], 0, 6.95700 * 10 ** 8,  1.98892 * 10 ** 30, (255,255,255), "star", False)
        STAR.yv = 225 * 1000000
        bodies.append(STAR)
    else:
        STAR = nbody.Nbody(x1[i] * 10 ** 22, y1[i], 0, 6.95700 * 10 ** 8,  1.98892 * 10 ** 30, (255,255,255), "star", False)
        STAR.yv = 225 * 1000000
        bodies.append(STAR)


print(len(bodies))