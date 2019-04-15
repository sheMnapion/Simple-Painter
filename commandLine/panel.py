import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from line import *

class Panel(object):
    """Class panel for drawing"""
    
    def __init__(self):
        self.w=100
        self.h=100
        self.drawColor=[0,0,0]
        self.elements={} # no installed elements
        self.canvas=np.ones((100,100,3),dtype=np.uint8)*255

    def resetCanvas(self,w,h):
        self.canvas=np.ones((h,w,3),dtype=np.uint8)*255
        self.w=w; self.h=h
        self.elements={} # clear all stored elements
    
    def saveCanvas(self,fileName):
        fileName=fileName+'.bmp'
        cv.imwrite(fileName,self.canvas)
    
    def setColor(self,r,g,b):
        self.drawColor=[b,g,r] # opencv stores everything in BGR order
    
    def display(self):
        showImg=cv.cvtColor(self.canvas,cv.COLOR_BGR2RGB)
        plt.imshow(showImg); plt.show()
    
    def DDADrawLine(self,x1,y1,x2,y2):
        """draw a line using DDA algorithm"""
        if x1==x2: # vertical to x axis
            x=int(round(x1))
            yStart=min(y1,y2); yEnd=max(y1,y2)
            for y in range(int(round(yStart)),int(round(yEnd))):
                self.canvas[x][y]=self.drawColor
        elif y1==y2: # parallel to x axis
            y=int(round(y1))
            xStart=min(x1,x2); xEnd=max(x1,x2)
            for x in range(int(round(xStart)),int(round(xEnd))):
                self.canvas[x][y]=self.drawColor
        else:
            m=(y2-y1)/(x2-x1)
            if np.abs(m)>1.0: # grow by y
                yStart=min(y1,y2)
                yEnd=max(y1,y2)
                xStart=x1
                if yStart==y2: xStart=x2
                for i,y in enumerate(range(int(round(yStart)),int(round(yEnd)))):
                    xPoz=xStart+(1.0/m)*i
                    self.canvas[int(round(xPoz))][y]=self.drawColor
            else:
                xStart=min(x1,x2)
                xEnd=max(x1,x2)
                yStart=x1
                if xStart==x2: yStart=y2
                for i,x in enumerate(range(int(round(xStart)),int(round(xEnd)))):
                    yPoz=yStart+m*i
                    self.canvas[x][int(round(yPoz))]=self.drawColor                 

    def drawLine(self,id,x1,y1,x2,y2,algorithm,useLib=False):
        """Draw a line on the panel"""
        if self.elements.has_key(id):
            print "\033[31mThe id for the line has been registered! Please use another one\033[0m"
            return
        y1=self.h-y1
        y2=self.h-y2
        if useLib==True:
            cv.line(self.canvas,(int(x1),int(y1)),(int(x2),int(y2)),self.drawColor,1)
            return
        lineEle=Line(id,(x1,y1),(x2,y2),algorithm)
        self.elements[id]=lineEle
        if algorithm=='DDA':
            self.DDADrawLine(y1,x1,y2,x2)