import pickle

from tqdm import tqdm


def get_pos(bodies, cycles):
    nn = False

    poses = [[] for i in range(cycles)]
    amount = len(bodies) * cycles
    print("Calculating Positions")
    with tqdm(total=amount) as pb:
        for i in range(cycles):
            for n, body in enumerate(bodies):
                body.position(bodies, nn)
                poses[i].append((*body.get_draw_pos(), body.radius))

                pb.update(1)
    with open('nbodies.pos', 'wb') as handle:
        pickle.dump(poses, handle)
    return poses