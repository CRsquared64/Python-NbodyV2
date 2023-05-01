import pygame
import nbody

import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
from tqdm import tqdm

def pygame_setup():
    global win, center_x, center_y
    pygame.init()

    WIDTH = 1920
    HEIGHT = 1080

    win = pygame.display.set_mode((WIDTH, HEIGHT))

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    center_x = screen_width // 2
    center_y = screen_height // 2


def render(poses, dist):
    with tqdm(total=len(poses)) as pb:
        for bodies in range(poses.shape[0]):
            win.fill((0, 0, 0))
            x = poses[bodies, :, 0]
            y = poses[bodies, :, 1]
            z = poses[bodies, :, 2]
            radius = poses[bodies, :, 3]
            for n in range(len(x)):
                x1 = int(x[n])
                y1 = int(y[n])
                z1 = int(z[n])
                radius1 = int(radius[n]) * nbody.Nbody.SCALE


                if z1 == 0:
                    z1 = z1 + 1

                rendered_x = int(x1 + (x1 / z1))
                rendered_y = int(y1 + (y1 / z1))
                dynamic_radius = int(radius1 / z1)

                pygame.draw.circle(win, (255,255,255), (center_x - rendered_x, center_y - rendered_y), dynamic_radius, 0)
            pygame.image.save(win, f'run/image{bodies}.jpg')
            pygame.display.flip()