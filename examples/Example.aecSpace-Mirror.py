"""
aecSpaceExample-Mirror

Assuming you've downloaded this source to your desktop, these instructions
should work.

These classes and this example were developed using the Anaconda development
environment, relevant due to the need for the pythonOCC toolkit, a Python
wrapper around the open source openCascade geometry kernel. The conda package
manager makes it easy to install pythonOCC.

To install Anaconda, visit https://www.anaconda.com/download/

To install pythonOCC, open the Anaconda prompt (not the OS command prompt!)
that you should find installed as a separate application from Anaconda 
Navigator, and paste in this line from http://www.pythonocc.org/download/

conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.18.1

aecSpace uses the shapely, sympy, numpy, and scipy libraries for geometric 
operations, so you'll need those as well:
    
conda install -c conda-forge shapely
conda install -c conda-forge sympy
conda install -c conda-forge scipy

numpy should already be installed with Anaconda.

After this you theoretically have everything you need to run this example.
Make sure your IDE can find the folder where you've stored these *.py files.
All the code outside of any aecSpaceExample-*.py file has been encapsulated 
as discrete objects.

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co
"""

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

# Create a five-sided aecSpace at the origin.

space.setBoundary([(0, 0), (20, 0), (60, 40), (30, 70), (10, 70)])
space.setHeight(15)
newSpace = spacer.copy(space, (0, 0, 20))
newSpace.mirror()
spaces = [space, newSpace]
     
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = True)
