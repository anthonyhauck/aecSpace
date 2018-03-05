"""
aecSpaceRowColumnMirrorExample

Assuming you've downloaded this source to your desktop, these instructions
should work.

These classes and this example were developed using the Anaconda development
environment, relevant due to the need for the pythonOCC toolkit, a Python
wrapper around the open source openCascade geometry kernel. The conda package
manager makes it easy to install pythonOCC.

To install Anaconda, visit https://www.anaconda.com/download/

To install pythonOCC, open the Anaconda prompt (not the OS command prompt!)
that you should find installed as a separate aplication from Anaconda 
Navigator, and paste in this line from http://www.pythonocc.org/download/

conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.18.1

After this you theoretically have everything you need to run this example.
Make sure your IDE can find the folder where you've stored these *.py files.
All the code outside of any *Example.py file has been encapsulated as discrete
objects.

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co

"""

import random

# aecSpaceDrawOCC imports all the rest of the pythonOCC components necessary.
# Here we just import enough to initalize the display. All other classes are 
# abstract geometry and have no dependency on the pythonOCC toolkit.

from OCC.Display.SimpleGui import init_display

# Import the classes we'll need.

from aecColors import aecColors
from aecSpace import aecSpace
from aecSpacer import aecSpacer
from aecSpaceDrawOCC import aecSpaceDrawOCC

# Create class instances.

colors = aecColors()
space = aecSpace()
spacer = aecSpacer()
spaceDrawer = aecSpaceDrawOCC()

# Create an aecSpace at the origin.

space.setBoundary([[0, 0], [20, 0], [60, 40], [30, 70], [10, 70]])
space.setHeight(10)

# Create copies of the initial aecSpace and arrange them in a row.

firstTower = spacer.stack(space, 9, 1)
rowTowers = []
for floor in firstTower:
    rowTowers += spacer.row(floor, 2, 70)

columnTowers = []
for floor in rowTowers:
    columnTowers += spacer.column(floor, 1, 70)
    
spaces = firstTower + rowTowers + columnTowers
    
for floor in spaces:
    floor.setColor(
        [random.randint(0, 255), 
         random.randint(0, 255),
         random.randint(0, 255)])
    
for floor in firstTower:
    if floor.getColor256()[0] > 100:
        if floor.getColor256()[1] < 100:
            floor.mirror(floor.getAxisMajor2D())
            floor.rotate(random.randint(0, 3))
        else:
            floor.mirror(floor.getAxisMinor2D())
            floor.rotate(random.randint(3, 6))
            
for floor in rowTowers:
    if floor.getColor256()[0] > 100:
        if floor.getColor256()[1] < 100:
            floor.mirror(floor.getAxisMajor2D())
            floor.rotate(random.randint(0, 3))
        else:
            floor.mirror(floor.getAxisMinor2D())
            floor.rotate(random.randint(3, 6))
            
for floor in columnTowers:
    if floor.getColor256()[0] > 100:
        if floor.getColor256()[1] < 100:
           floor.mirror(floor.getAxisMajor2D())
           floor.rotate(random.randint(0, 3))
        else:
            floor.mirror(floor.getAxisMinor2D())
            floor.rotate(random.randint(3, 6))
     
# Initialize the pythonOCC display.

display, start_display, add_menu, add_function_to_menu = init_display()

# Call the instance of aecSpaceDrawOCC to draw 
# the aecSpaces in the pythonOCC environment.

spaceDrawer.Draw3D(display, spaces)

# Start the pythonOCC display.

start_display()