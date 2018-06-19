"""
Example.aecSpaceGrid

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
Anthony Hauck | Black Arts Consulting LLC
anthony@blackarts.co
"""

# Import the classes we'll need.

from aecSpaceGrid import aecSpaceGrid
from aecSpaceDrawOCC import aecSpaceDrawOCC

# Create class instances.

spaceGrid = aecSpaceGrid()
spaceDrawer = aecSpaceDrawOCC()

# Create an eight-celled 3D grid.

spaceGrid.makeCells((0, 0, 0), 2, (20, 3, 3))
spaces = spaceGrid.getCells()
     
spaceDrawer.draw3D(spaces, displaySize = (1600, 900), update = False)
# update = True will animate the example by updating the display after every space placement.
# About 60x slower to completion, but more interesting to watch.