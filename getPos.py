import pickle
import numpy as np
from tqdm import tqdm
from numba import njit, cuda

def get_pos(bodies, cycles):
    data = np.array([[body.x, body.y, body.z] for body in bodies])
    poses = [[] for i in range(cycles)]
    amount = len(bodies) * cycles
    #nn = NNDescent(data)
    print("Calculating Positions")
    with tqdm(total=amount) as pb:
        for i in range(cycles):
            for n, body in enumerate(bodies):
                body.position(bodies, 2)
                poses[i].append((*body.get_draw_pos(), body.radius))

                pb.update(1)
    with open('nbodies.pos', 'wb') as handle:
        pickle.dump(poses, handle)
    return poses