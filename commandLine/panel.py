import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from line import Line
from polygon import Polygon
from ellipse import *
from curve import *
import time

class Panel(object):
    """Class panel for drawing"""
    
    def __init__(self,outputDir='./'):
        self.w=100
        self.h=100
        self.drawColor=[0,0,0]
        self.elements={} # no installed elements
        self.canvas=np.ones((100,100,3),dtype=np.uint8)*255
        self.sync=True
        self.outputDir=outputDir

    def deleteElement(self,deleteID):
        """delete an element from canvas
            specially used for gui
        """
        if deleteID in self.elements.keys():
            del self.elements[deleteID]
            self.sync=False
        else:
            print("The element to delete doesn't exist!")
        # print self.elements

    def resetCanvas(self,w,h):
        self.canvas=np.ones((h,w,3),dtype=np.uint8)*255
        self.w=w; self.h=h
        self.elements={} # clear all stored elements
        self.sync=True

    def _drawOnCanvas(self):
        """draw all the elements on the canvas"""
        self.canvas=np.ones(self.canvas.shape,dtype=np.uint8)*255
        for key in self.elements:
            graphElement=self.elements[key]
            graphElement.draw(self.canvas)
        self.sync=True

    def saveCanvas(self,fileName):
        """save the canvas of present object, so if not synced, draw now"""
        if self.sync==False:
            self._drawOnCanvas()
        fileName=self.outputDir+fileName+'.bmp'
        cv.imwrite(fileName,self.canvas)
    
    def checkInBound(self,value,checkEdge):
        """check whether the point input is valid"""
        assert(checkEdge==0 or checkEdge==1)
        if checkEdge==0: # width
            assert(value>=0 and value<self.w)
        else:
            assert(value>=0 and value<self.h)

    def setColor(self,r,g,b):
        self.drawColor=[b,g,r] # opencv stores everything in BGR order
    
    def display(self):
        if self.sync==False:
            self._drawOnCanvas()        
        showImg=cv.cvtColor(self.canvas,cv.COLOR_BGR2RGB)
        plt.imshow(showImg); plt.show()

    def getPic(self):
        """get picture for present panel; """
        if self.sync==False:
            self._drawOnCanvas()
        return self.canvas

    def drawLine(self,id,x1,y1,x2,y2,algorithm,useLib=False):
        """Draw a line on the panel"""
        if id in self.elements.keys():
            print("The id for the line has been registered! Please use another one")
            return
        y1=self.h-1-y1
        y2=self.h-1-y2
        try:
            self.checkInBound(x1,0); self.checkInBound(x2,0)
            self.checkInBound(y1,1); self.checkInBound(y2,1)
        except AssertionError as e:
            # print self.canvas.shape
            # print self.w,self.h,x1,y1,x2,y2
            print("Some value is out of bound! Please check your input")
            return
        lineEle=Line(id,(y1,x1),(y2,x2),algorithm,self.drawColor)
        self.elements[id]=lineEle
        self.sync=False 
    
    def drawPolygon(self,id,points,algorithm):
        """draw a polygon on the panel"""
        if id in self.elements.keys():
            print("The id for the polygon has been registered! Please use another one")
            return
        for i, p in enumerate(points):
            x=p[0]; y=self.h-1-p[1]
            try:
                self.checkInBound(x,0); self.checkInBound(y,1)
            except AssertionError as e:
                # print self.w,self.h,x,y
                print("Some value is out of bound! Please check your input")
                return
        points=[(self.h-1-p[1],p[0]) for p in points]
        polygonEle=Polygon(id,points,algorithm,self.drawColor)
        self.elements[id]=polygonEle
        self.sync=False        
    
    def drawCurve(self,id,points,algorithm):
        """draw a curve on the panel"""
        if id in self.elements.keys():
            print("The id for the curve has been registered! Please use another one")
            return        
        for i, p in enumerate(points):
            x=p[0]; y=self.h-1-p[1]
            try:
                self.checkInBound(x,0); self.checkInBound(y,1)
            except AssertionError as e:
                # print self.w,self.h,x,y
                print("Some value is out of bound! Please check your input")
                return
        points=[(self.h-1-p[1],p[0]) for p in points]
        curveEle=Curve(self.drawColor,id,len(points),points,algorithm)
        self.elements[id]=curveEle
        self.sync=False

    def drawEllipse(self,id,x,y,rx,ry):
        """draw an ellipse on the panel"""
        if id in self.elements.keys():
            print("The id for the ellipse has been registered! Please use another one")
            return
        try:
            self.checkInBound(x,0); self.checkInBound(x+rx,0); self.checkInBound(x-rx,0)
        except AssertionError as e:
            print("The ellipse set would be longer than the x axis of canvas!")
            return
        try:
            self.checkInBound(y,0); self.checkInBound(y+ry,0); self.checkInBound(y-ry,0)
        except AssertionError as e:
            print("The ellipse set would be longer than the y axis of canvas!")
            return
        ellipseEle=Ellipse(id,self.h-1-y,x,ry,rx,self.drawColor)
        self.elements[id]=ellipseEle
        self.sync=False
    
    def translate(self,id,dx,dy):
        """translate an element on the panel"""
        if id not in self.elements.keys():
            print("Id input not registered! Please check your process")
            return False
        element=self.elements[id]
        state=element.translate(-dy,dx,self.w,self.h)
        if state==True:
            self.canvas=np.ones((self.h,self.w,3),dtype=np.uint8)*255
            self.sync=False
        return state

    def scale(self,id,x,y,s):
        """scale an element on the panel"""
        if id not in self.elements.keys():
            print("Id input not registered! Please check your process")
            return False
        element=self.elements[id]
        state=element.scale(self.h-1-y,x,s,self.w,self.h)
        if state==True:
            self.canvas=np.ones((self.h,self.w,3),dtype=np.uint8)*255
            self.sync=False
        return state

    def rotate(self,id,x,y,r):
        """translate an element on the panel"""
        if id not in self.elements.keys():
            print("Id input not registered! Please check your process")
            return False
        element=self.elements[id]
        state=element.rotate(self.h-1-y,x,-r,self.w,self.h)
        if state==True:
            self.canvas=np.ones((self.h,self.w,3),dtype=np.uint8)*255
            self.sync=False
        return state
    
    def clip(self,id,x1,y1,x2,y2,algorithm):
        """clip a line on canvas"""
        if id not in self.elements.keys():
            print("The line to clip has not been registered! Please check your process")
            return False
        try:
            self.checkInBound(x1,0); self.checkInBound(x2,0)
            self.checkInBound(y1,1); self.checkInBound(y2,1)
            # assert(x1<=x2); assert(y1<=y2)
        except AssertionError as e:
            # print x1,y1,x2,y2
            print("Illegal clip window coordinates! Please check your input")
            return False
        element=self.elements[id]
        keepElement=element.clip(self.h-1-y1,x1,self.h-1-y2,x2,algorithm)
        if keepElement==False: # delete key
            # print "Deleting", id
            self.elements.pop(id)
        self.canvas=np.ones((self.h,self.w,3),dtype=np.uint8)*255
        self.sync=False