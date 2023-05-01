import matplotlib.pyplot as plt
import numpy as np
import random

fig = plt.figure()
ax = plt.axes(projection='3d')
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.grid(False)
ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
def render(poses, dist):
    for bodies in range(poses.shape[0]):
        x = poses[bodies, :, 0]
        y = poses[bodies, :, 1]
        z = poses[bodies, :, 2]
        radius = poses[bodies, :, 3]
        ax.scatter3D(x,y,z, s=radius / 100000, cmap="Blues",c=radius)
        plt.savefig(f'run/images{bodies}.png')
        plt.clf()
