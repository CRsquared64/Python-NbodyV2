import nbody
import random
from nbody import Nbody

global bodies, scale
distance_to_moon = 3.84399 * 10 ** 8

bodies = []
for i in range(40):

    body = nbody.Nbody(random.uniform(-4, 4) * 10 ** 7,random.uniform(-4, 4) * 10 ** 7, 0, 6.3781*10**6 , 5.9742 * 10 ** 24, (0, 0, 255), "earth")
    body.yv = random.uniform(-5,5) * 1000
    body.xv = random.uniform(-5, 5) * 1000
    bodies.append(body)


scale = 100 / distance_to_moon
