import matplotlib.pyplot as plt
import numpy
import numpy as np
import random
import cv2 as cv
import os

import glob
import nbody

from tqdm import tqdm


fig = plt.figure()
ax = plt.axes(projection='3d')
fig.set_facecolor('black')
ax.set_facecolor('black')

def axis_setup():
    ax.grid(False)
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

def render(poses, dist):
    with tqdm(total=len(poses)) as pb:
        for bodies in range(poses.shape[0]):
            axis_setup()
            x = poses[bodies, :, 0]
            y = poses[bodies, :, 1]
            z = poses[bodies, :, 2]
            radius = poses[bodies, :, 3]
            ax.scatter3D(x,y,z, s=radius / 100000, cmap="Blues",c=radius, depthshade=False)
            plt.savefig(f'run/images{bodies}.jpg')
            ax.clear()
            pb.update(1)
def img2vid(FPS, vid_id, cycles):
    filenames = sorted(glob.glob("run/*.jpg"), key=os.path.getmtime)

    images = [cv.imread(img) for img in filenames]
    img_amount = len(images)

    video_name = f"{vid_id}_{cycles}_{nbody.Nbody.TIMESTEP}.mp4"
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video = cv.VideoWriter(video_name, fourcc, FPS, (960, 720))

    print("Creating Video From Frames")
    with tqdm(total=img_amount) as pb:
        for img in images:
            video.write(img)
            pb.update(1)


if __name__=="__main__":
    data = numpy.loadtxt('c_positions/Nbodypositions_0.txt')
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    axis_setup()
    ax.scatter3D(x, y, z, s=1, cmap="Blues", c=x, depthshade=False)
    plt.show()
