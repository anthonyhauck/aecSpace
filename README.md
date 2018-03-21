# aecSpace 0.31 | 2018.03.21
Python classes useful for creating and editing volumes indicating building spaces.

# Version Notes

* Added an aecShaper class to provide utilties for creating aecSpaces of various canaonical plan shapes
* aecSpace.addBoundary(points) attempts to add an additional boundary as union to the existing boundary
* aecSpace.Wrap(points) takes over from aecSpacer to wrap a boundary around a set of points
* aecSpace.getPoints() functions changed to aecSpace.getPointsExterior..() to differentiate from future access to interior points
* aecSpace.getPointsExterior3D() now returns two lists of all the bottom and top points, not just the bottom points.
* aecSpace.getSides() returns all the rectangles making up the sides of the aecSpace as a list of 4-point sets.
* aecSpace.getMesh3D() returns an [indices, points] construct. Now tested, fixed, and appears to be working
* Several new examples added, all moved to the examples folder.


# Setup
These classes and examples were developed using the Anaconda development
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

After this you theoretically have everything you need to run these examples.
Make sure your IDE can find the folder where you've stored these *.py files.
All the code outside of any aecSpaceExample-*.py file has been encapsulated 
as discrete objects.

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co
"""

# Geometric Limitations

* Curved walls are represented as a series of straight segments
* No slanted walls
* No sloped floors or ceilings

# Performance Limitations

Some of the examples might require up to 3 seconds to run.

# Contact

Please leave questions and comments here or send to the e-mail address below:

Anthony Hauck | Black Arts Consulting
anthony |at| blackarts.co
