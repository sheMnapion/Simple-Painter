import numpy as np
import cv2 as cv
from line import Line

class Polygon(object):
    """polygon class, supporting draw"""
    def __init__(self,id,points,algorithm,color):
        """store the basical information of a line object"""
        self.id=id
        self.points=points
        self.lines=[]
        for i in range(len(self.points)):
            if i==len(self.points)-1:
                self.lines.append(Line(i,points[i],points[0],algorithm,color))
            else:
                self.lines.append(Line(i,points[i],points[i+1],algorithm,color))
        self.algorithm=algorithm
        self.color=color
    
    def draw(self,pic):
        """draw the polygon on a given picture"""
        print("POLYGON DRAWING")
        print("Number of lines:%d" % (len(self.lines)))
        for line in self.lines:
            line.draw(pic)
    
    def translate(self,dx,dy,w,h):
        """translate the polygon on a given canvas with shape w*h"""
        for i, line in enumerate(self.lines):
            state=line.translate(dx,dy,w,h)
            if state==False:
                for j in range(i):
                    self.lines[j].translate(-dx,-dy,w,h) # move back to enable synchronize
                return False
        return True
    
    def rotate(self,x,y,r,w,h):
        """rotate the polygon on a given canvas centered at (x,y)"""
        for i, line in enumerate(self.lines):
            state=line.rotate(x,y,r,w,h)
            if state==False:
                for j in range(i):
                    self.lines[j].rotate(x,y,-r,w,h)
                return False
        return True

    def scale(self,x,y,s,w,h):
        """scale the polygon on a given canvas centered at (x,y)"""
        for i, line in enumerate(self.lines):
            state=line.scale(x,y,s,w,h)
            if state==False:
                for j in range(i):
                    self.lines[j].scale(x,y,1.0/s,w,h)
                return False
        return True
    
    def dist(self,p):
        """nearest euclid distance"""
        if len(self.lines)==0:
            return 1e6
        dists=[line.dist(p) for line in self.lines]
        return min(dists)