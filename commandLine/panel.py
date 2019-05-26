import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from line import *
import time

class Panel(object):
    """Class panel for drawing"""
    
    def __init__(self):
        self.w=100
        self.h=100
        self.drawColor=[0,0,0]
        self.elements={} # no installed elements
        self.canvas=np.ones((100,100,3),dtype=np.uint8)*255
        self.sync=True

    def resetCanvas(self,w,h):
        self.canvas=np.ones((h,w,3),dtype=np.uint8)*255
        self.w=w; self.h=h
        self.elements={} # clear all stored elements
        self.sync=True

    def _drawOnCanvas(self):
        """draw all the elements on the canvas"""
        for key in self.elements:
            graphElement=self.elements[key]
            graphElement.draw(self.canvas)
        self.sync=True

    def saveCanvas(self,fileName):
        """save the canvas of present object, so if not synced, draw now"""
        if self.sync==False:
            self._drawOnCanvas()
        fileName=fileName+'.bmp'
        cv.imwrite(fileName,self.canvas)
    
    def checkInBound(self,value,checkEdge):
        """check whether the point input is valid"""
        assert(checkEdge==0 or checkEdge==1)
        if checkEdge==0: # width
            assert(value>=0 and value<self.h)
        else:
            assert(value>=0 and value<self.w)

    def setColor(self,r,g,b):
        self.drawColor=[b,g,r] # opencv stores everything in BGR order
    
    def display(self):
        if self.sync==False:
            self._drawOnCanvas()        
        showImg=cv.cvtColor(self.canvas,cv.COLOR_BGR2RGB)
        plt.imshow(showImg); plt.show()

    def drawLine(self,id,x1,y1,x2,y2,algorithm,useLib=False):
        """Draw a line on the panel"""
        if self.elements.has_key(id):
            print "\033[31mThe id for the line has been registered! Please use another one\033[0m"
            return
        y1=self.h-1-y1
        y2=self.h-1-y2
        try:
            self.checkInBound(x1,0); self.checkInBound(x2,0)
            self.checkInBound(y1,1); self.checkInBound(y2,1)
        except AssertionError as e:
            print self.w,self.h,x1,y1,x2,y2
            print "\033[31m Some value is out of bound! Please check your input\033[0m"
            return
        lineEle=Line(id,(y1,x1),(y2,x2),algorithm,self.drawColor)
        self.elements[id]=lineEle
        self.sync=False 