import pickle
import numpy as np
from tqdm import tqdm
from numba import njit, cuda

def get_pos(bodies, cycles):
    poses = [[] for i in range(cycles)]
    amount = len(bodies) * cycles
    print("Calculating Positions")
    with tqdm(total=amount) as pb:
        for i in range(cycles):
            for n, body in enumerate(bodies):
                body.position(bodies, 40)
                poses[i].append((*body.get_draw_pos(), body.radius))

                pb.update(1)

    return poses