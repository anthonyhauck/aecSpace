# aecSpace 0.5 | 2018.04.18
Python classes useful for creating and editing volumes indicating building spaces.

# 0.5 Version Notes

* New aecSpaceGroup object provides multiple functions for querying and changing multiple aecSpace instances at once.
* New fucnction aecSpace.fitWithin() trims aecSpace boundary to the limits of another larger boundary.
* New function aecErrorCheck.checkIndices() aids in constructing acceptable list of integeer indices.
* New function aecSpacer.stackToArea() stacks aecSpaces until the aggregate area meets or exceeds the area argument.
* New function aecGeomCalc.containsPoint() returns boolean test result of a point within a boundary.
* New function aecGeomCalc.containsShape() returns boolean test result of a boundary within a boundary.
* New function aecGeomCalc.findpoint() returns a random point inside a boundary.
* New function aecGeomCalc.getDifference() returns point lists of boundaries unshared between two intersecting boundaries.
* New function aecGeomCalc.getIntersection() returns a point list of the boundary shared between two intersecting boundaries.

* aecShaper object functionality combined into aecSpace object; aecShaper object eliminated.

* aecSpace.makeCylinder() replaces aecShaper.makeCircle and provides a parameter to set the aecSpace height.
* aecSpace.makePolygon() now provides a parameter to set the aecSpace height.
* aecSpace.wrap() function now refactored into separate function convexHull() in aecGeomCalc object.

* aecSpacer.column() function now refactored into single aecSpacer.row() function with an axis argument.
* aecSpace and aecSpaceGroup function getProperties() returns a dictionary of internal instance parameters.
* aecSpace.getProperty() retrieves internal properties by name.
* aecSpace.setProperty() directly sets instance properties, bypassing error checking (dangerous!).
* aecSpacer object functions no longer return the delivered aecSpace in the list of copied spaces.

* aecSpaceDrawOcc.draw3D() now accepts either a list of aecSpaces as before or a single aecSpaceGroup instance.

* aecErrorCheck and aecGeomCalc objects are now shared as single instances between multiple instances of other objects.

* Function parameter error checking extensively enhanced -- they're not bulletproof, but they're less fragile.
* Functions in source now entirely in alphabetical order by function name, rather than the former idiosyncratic organization.
* Function and object documentation heavily corrected, revised, and enhanced.
* Fixed a bug in aecSpacer.stack() that inaccurately placed aecSpaces when starting higher than level 0.
* Eliminated redundant code in aecSpace.mirror() function in favor of code in aecGeomCalc.mirrorPoints2D()

# 0.41 Version Notes 

This version is a wide-ranging overhaul of the aecSpace object, adding numeric mesh representations, normalizing
interactions across multiple functions, updating documentation, and cleaning up shared data issues.

* Redundant colinear points are now removed from point supplied to aecSpace.setBoundary().
* New getMesh* functions return various mesh representations of aecSpace surfaces and the volume.
* New getNorml* functions return point and surface normals.
* New getAngles() function returns internal and external angles of perimeter vertices.
* Internal data handling updated for ease of initialization and future serialization.
* Most point arguments and returns are 3D by default.
* Distinct "2D" point functions collapsed into single functions with an argument to return 2D points if desired.
* New aecVertex object describes point, angles, and point normals.
* New aecGeomCalc function areColinear() tests whether points are colinear.
* New aecGeomCalc function rmvColinear() removes redundant colinear points from the delivered point list.
* New aecErrorCheck function makePercentage() converts numeric arguments to percentages between 0 and 1.
* Exception error reporting made simpler and reliable.
* Renamed example files for easier sorting out from source files in a single folder.
* 0.41: Fixed a bug that allowed MultiPolygons as the boundary definition by merging multipolygons.

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
