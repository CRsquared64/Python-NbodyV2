
import random
from nbody import Nbody
import numpy as np

# Set the number of bodies in each galaxy
n_bodies = 2000

# Set the initial separation between the two galaxies
separation = 1e8

# Set the mass of the central black hole in each galaxy
m_bh = 1e9

# Set the scale length of the spiral arms in each galaxy
r_arm = 2e7

# Set the width of the spiral arms in each galaxy
w_arm = 1e6

# Create two lists to store the bodies in each galaxy
galaxy1 = []
galaxy2 = []

def generate_spiral_galaxy(n_bodies, m_bh, r_arm, w_arm):
    # Generate random angles for each body
    theta = np.random.uniform(0, 2*np.pi, n_bodies)

    # Generate random radii for each body following a distribution that has
    # a higher probability at smaller radii (to simulate a bulge at the center)
    r = np.abs(np.random.normal(loc=0, scale=1, size=n_bodies))
    r = r**2

    # Calculate the x and y coordinates of each body based on the angles and radii
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Set the z-coordinate of each body to zero (since we are working in 2D)
    z = np.zeros(n_bodies)

    # Calculate the distance of each body from the center of the galaxy
    d = np.sqrt(x**2 + y**2 + z**2)

    # Calculate the initial velocities of each body to follow a circular orbit
    # around the center of the galaxy, with a small perturbation to simulate
    # the spiral arms
    v_circ = np.sqrt(Nbody.G * m_bh / d)
    v_perturb = w_arm * np.exp(-r**2 / (2*r_arm**2)) * np.sin(theta)
    vx = -v_circ * y / d + v_perturb
    vy = v_circ * x / d + v_perturb
    vz = np.zeros(n_bodies)

    # Assign random masses to each body
    m = np.random.uniform(1e20, 1e22, n_bodies)

    # Create a list of Nbody objects for the galaxy
    galaxy = []
    for i in range(n_bodies):
        body = Nbody(x[i], y[i], z[i], 6.3781*10**6, m[i], (0, 0, 255), "galaxy1")
        body.xv = vx[i]
        body.yv = vy[i]
        body.zv = vz[i]
        galaxy.append(body)

    return galaxy

# Generate the bodies in the first galaxy
galaxy1 = generate_spiral_galaxy(n_bodies, m_bh, r_arm, w_arm)

# Generate the bodies in the second galaxy
galaxy2 = generate_spiral_galaxy(n_bodies, m_bh, r_arm, w_arm)
for body in galaxy2:
    body.x += separation
    body.color = (255, 0, 0)
    body.name = "galaxy2"

# Combine the two galaxies into a single list of

bodies = galaxy1 + galaxy2