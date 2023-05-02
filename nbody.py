import numpy as np
import pynndescent
import numba
from typing import List
from numba import jit, float64, int64
from numba.experimental import jitclass
import nbody
from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

WIDTH, HEIGHT = 1920, 1080
spec = [
    ('x', float64),
    ('y', float64),
    ('z', float64),
    ('identify', numba.types.unicode_type),
    ('radius', float64),
    ('mass', float64),
    ('colour', numba.types.UniTuple(numba.types.int64, 3)),
    ('use_approximate_nn', numba.types.boolean),
    ('xv', float64),
    ('yv', float64),
    ('zv', float64),
    ('G', float64),
    ('AU', float64),
    ('distance_to_moon', float64),
    ('PLUTO_TO_CHARON', float64),
    ('TIMESTEP', float64),
    ('SCALE', float64)
]

@jitclass(spec)
class Nbody:

    def __init__(self, x, y, z, radius, mass, colour, identify, use_approximate_nn=False):
        global SCALE
        self.x = x
        self.y = y
        self.z = z
        self.identify = identify
        self.radius = radius
        self.mass = mass
        self.colour = colour

        self.use_approximate_nn = use_approximate_nn

        self.xv = 0
        self.yv = 0
        self.zv = 0
        self.G = 1 * 0.6 #* 6.67428e-11  # can also be 1, makes some difference
        self.AU = 149.6e6 * 1000
        self.distance_to_moon = 3.84399 * 10 ** 8
        self.PLUTO_TO_CHARON = 19640 * 1000
        self.TIMESTEP = 3600 * 24 * 365 * 100000  # seconds
        self.SCALE = 1.5e-20  # / distance_to_moon  # 75 / AU or 500 / distance-tomoon or 75 * 10 ** -20

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and \
            self.identify == other.identify and self.radius == other.radius and \
            self.mass == other.mass and self.colour == other.colour and \
            self.use_approximate_nn == other.use_approximate_nn and \
            self.xv == other.xv and self.yv == other.yv and self.zv == other.zv and \
            self.G == other.G and self.AU == other.AU and \
            self.distance_to_moon == other.distance_to_moon and \
            self.PLUTO_TO_CHARON == other.PLUTO_TO_CHARON and \
            self.TIMESTEP == other.TIMESTEP and self.SCALE == other.SCALE

    #@numba.jit(nopython=True)
    def force(self, obj : List[type]):
        obj_x = obj.x
        obj_y = obj.y
        obj_z = obj.z
        obj_dist = np.array([obj_x, obj_y, obj_z]) - np.array([self.x, self.y, self.z])
        dist = np.linalg.norm(obj_dist)

        force = self.G * self.mass * obj.mass / dist ** 2
        force_vector = force * obj_dist / dist

        force_x = force_vector[0]
        force_y = force_vector[1]
        force_z = force_vector[2]

        return force_x, force_y, force_z

    #@numba.jit(nopython=True)
    def position(self, bodies : numba.types.List):

        total_force_x = 0
        total_force_y = 0
        total_force_z = 0

        for body in bodies:
            if self == body:
                continue

            force_x, force_y, force_z = self.force(body)
            total_force_x += force_x
            total_force_y += force_y
            total_force_z += force_z

        # Update the velocity and position of this body based on the total force
        self.xv += total_force_x / self.mass * self.TIMESTEP
        self.yv += total_force_y / self.mass * self.TIMESTEP
        self.zv += total_force_z / self.mass * self.TIMESTEP

        self.x += self.xv * self.TIMESTEP
        self.y += self.yv * self.TIMESTEP
        self.z += self.zv * self.TIMESTEP

    def get_draw_pos(self):
        x = self.x * self.SCALE
        y = self.y * self.SCALE
        z = self.z * self.SCALE
        return x, y, z
