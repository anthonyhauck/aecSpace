# aecSpace 0.6 | 2018.05.17
Python classes useful for creating and editing volumes indicating building spaces and other objects.

# 0.6 Version Notes

New Class aecCompassPoints defines constants referring to local cardinal directions.

aecSpace Class Changes
* New method aecSpace.getCompassPoint returns the boundary intersection of a vector from the centroid to a bounding box point.
* New method aecSpace.getCompassPointBox returns the bounding box intersection of a vector to a division of the bounding box.
* New method aecSpace.moveTo moves the aecSpace relatively from a specified point to a specified point.
* Bug fix: fixed a caching bug that allowed the boundary point list to desynchronize with changes to level and height values.

aecSpacer Class Changes
* New method aecSpacer.placeWithin attempts to place an aecSpace wholly within another aecSpace without altering either.
* New method aecSpacer.placeWithinLine attempts to plavce an aecSpace wholly within another aecSpace without altering either along a specified vector.

aecErrorCheck Changes
* New method aecErrorCheck.checkAngle attempts to correct an angle to fall within a 0 to 360 range.
* New method aecErrorCheck.checkColor attempts to correct a tuple to become a valid color with three values from 0 to 255.

aecGeomCalc Changes
* New method checkBoundingBox attempts to construct valid corner points for a delivered bounding box.

aecColor Class Changes

* Added a Red color constant

Examples Changes
* Added code to set pythonOCC display size.
* Added toggle for displaying animated contruction of a scene.
* Some examples show fewer iterations to speed up time to full display.

# 0.51 Version Notes | 2018.04.25

* New aecSpaceGrid object provides some methodality for creating and manipulating voxel grids. More methodality in progress.
* Added Example.aecSpace-SpaceGrid to demonstrate some of the current methodality.
* New method aecErrorCheck.checkAddress() for checking the formation of voxel addresses.
* New method aecSpaceGroup.getIndices() returns a list of valid indices into the group.
* Added further error checking against aecSpace.move() inputs.
* Added getType() method to objects to return a constant string identifying the object type.
* Added Example.aecSpace-RandomLandDevelopment.py to demonstrate new aecSpaceGroup methodality in version 0.5   
* Fixed a bug in aecSpace and aecSpacer objects that prevented re-initialization of some instance variables.
* Corrected a number of documentation errors.

# 0.5 Version Notes

* New aecSpaceGroup object provides multiple methods for querying and changing multiple aecSpace instances at once.
* New method aecSpace.fitWithin() trims aecSpace boundary to the limits of another larger boundary.
* New method aecErrorCheck.checkIndices() aids in constructing acceptable list of integeer indices.
* New method aecSpacer.stackToArea() stacks aecSpaces until the aggregate area meets or exceeds the area argument.
* New method aecGeomCalc.containsPoint() returns boolean test result of a point within a boundary.
* New method aecGeomCalc.containsShape() returns boolean test result of a boundary within a boundary.
* New method aecGeomCalc.findpoint() returns a random point inside a boundary.
* New method aecGeomCalc.getDifference() returns point lists of boundaries unshared between two intersecting boundaries.
* New method aecGeomCalc.getIntersection() returns a point list of the boundary shared between two intersecting boundaries.

* aecShaper object methodality combined into aecSpace object; aecShaper object eliminated.

* aecSpace.makeCylinder() replaces aecShaper.makeCircle and provides a parameter to set the aecSpace height.
* aecSpace.makePolygon() now provides a parameter to set the aecSpace height.
* aecSpace.wrap() method now refactored into separate method convexHull() in aecGeomCalc object.

* aecSpacer.column() method now refactored into single aecSpacer.row() method with an axis argument.
* aecSpace and aecSpaceGroup method getProperties() returns a dictionary of internal instance parameters.
* aecSpace.getProperty() retrieves internal properties by name.
* aecSpace.setProperty() directly sets instance properties, bypassing error checking (dangerous!).
* aecSpacer object methods no longer return the delivered aecSpace in the list of copied spaces.

* aecSpaceDrawOcc.draw3D() now accepts either a list of aecSpaces as before or a single aecSpaceGroup instance.

* aecErrorCheck and aecGeomCalc objects are now shared as single instances between multiple instances of other objects.

* method parameter error checking extensively enhanced -- they're not bulletproof, but they're less fragile.
* methods in source now entirely in alphabetical order by method name, rather than the former idiosyncratic organization.
* method and object documentation heavily corrected, revised, and enhanced.
* Fixed a bug in aecSpacer.stack() that inaccurately placed aecSpaces when starting higher than level 0.
* Eliminated redundant code in aecSpace.mirror() method in favor of code in aecGeomCalc.mirrorPoints2D()

# 0.41 Version Notes 

This version is a wide-ranging overhaul of the aecSpace object, adding numeric mesh representations, normalizing
interactions across multiple methods, updating documentation, and cleaning up shared data issues.

* Redundant colinear points are now removed from point supplied to aecSpace.setBoundary().
* New getMesh* methods return various mesh representations of aecSpace surfaces and the volume.
* New getNorml* methods return point and surface normals.
* New getAngles() method returns internal and external angles of perimeter vertices.
* Internal data handling updated for ease of initialization and future serialization.
* Most point arguments and returns are 3D by default.
* Distinct "2D" point methods collapsed into single methods with an argument to return 2D points if desired.
* New aecVertex object describes point, angles, and point normals.
* New aecGeomCalc method areColinear() tests whether points are colinear.
* New aecGeomCalc method rmvColinear() removes redundant colinear points from the delivered point list.
* New aecErrorCheck method makePercentage() converts numeric arguments to percentages between 0 and 1.
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

Some of the examples might require up to a minute to run.

# Contact

Please leave questions and comments here or send to the e-mail address below:

Anthony Hauck | Black Arts Consulting
anthony |at| blackarts.co
