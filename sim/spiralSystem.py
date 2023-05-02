from math import *

import numpy as np
from pylab import *



global bodies, video_name

from nbody import Nbody

video_name = "SpiralSystem"
bodies = []
n = 1000
separation = 1


def coord(n):
    # math credit to https://stackoverflow.com/questions/38562144/simulating-a-logarithmic-spiral-galaxy-in-python
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


B_HOLE = Nbody(0, 0, 0, 69, 8.26 * 10 ** 28, (0, 0, 255), "Black hole")
bodies.append(B_HOLE)
x, y, x1, y1 = coord(n)
k = (n / 2)
for i in range(n):
    import random
    if i < k:
        STAR = Nbody(x[i] * 10 ** 22, y[i] * 10 ** 22, 0, 6.95700 * 10 ** 8, np.random.uniform(1e20, 1e22), (255, 255, 255),
                           "star", False)
        STAR.yv = random.gauss(225e4, 50e3)
        STAR.xv = random.gauss(-225e4, 50e3)
        bodies.append(STAR)
    else:
        STAR = Nbody(x1[i] * 10 ** 22 + separation,
                           y1[i] * 10 ** 22, 0,
                           6.95700 * 10 ** 8,
                           random.uniform(1e20,
                                          1e22),
                           (255,
                            255,
                            255),
                           "star",
                           False)
        STAR.yv = random.gauss(-225e4,
                               50e3)
        STAR.xv = random.gauss(225e4,
                               50e3)
        bodies.append(STAR)

print(len(bodies))
