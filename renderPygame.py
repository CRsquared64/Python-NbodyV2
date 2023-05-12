import numpy
import numpy as np
import pygame
import nbody
import glob
import cv2 as cv
import os
#os.environ["SDL_VIDEODRIVER"] = "dummy"
from tqdm import tqdm
import random


def pygame_setup():
    global win, center_x, center_y, font
    pygame.init()

    WIDTH = 1920
    HEIGHT = 1080

    win = pygame.display.set_mode((WIDTH, HEIGHT))

    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    center_x = screen_width // 2
    center_y = screen_height // 2
    font = pygame.font.SysFont(None, 16)
    # print(center_x, center_y)


def render(poses):
    with tqdm(total=len(poses)) as pb:
        i = 0
        for bodies in range(poses.shape[0]):
            win.fill((0, 0, 0))
            x = poses[bodies, :, 0]
            y = poses[bodies, :, 1]
            z = poses[bodies, :, 2]
            data = np.column_stack((x,y,z))
            open(f"data/test{i}.txt", 'w').close()
            numpy.savetxt(f"data/test{i}.txt", data)
            i = i + 1
            radius = poses[bodies, :, 3]
            for n in range(len(x)):
                x1 = int(x[n])
                y1 = int(y[n])
                z1 = int(z[n])
                radius1 = int(radius[n]) * 1  # depracated, all radius is 1
                # print(x1, y1, z1, radius1)

                if z1 == 0:
                    z1 = z1 + 1

                rendered_x = int(x1 + (x1 / z1))
                rendered_y = int(y1 + (y1 / z1))
                if radius1 == 69:
                    dynamic_radius = 5
                else:
                    dynamic_radius = 1

                # print(f"Render X: {rendered_x}, Rendered Y: {rendered_y}, Rendered Radius: {dynamic_radius}")
                try:
                    pygame.draw.circle(win, (255, 255, 255), (int(center_x - rendered_x), int(center_y - rendered_y)),
                                       dynamic_radius, 0)
                    #print("On Screen")
                except TypeError:
                    #print("Not On screen")
                    pass

            pygame.image.save(win, f'run/image0{bodies}.jpg')
            pb.update(1)
            pygame.display.flip()


def coord_obscuration(x,y,k,r):
    xnoise = []
    ynoise = []
    for i in range(k):
        x_noise = random.randint(x - r, x + r)
        y_noise = random.randint(y - r, x + r)
        xnoise.append(x_noise)
        ynoise.append(y_noise)
    return xnoise, y_noise


def render_c(folder):
    i = 0
    scale_f = 0.6
    color_scale = 8

    # Get positions from the first frame
    first_frame_data = numpy.loadtxt(f'{folder}/Nbodypositions_{i}.txt')
    x0 = first_frame_data[:, 0]
    y0 = first_frame_data[:, 1]
    z0 = first_frame_data[:, 2]



    # Find the distance from the first body to all other bodies (for the first half)
    distances_first_half = numpy.sqrt((x0[0] - x0[:len(x0)//2]) ** 2 + (y0[0] - y0[:len(y0)//2]) ** 2 + (z0[0] - z0[:len(z0)//2]) ** 2)
    max_distance_first_half = numpy.max(distances_first_half)

    # Find the distance from the second body to all other bodies (for the second half)
    distances_second_half = numpy.sqrt((x0[1] - x0[:len(x0) // 2]) ** 2 + (y0[1] - y0[:len(y0) // 2]) ** 2 + (z0[1] - z0[:len(z0) // 2]) ** 2)
    max_distance_second_half = numpy.max(distances_second_half)

    for files in os.listdir(folder):
        win.fill((0, 0, 0))
        data = numpy.loadtxt(f'{folder}/Nbodypositions_{i}.txt')
        x = data[:, 0]
        y = data[:, 1]
        z = data[:, 2]
        bodies_count = len(x)
        credit_text = "Copyright Callum Redpath 2023 (CRsquared64)"
        for n in range(len(x)):
            x1 = int(x[n]) * scale_f
            y1 = int(y[n]) * scale_f
            z1 = int(z[n])

            if n < len(x + 1) // 2:
                # Calculate the normalized distance for the first half
                distance = numpy.sqrt((x0[0] - x[n]) ** 2 + (y0[0] - y[n]) ** 2 + (z0[0] - z[n]) ** 2)
                normalized_distance = distance / max_distance_first_half
                red = 255
                green = int(255 * (1 - normalized_distance) ** color_scale)
                blue = int(255 * (1 - normalized_distance) ** color_scale)
                color = (red, green, blue)
            else:
                # Calculate the normalized distance for the second half
                distance = numpy.sqrt((x0[1] - x[n]) ** 2 + (y0[1] - y[n]) ** 2 + (z0[1] - z[n]) ** 2)
                normalized_distance = distance / max_distance_second_half
                red = int(255 * (1 - normalized_distance) ** color_scale)
                green = int(255 * (1 - normalized_distance) ** color_scale)
                blue = 255
                color = (red, green, blue)

            # Assign color based on the normalized distance



            try:
                pygame.draw.circle(win, color, (int(center_x - x1), int(center_y - y1)), 1, 0)
            except ValueError:
                color = (0, 0, 0)
                pygame.draw.circle(win, color, (int(center_x - x1), int(center_y - y1)), 1, 0)
            except TypeError as e:
                pass
        text = f"{i} Cycles"
        bodies_text = f"{bodies_count} Bodies In Simulation"
        bodies_surface = font.render(bodies_text, True, (255,255,255))
        credit_surface = font.render(credit_text, True, (255,255,255))

        text_surface = font.render(text, True, (255,255,255))
        win.blit(text_surface, (0,0))
        win.blit(bodies_surface, (0, 18))
        win.blit(credit_surface, (0, 36))
        pygame.image.save(win, f'run/image0{i}.jpg')
        i += 1
        pygame.display.flip()


def img2vid(FPS, vid_id, cycles):
    filenames = sorted(glob.glob("run/*.jpg"), key=os.path.getmtime)

    images = [cv.imread(img) for img in filenames]
    img_amount = len(images)

    video_name = f"{vid_id}_{cycles}_nbody.mp4"
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    video = cv.VideoWriter(video_name, fourcc, FPS, (1920, 1080))

    print("Creating Video From Frames")
    with tqdm(total=img_amount) as pb:
        for img in images:
            video.write(img)
            pb.update(1)

    cv.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    pygame_setup()
    print("Pygame Setup Completed")
    render_c("c_positions")
    img2vid(120, "cbodies", 100)