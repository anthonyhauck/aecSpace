"""
aecSpaceFloorExample

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

# Create a rectangular aecSpace at the origin.

space.makeBox([0, 0, 0], [20, 30, 20])
space.setBoundary([[0, 0], [20, 0], [60, 40], [30, 70], [10, 70]])
newSpace = spacer.copy(space, [0, 0, 20])
newSpace.mirror()
spaces = [space, newSpace]
     
# Initialize the pythonOCC display.

display, start_display, add_menu, add_function_to_menu = init_display()

# Call the instance of aecSpaceDrawOCC to draw 
# the aecSpaces in the pythonOCC environment.

spaceDrawer.Draw3D(display, spaces)

# Start the pythonOCC display.

start_display()