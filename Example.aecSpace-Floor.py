"""
aecSpaceExample-Floor

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co
"""

import random

# Import the classes we'll need.

from aecSpace.aecColor import aecColor
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpaceDrawOCC import aecSpaceDrawOCC

# Create class instances.

colors = aecColor()
space = aecSpace()
spacer = aecSpacer()
spaces = aecSpaceGroup()
spaceDrawer = aecSpaceDrawOCC()

# Create a rectangular aecSpace at the origin.

space.points_floor = [aecPoint(0, 0), 
                      aecPoint(20, 0), 
                      aecPoint(30, 30), 
                      aecPoint(20, 50), 
                      aecPoint(0, 50)]
space.height = 5

# Create copies of the initial aecSpace and arrange them in a row.

floors = spacer.row(space, 3, 3)

for room in floors:
    floors = floors + spacer.stack(room, 5, 0)
    
for room in floors:
    floors = floors + spacer.row(room, 3, 3, False)

for room in floors:
    room.color.color = ([random.randint(0, 255), random.randint(0, 255),random.randint(0, 255)])
    if room.color.color_01[0] > 0.5:
        room.mirror()
    
#spaces.add(floors)   
spaceDrawer.draw3D(floors, displaySize = (1600, 900), update = False)
# update = True animates the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.
