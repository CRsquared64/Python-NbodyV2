import os
import shutil
import sys
import numpy as np

import getPos
import sim.solarSystem
#import sim.spiralSystem

import renderMatplot

import sim.earthMoonSystem
# import sim.plutoCharonSystem

try:
    os.mkdir('run')
except OSError as error:
    print('Emptying old cache...')
    shutil.rmtree('run')
    os.mkdir('run')



CYCLES = 24
BODIES = sim.earthMoonSystem.bodies
body_count = len(BODIES)
VID_ID = sim.solarSystem.video_name

load = False
#file = str(sys.argv[1])

if __name__ == '__main__':
    if not load:
        print(f"Generating {body_count} bodies, for {CYCLES} cycles.")
        poses = np.array(getPos.get_pos(BODIES, CYCLES))
        print("Generation Finished")
    else:
        #poses = fileHandler.file_load(file)
        #print(f"Loaded positions from {file}")
        pass
    renderMatplot.render(poses, 0)

