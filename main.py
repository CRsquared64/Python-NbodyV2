import os
import shutil
import sys
import numpy as np

import getPos
#import sim.solarSystem
import sim.spiralSystem
#import sim.galaxyCollison
#import sim.GalaxyCollison2
#import renderMatplot
import renderPygame

#import sim.earthMoonSystem
#import sim.randomBodies
# import sim.plutoCharonSystem
import fileHandler

try:
    os.mkdir('run')
except OSError as error:
    print('Emptying old cache...')
    shutil.rmtree('run')
    os.mkdir('run')



CYCLES = 20
BODIES = sim.spiralSystem.bodies
body_count = len(BODIES)
VID_ID = sim.spiralSystem.video_name

load = False
file = str(sys.argv[1])

if __name__ == '__main__':
    if not load:
        print(f"Generating {body_count} bodies, for {CYCLES} cycles.")
        poses = np.array(getPos.get_pos(BODIES, CYCLES))
        with open('nbodies.pos', 'wb') as handle:
            handle.write(poses)
        print("Generation Finished")
    else:
        poses = np.array(fileHandler.file_load(file))
        print(f"Loaded positions from {file}")
        pass
    #renderMatplot.render(poses, 0)
    #renderMatplot.img2vid(60, "Moon", CYCLES)
    renderPygame.pygame_setup()
    renderPygame.render(poses, 0)
    renderPygame.img2vid(60, "Moon", CYCLES)

