# This file implements the line class
import numpy as np
import cv2 as cv

class Line(object):
    def __init__(self,id,startPoint,endPoint,algorithm,color):
        """store the basical information of a line object"""
        self.id=id
        self.startPoint=startPoint
        self.endPoint=endPoint
        self.algorithm=algorithm
        self.color=color
    
    def _DDADraw(self,pic):
        """draw a line using DDA algorithm"""
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        # print "DDA: (%d.%d)->(%d.%d)" % (x1,y1,x2,y2)
        if x1==x2: # vertical to x axis
            x=int(round(x1))
            yStart=min(y1,y2); yEnd=max(y1,y2)
            for y in range(int(round(yStart)),int(round(yEnd))):
                pic[x][y]=self.color
        elif y1==y2: # parallel to x axis
            y=int(round(y1))
            xStart=min(x1,x2); xEnd=max(x1,x2)
            for x in range(int(round(xStart)),int(round(xEnd))):
                pic[x][y]=self.color
        else:
            m=float(y2-y1)/(x2-x1)
            # print "M:", m
            if np.abs(m)>1.0: # grow by y
                # print "Grow by y"
                yStart=min(y1,y2)
                yEnd=max(y1,y2)
                xStart=x1
                if yStart==y2: xStart=x2
                for i,y in enumerate(range(int(round(yStart)),int(round(yEnd)))):
                    xPoz=xStart+(1.0/m)*i
                    pic[int(round(xPoz))][y]=self.color
            else:
                xStart=min(x1,x2)
                xEnd=max(x1,x2)
                yStart=y1
                if xStart==x2: yStart=y2
                for i,x in enumerate(range(int(round(xStart)),int(round(xEnd)))):
                    yPoz=yStart+m*i
                    pic[x][int(round(yPoz))]=self.color  

    def _BrensenhamDraw(self,pic):
        """draw the line using Brasenham algorithm"""
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        if x1==x2: # vertical to x axis
            x=int(round(x1))
            yStart=int(round(min(y1,y2)))
            yEnd=int(round(max(y1,y2)))
            pic[x][yStart:yEnd+1]=self.color
        elif y1==y2: # parallel to x axis
            y=int(round(y1))
            xStart=int(round(min(x1,x2)))
            xEnd=int(round(max(x1,x2)))
            pic[xStart:xEnd+1][y]=self.color
        else: 
            x1=int(round(x1)); x2=int(round(x2))
            y1=int(round(y1)); y2=int(round(y2))
            if y1>y2:
                x1,x2=x2,x1
                y1,y2=y2,y1 
            # now y2 > y1
            print "(%d,%d) -> (%d,%d)" % (x1,y1,x2,y2)
            deltaX=x2-x1; deltaY=y2-y1
            m=float(y2-y1)/(x2-x1)
            print "M:",m, "delta x:",deltaX,"delta y:",deltaY
            deltaX=np.abs(deltaX)
            deltaY=np.abs(deltaY)
            if np.abs(m)<1.0: # grow by x
                print "Grow by x"
                p=2*deltaY-deltaX
                yPointer=y1
                if x1<x2:
                    xPositions=range(x1,x2+1)
                else:
                    xPositions=range(x1,x2-1,-1)
                for x in xPositions:
                    if p<0:
                        pic[x][yPointer]=self.color
                        p+=2*deltaY
                    else:
                        yPointer+=1
                        if yPointer>y2:
                            break
                        pic[x][yPointer]=self.color
                        p+=2*deltaY-2*deltaX
            else: # grow by y
                print "Grow by y"
                yPositions=range(y1,y2+1)
                xPointer=x1
                p=2*deltaX-deltaY
                for y in yPositions:
                    if p<0:
                        pic[xPointer][y]=self.color
                        p+=2*deltaX
                    else:
                        if x1>x2:
                            xPointer-=1
                            if xPointer<x2:
                                break
                        else:
                            xPointer+=1
                            if xPointer>x2:
                                break
                        pic[xPointer][y]=self.color
                        p+=2*deltaX-2*deltaY
                
    def _libDraw(self,pic):
        """using cv library to draw a line"""
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        x1=int(np.round(x1)); x2=int(np.round(x2))
        y1=int(np.round(y1)); y2=int(np.round(y2))
        cv.line(pic,(y1,x1),(y2,x2),self.color)

    def draw(self,pic):
        """draw itself on pic"""
        if self.algorithm=='DDA':
            self._DDADraw(pic)
        elif self.algorithm=='Bresenham':
            self._BrensenhamDraw(pic)
        else:
            self._libDraw(pic)