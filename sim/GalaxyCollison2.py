import nbody
import random
from nbody import Nbody
import numpy as np

# Set the number of bodies in each galaxy
n_bodies = 100

# Set the initial separation between the two galaxies
separation = 1e8

# Create two lists to store the bodies in each galaxy
galaxy1 = []
galaxy2 = []


def generate_spiral_galaxy(n_bodies, a, b):
    th = np.random.randn(n_bodies)
    x = a * np.exp(b * th) * np.cos(th)
    y = a * np.exp(b * th) * np.sin(th)
    z = np.zeros(n_bodies)
    return x, y, z


x, y, z = generate_spiral_galaxy(n_bodies, 0.5, 0.6)
for i in range(n_bodies):
    mass = random.uniform(1e20, 1e22)
    body = Nbody(x[i], y[i], z[i], 6.3781 * 10 ** 6, mass, (0, 0, 255), "galaxy1")

    # Calculate the distance from the body to the center of the other galaxy
    r = np.sqrt((body.x - separation) ** 2 + body.y ** 2 + body.z ** 2)

    # Calculate the gravitational force between the body and the center of the other galaxy
    F = Nbody.G * body.mass / r ** 2

    # Set the initial velocity of the body to move towards the other galaxy
    body.xv = -np.sqrt(F * r / body.mass) * (body.x - separation) / r
    body.yv = -np.sqrt(F * r / body.mass) * body.y / r
    body.zv = 0

    galaxy1.append(body)

# Generate the bodies in the second galaxy
x, y, z = generate_spiral_galaxy(n_bodies, 0.5, 0.6)
for i in range(n_bodies):
    mass = random.uniform(1e20, 1e22)
    body = Nbody(x[i] + separation, y[i], z[i], 6.3781 * 10 ** 6, mass, (255, 0, 0), "galaxy2")

    # Calculate the distance from the body to the center of the other galaxy
    r = np.sqrt((body.x - separation) ** 2 + body.y ** 2 + body.z ** 2)

    # Calculate the gravitational force between the body and the center of the other galaxy
    F = Nbody.G * body.mass / r ** 2

    # Set the initial velocity of the body to move towards the other galaxy
    body.xv = np.sqrt(F * r / body.mass) * (body.x - separation) / r
    body.yv = np.sqrt(F * r / body.mass) * body.y / r
    body.zv = 0

    galaxy2.append(body)


# Combine the two galaxies into a single list of bodies
bodies = galaxy1 + galaxy2