import sys
import numpy as np
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QLabel, QColorDialog)
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QSlider, QLineEdit, QSpinBox
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLCDNumber, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QMainWindow, QErrorMessage
from PyQt5.QtGui import QFont, QPixmap, QImage, QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QSize, pyqtSignal

class DisplayLabel(QLabel):
    """My label class, with mouse event overwritten"""
    def __init__(self,parent=None):
        super(DisplayLabel,self).__init__(parent)
        self.parent=parent
        self.recordPosition=False
        self.inDrawLine=False
        self.inDrawEllipse=False
        self.inDrawPolygon=False
        self.inDrawCurve=False
        self.inTranslation=False
        self.inClipLine=False
        self.setScale=False

        self.firstPoint=[-1,-1]
        self.secondPoint=[-1,-1]
        self.setCenter=False
        self.setDegree=False
        self.points=[]
        self.firstPointSet=False
        
    def startDrawLine(self):
        """set bit information to the state before drawing a line"""
        self.recordPosition=True
        self.inDrawLine=True
        self.firstPoint=[-1,-1]
        self.secondPoint=[-1,-1]

    def startDrawEllipse(self):
        """set bit information to the state before drawing an ellipse"""
        self.recordPosition=True
        self.inDrawEllipse=True
        self.firstPoint=[-1,-1]
        self.secondPoint=[-1,-1]

    def startDrawPolygon(self):
        """set bit information to the state before drawing a polygon"""
        self.recordPosition=True
        self.inDrawPolygon=True
        self.points=[]

    def startDrawCurve(self):
        """set bit information to the state before drawing a curve"""
        self.recordPosition=True
        self.inDrawCurve=True
        self.points=[]

    def startTranslation(self):
        """set bit information to the state before translating"""
        self.recordPosition=True
        self.inTranslation=True
    
    def endTranslation(self):
        """set bit information to the state before translating"""
        self.recordPosition=False
        self.inTranslation=False

    def startClipLine(self):
        """set bit information to the state before clipping a line"""
        self.recordPosition=True
        self.inClipLine=True

    def endClipLine(self):
        """set bit information to stop clipping a line"""
        self.recordPosition=False
        self.inClipLine=False

    def endDrawPolygon(self):
        """set bit information to stop drawing polygon"""
        self.recordPosition=False
        self.inDrawPolygon=False
        self.parent.drawPolygon(self.points)

    def endDrawCurve(self):
        """set bit information to stop drawing polygon"""
        self.recordPosition=False
        self.inDrawCurve=False
        self.parent.drawCurve(self.points)

    def mousePressEvent(self,event):
        """mouse pressed"""
        x=event.pos().x()
        y=event.pos().y()
        # print "Mouse pressed at", x, y
        x,y=self.parent._pointUnderPresentShape([x,y])
        w,h=self.parent.backPanel.canvas.shape[:2]
        # print "True pos:", x, y
        if self.recordPosition==True:
            self.parent.selected=False
            if self.inDrawLine==True:
                self.firstPoint=[x,y]
            elif self.inDrawEllipse==True:
                self.firstPoint=[x,y]
            elif self.inDrawPolygon==True:
                self.points.append([x,y])
            elif self.inDrawCurve==True:
                self.points.append([x,y])
            elif self.inTranslation==True: # two points to decide translation degree
                self.firstPoint=[x,y]
            elif self.inClipLine==True:
                self.firstPoint=[x,y] 
        elif self.setCenter==True:
            self.parent.centerSet=True
            self.parent.center=[x,y]
            self.setCenter=False
            # print "Center set at", [x,y]
            self.parent.operationInterface()    
        elif self.setDegree==True:
            self.firstPointSet=True
            self.firstPoint=[x,y]  
            # print "Operation first point set at",x,y    
        elif self.setScale==True:
            self.firstPointSet=True
            self.firstPoint=[x,y]  
            # print "Operation first point set at",x,y              
        else: # in selection module
            elements=self.parent.backPanel.elements
            dists=[(elements[eleID].dist([y,x]),eleID) for eleID in elements]
            if len(dists)==0: 
                self.parent.statusBar().showMessage("") # clear state
                return
            dists=sorted(dists,key=lambda x:x[0])
            # print dists
            if dists[0][0]>10.0: # not selecting anything
                self.parent.selected=False
                self.parent.statusBar().showMessage("")
            else:
                self.parent.setSelected(dists[0][1])
                self.parent.selected=True

    def mouseReleaseEvent(self,event):
        """mouse released"""
        x=event.pos().x()
        y=event.pos().y()
        x,y=self.parent._pointUnderPresentShape([x,y])
        if self.recordPosition==True:
            self.parent.selected=False
            if self.inDrawLine==True:
                self.secondPoint=[x,y]
                self.inDrawLine=False
                self.recordPosition=False
                # print "Line:", self.firstPoint, "To", self.secondPoint
                self.parent.drawLine(self.firstPoint,self.secondPoint)
            elif self.inDrawEllipse==True:
                self.secondPoint=[x,y]
                self.inDrawEllipse=False
                self.recordPosition=False
                # print "Ellipse:", self.firstPoint, self.secondPoint
                self.parent.drawEllipse(self.firstPoint,self.secondPoint)
            elif self.inTranslation==True:
                self.secondPoint=[x,y]
                # print self.firstPoint
                # print self.secondPoint
                dx=self.firstPoint[0]-self.secondPoint[0]
                dy=self.firstPoint[1]-self.secondPoint[1]
                # print "\033[32mTranslation: %d.%d\033[0m" % (dx,dy)
                self.parent.translate(dx,dy)
            elif self.inClipLine==True:
                self.secondPoint=[x,y]
                # print "Second point:", self.secondPoint
                self.parent.clip(self.firstPoint[0],self.firstPoint[1],x,y)
        elif self.setDegree==True:
            if self.firstPointSet==False:
                return
            # print "Seconds point set at", [x,y]
            vec1=np.array([self.firstPoint[0]-self.parent.center[0],
                self.firstPoint[1]-self.parent.center[1]])
            vec2=np.array([x-self.parent.center[0],y-self.parent.center[1]])
            # print vec1, vec2
            if sum(vec1*vec1)==0 or sum(vec2*vec2)==0:
                self.parent.statusBar().showMessage("Invalid rotation")
                self.firstPoint=False
                return
            arcDegree=np.arccos(sum(vec1*vec2)/np.sqrt(sum(vec1*vec1)*sum(vec2*vec2)))
            if vec1[0]*vec2[1]-vec1[1]*vec2[0]<0:
                arcDegree=-arcDegree
            self.parent.degree=arcDegree*180/np.pi
            # print "Rotation degree:", self.parent.degree
            # print "center:", self.parent.center
            # print x,y,self.firstPoint
            self.parent.degreeSet=True
            self.setDegree=False
            self.firstPointSet=False
            self.parent.operationInterface()
        elif self.setScale==True:
            if self.firstPointSet==False:
                return
            vec1=np.array([self.firstPoint[0]-self.parent.center[0],
                self.firstPoint[1]-self.parent.center[1]])
            vec2=np.array([x-self.parent.center[0],y-self.parent.center[1]])
            ratio=np.sum(vec2*vec2)/np.sum(vec1*vec1)
            self.parent.scaleRatio=ratio
            self.parent.scaleSet=True
            self.setScale=False
            self.firstPointSet=False
            self.parent.operationInterface()
