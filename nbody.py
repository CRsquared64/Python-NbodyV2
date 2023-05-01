import numpy as np

WIDTH, HEIGHT = 1920, 1080

'''

This Class is taken from my previous Nbody Simulation in python and can be found here:
https://github.com/CRsquared64/3D-Nbody/blob/main/nbody.py


'''
class Nbody:
    G = 6.67428e-11  # can also be 1, makes some difference
    AU = 149.6e6 * 1000
    distance_to_moon = 3.84399 * 10 ** 8
    PLUTO_TO_CHARON = 19640 * 1000
    TIMESTEP = 3600 * 24  # seconds
    SCALE = 75 / AU  # 75 / AU or 500 / distance-tomoon or 75 * 10 ** -20

    # 106983694 = y

    def __init__(self, x, y, z, radius, mass, colour, identify, use_approximate_nn=False):
        self.x = x
        self.y = y
        self.z = z
        self.identify = identify
        self.radius = radius
        self.mass = mass
        self.colour = colour

        self.use_approximate_nn = use_approximate_nn

        self.trail = []

        self.xv = 0
        self.yv = 0
        self.zv = 0

    def force(self, obj):
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

    def position(self, bodies, nn):
        if self.use_approximate_nn:
            neighbors = nn.query((self.x, self.y, self.z), k=2)
        else:
            neighbors = bodies

        total_force_x = 0
        total_force_y = 0
        total_force_z = 0

        for body in neighbors:
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

        self.trail.append((self.x, self.y, self.z))

    def get_draw_pos(self):
        x = self.x
        y = self.y
        z = self.z
        return x, y, z