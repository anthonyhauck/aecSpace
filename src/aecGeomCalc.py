import math
import numpy
import traceback

from aecErrorCheck import aecErrorCheck

class aecGeomCalc:
    
    # An instance of aecErrorCheck.
    __aecErrorCheck = None
    
    
    def __init__(self):
        """
        aecGeomCalc Constructor
        """
        self.__aecErrorCheck = aecErrorCheck()    
    
    def mirrorPoints2D (self, points, mPoints = [(0, 0), (0, 1)]):
        """
        [(2 float),...] mirrorPoints2D([(2 floats),...], [(2 floats), (2 floats)])
        Accepts a set of points and a mirror axis defined by two points
        and returns a set of points reflected around the mirror axis.
        """
        try:
            mPnt1 = mPoints[0]
            mPnt2 = mPoints[1]
            newPoints = []
            if mPnt1[0] == mPnt2[0]: # vertical mirror
                for point in points:
                    point = list(point)
                    distance = abs(point[0] - mPnt1[0]) * 2
                    if point[0] < mPnt1[0]:
                        point[0] += distance
                    else:
                        point[0] -= distance
                    newPoints.append(tuple(point))
                return newPoints
            if mPnt1[1] == mPnt2[1]: # horizontal mirror
                for point in points:
                    point = list(point)          
                    distance = abs(point[1] - mPnt1[1]) * 2                          
                    if point[1] < mPnt1[1]:
                        point[1] += distance
                    else:
                        point[1] -= distance
                    newPoints.append(tuple(point))
                return newPoints           
            mSlope = (mPnt2[1] - mPnt1[1]) / (mPnt2[0] - mPnt1[0])
            rSlope = (-1 / mSlope)
            dSlope = (mSlope - rSlope)
            mYint = ((mSlope * mPnt1[0]) - mPnt1[1]) * -1
            for point in points:                
                rYint = ((rSlope * point[0]) - point[1]) * -1
                xCoord = (rYint - mYint) / dSlope
                yCoord = ((mSlope * rYint) - (rSlope * mYint)) / dSlope
                xDist = abs(point[0] - xCoord)
                yDist = abs(point[1] - yCoord)
                rLength = math.sqrt(xDist + yDist) * 2
                point = numpy.array(list(point))
                mPoint = numpy.array([xCoord, yCoord])
                newPoint = (rLength * (mPoint - point)) + point
                newPoints.append(tuple(newPoint))
            return newPoints
        except:
            return self.__aecErrorCheck.errorMessage \
            (self.__class__.__name__, traceback)
            
# end class