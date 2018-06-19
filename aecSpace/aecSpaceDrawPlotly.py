import plotly.graph_objs as graph
import plotly
import traceback

from typing import List

from .aecSpace import aecSpace

"""
aecSpaceDrawPlotly accepts lists of aecSpaces or an
aecSpaceGroup instance to render in plotly.
"""

class aecSpaceDrawPlotly:
   
    def __init__(self):
        """
        aecSpaceDrawOCC Constructor
        Creates a new aecErrorCheck object.
        """
        pass
   
    def draw3D(self, spaces: List[aecSpace]) -> bool:
        """
        Accepts an aecSpaceGroup object and renders its list of aecSpaces to the plotly display.
        Returns True on success failure.
        Returns False on failure.
        """
        try:
            for space in spaces:
                mesh = space.mesh
                vertices = mesh.vertices
                indices = mesh.indices
                xGroup =  [vtx[0] for vtx in vertices]
                yGroup =  [vtx[1] for vtx in vertices]
                zGroup =  [vtx[2] for vtx in vertices]
                iGroup =  [idx[0] for idx in indices]
                jGroup =  [idx[1] for idx in indices]
                kGroup =  [idx[2] for idx in indices]            
                trace = graph.Mesh3d(x = xGroup, y = yGroup, z = zGroup, 
                                     i = iGroup, j = jGroup, k = kGroup)
            plotly.offline.plot([trace])           
            return True
        except Exception:
            traceback.print_exc()
            return False

# end class

