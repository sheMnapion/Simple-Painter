import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

class Panel(object):
    """Class panel for drawing"""
    
    def __init__(self):
        self.w=100
        self.h=100
        self.drawColor=[0,0,0]

    def resetCanvas(self,w,h):
        self.canvas=np.ones((h,w,3),dtype=np.uint8)*255
        self.w=w; self.h=h
    
    def saveCanvas(self,fileName):
        fileName=fileName+'.bmp'
        cv.imwrite(fileName,self.canvas)
    
    def setColor(self,r,g,b):
        self.drawColor=[b,g,r] # opencv stores everything in BGR order
    
    def display(self):
        showImg=cv.cvtColor(self.canvas,cv.COLOR_BGR2RGB)
        plt.imshow(showImg); plt.show()
    
    def drawLine(self,id,x1,y1,x2,y2,algorithm,useLib=False):
        """Draw a line on the panel"""
        if useLib==True:
            cv.line(self.canvas,(int(x1),int(y1)),(int(x2),int(y2)),self.drawColor,1)