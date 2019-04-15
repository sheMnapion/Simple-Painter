# This file implements the line class
import numpy as np

class Line(object):
    def __init__(self,id,startPoint,endPoint,algorithm):
        self.id=id
        self.startPoint=startPoint
        self.endPoint=endPoint
        self.algorithm=algorithm