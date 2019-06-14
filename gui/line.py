# This file implements the line class
import numpy as np
import cv2 as cv

class Line(object):
    def __init__(self,id,startPoint,endPoint,algorithm,color):
        """store the basical information of a line object"""
        self.id=id
        # print "\033[32mIniting line %d: [%d.%d] --> [%d.%d]\033[0m" % (id,startPoint[0],startPoint[1],
        #    endPoint[0],endPoint[1])
        self.startPoint=startPoint
        self.endPoint=endPoint
        self.algorithm=algorithm
        self.color=color
    
    def _DDADraw(self,pic):
        """draw a line using DDA algorithm"""
        # print(self.startPoint,self.endPoint)
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        # print(x1,y1,x2,y2)
        # print "DDA: (%d.%d)->(%d.%d)" % (x1,y1,x2,y2)
        if x1==x2: # vertical to x axis
            x=int(round(x1))
            yStart=min(y1,y2); yEnd=max(y1,y2)
            for y in range(int(round(yStart)),int(round(yEnd))):
                pic[x][y]=self.color
                self.points.append([x,y])
        elif y1==y2: # parallel to x axis
            y=int(round(y1))
            xStart=min(x1,x2); xEnd=max(x1,x2)
            for x in range(int(round(xStart)),int(round(xEnd))):
                pic[x][y]=self.color
                self.points.append([x,y])
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
                    self.points.append([int(round(xPoz)),y])
            else:
                # print(x1,x2)
                xStart=min(x1,x2)
                xEnd=max(x1,x2)
                yStart=y1
                # print(xStart,xEnd,yStart)
                if xStart==x2: yStart=y2
                for i,x in enumerate(range(int(round(xStart)),int(round(xEnd)))):
                    yPoz=yStart+m*i
                    # print(yPoz)
                    pic[x][int(round(yPoz))]=self.color 
                    self.points.append([x,int(round(yPoz))]) 

    def _BrensenhamDraw(self,pic):
        """draw the line using Brasenham algorithm"""
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        x1=int(round(x1)); x2=int(round(x2))
        y1=int(round(y1)); y2=int(round(y2))
        # print(x1,y1,x2,y2)
        # print(pic.shape)
        # print("--------------------------------------------")
        if x1==x2: # vertical to x axis
            # print "============================================"
            x=int(round(x1))
            yStart=int(round(min(y1,y2)))
            yEnd=int(round(max(y1,y2)))
            for i in range(yStart,yEnd+1):
                pic[x][i]=self.color
            self.points.extend([[x,y] for y in range(yStart,yEnd+1)])
        elif y1==y2: # parallel to x axis
            # print "||||||||||||||||||||||||||||||||||||||||||||||"
            y=int(round(y1))
            xStart=int(round(min(x1,x2)))
            xEnd=int(round(max(x1,x2)))
            for i in range(xStart,xEnd):
                pic[i][y]=self.color
            self.points.extend([[x,y] for x in range(xStart,xEnd+1)])
        else: 
            if y1>y2:
                x1,x2=x2,x1
                y1,y2=y2,y1 
            # now y2 > y1
            # print "(%d,%d) -> (%d,%d)" % (x1,y1,x2,y2)
            deltaX=x2-x1; deltaY=y2-y1
            m=float(y2-y1)/(x2-x1)
            # print "M:",m, "delta x:",deltaX,"delta y:",deltaY
            deltaX=np.abs(deltaX)
            deltaY=np.abs(deltaY)
            if np.abs(m)<1.0: # grow by x
                # print "Grow by x"
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
                    self.points.append([x,yPointer])
            else: # grow by y
                # print "Grow by y"
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
                    self.points.append([xPointer,y])
                
    def _libDraw(self,pic):
        """using cv library to draw a line"""
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        x1=int(np.round(x1)); x2=int(np.round(x2))
        y1=int(np.round(y1)); y2=int(np.round(y2))
        cv.line(pic,(y1,x1),(y2,x2),self.color)

    def translate(self,dx,dy,w,h):
        """translate the line on canvas with [picShape]"""
        x1=self.startPoint[0]; y1=self.startPoint[1]
        x2=self.endPoint[0]; y2=self.endPoint[1]
        newX1=x1+dx; newX2=x2+dx
        newY1=y1+dy; newY2=y2+dy
        # print x1,y1,x2,y2
        # print w,h
        # print newX1, newY1, newX2, newY2
        if newX1<0 or newX1>=h or newX2<0 or newX2>=h:
            print("Out of bound after translating! Please check the value for dx")
            return False
        if newY1<0 or newY1>=w or newY2<0 or newY2>=w:
            print("Out of bound after translating! Please check the value for dy")
            return False
        self.startPoint=(newX1,newY1)
        self.endPoint=(newX2,newY2)
        return True

    def _rotatePoint(self,x1,y1,x,y,r,w,h):
        """rotate a given point (x1,y1) with rotation specification"""
        relaX=x1-x
        relaY=y1-y
        homoPoint=np.array([relaX,relaY,1.0]).reshape(3,1)
        homoTrans=np.zeros((3,3))
        homoTrans[2][2]=1.0
        homoTrans[0][0]=homoTrans[1][1]=np.cos(r*np.pi/180.0)
        homoTrans[1][0]=np.sin(r*np.pi/180)
        homoTrans[0][1]=-homoTrans[1][0]
        transPoint=np.dot(homoTrans,homoPoint)
        transPoint[0]+=x
        transPoint[1]+=y
        if transPoint[0]<0 or transPoint[0]>=h or transPoint[1]<0 or transPoint[1]>=w:
            print("Rotation out of bound!")
            # print transPoint
            return False, (transPoint[0][0], transPoint[1][0])
        return True, (transPoint[0][0], transPoint[1][0])

    def _scalePoint(self,x1,y1,x,y,s,w,h):
        """scale a given point (x1,y1) with scale specification"""
        relaX=x1-x
        relaY=y1-y
        homoPoint=np.array([relaX,relaY,1.0]).reshape(3,1)
        homoTrans=np.zeros((3,3))
        homoTrans[2][2]=1.0
        homoTrans[0][0]=homoTrans[1][1]=s
        transPoint=np.dot(homoTrans,homoPoint)
        transPoint[0]+=x
        transPoint[1]+=y
        if transPoint[0]<0 or transPoint[0]>=h or transPoint[1]<0 or transPoint[1]>=w:
            # print "Point (%d.%d) from (%d.%d) with scale %.3f" % (x1,y1,x,y,s)
            # print homoTrans
            # print "Result:"
            # print transPoint
            # print "\033[31mScaling out of bound!\033[0m"
            return False, (transPoint[0][0], transPoint[1][0])
        return True, (transPoint[0][0], transPoint[1][0])

    def scale(self,x,y,s,w,h):
        """scale the line according to s centered at (x,y) in canvas w*h"""
        x1,y1=self.startPoint
        state, (xx1,yy1)=self._scalePoint(x1,y1,x,y,s,w,h)
        if state==False:
            print("Edge point",self.startPoint,"out of bound")
            return False
        x2, y2=self.endPoint
        state, (xx2,yy2)=self._scalePoint(x2,y2,x,y,s,w,h)
        if state==False:
            print("Edge point",self.endPoint,"out of bound")
            return False
        self.startPoint=(xx1,yy1)
        self.endPoint=(xx2,yy2)
        return True

    def rotate(self,x,y,r,w,h):
        """rotate the line according to degree[r] centered at (x,y) in pic w*h"""
        x1,y1=self.startPoint
        state, (xx1,yy1)=self._rotatePoint(x1,y1,x,y,r,w,h)
        if state==False:
            return False
        x2, y2=self.endPoint
        state, (xx2,yy2)=self._rotatePoint(x2,y2,x,y,r,w,h)
        if state==False:
            return False
        self.startPoint=(xx1,yy1)
        self.endPoint=(xx2,yy2)
        return True

    def draw(self,pic):
        """draw itself on pic"""
        self.points=[]
        if self.algorithm=='DDA':
            self._DDADraw(pic)
        elif self.algorithm=='Bresenham':
            self._BrensenhamDraw(pic)
        else:
            self._libDraw(pic)
    
    def euclidDist(self,p1,p2):
        return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
        
    def dist(self,p):
        """calculate the distance of a point p to this ellipse
            need not to be too precise
        """
        if len(self.points)==0:
            return 1e6
        dists=[self.euclidDist(p,point) for point in self.points]
        return min(dists)

    def _areaCode(self,x1,y1,x2,y2,x,y):
        """return the area code of a given point (x,y)"""
        ret=0
        ret+=int(x<x1)*1
        ret+=int(x>x2)*2
        ret+=int(y<y1)*4
        ret+=int(y>y2)*8
        return ret

    def _leftIntercept(self,xValue,yMin,yMax):
        """return the intercept point of line to the left side of window"""
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        assert(x1!=x2)
        k=(y1-y2)/(x1-x2)
        yValue=k*(xValue-x2)+y2
        return yValue

    def _rightIntercept(self,xValue,yMin,yMax):
        """return the intercept point of line to the right side of window"""
        return self._leftIntercept(xValue,yMin,yMax)

    def _upperIntercept(self,yValue,xMin,xMax):
        """return the intercept point of line to the upper side of window"""
        x1,y1=self.startPoint
        x2,y2=self.endPoint
        if x1==x2:
            return x1
        k=(y1-y2)/(x1-x2)
        xValue=(yValue-y2)/k+x2
        return xValue        

    def _lowerIntercept(self,yValue,xMin,xMax):
        """return the intercept point of line to the lower side of window"""
        return self._upperIntercept(yValue,xMin,xMax)

    def _liangBarskyClip(self,x1,y1,x2,y2):
        """use Liang-Barsky algorithm to clip
            return whether to preserve the line
        """
        x1,x2=(min(x1,x2),max(x1,x2))
        y1,y2=(min(y1,y2),max(y1,y2))
        lineX1,lineX2=self.startPoint[0],self.endPoint[0]
        lineY1,lineY2=self.startPoint[1],self.endPoint[1]
        while True:
            u1=0.0; u2=1.0
            # print 'Window is:',x1,y1,x2,y2
            # print 'Line endpoints are',lineX1,lineY1,lineX2,lineY2
            # print u1,u2
            deltaX=lineX2-lineX1
            deltaY=lineY2-lineY1
            p=[-deltaX,deltaX,-deltaY,deltaY]
            q=[lineX1-x1,x2-lineX1,lineY1-y1,y2-lineY1]
            # print p,q
            for i in range(4):
                if p[i]==0:
                    if q[i]<0: # out of bound
                        return False
                else:
                    if p[i]<0:
                        # print("Diminish,",q[i]/p[i])
                        u1=max(u1,q[i]/p[i])
                    else:
                        # print("Squinsh,",q[i]/p[i])
                        u2=min(u2,q[i]/p[i])
                    if u1>u2:
                        return False
                    # print "u1: %.3f u2: %.3f (i: %d)" % (u1,u2,i)
            lineX2=lineX1+deltaX*u2
            lineY2=lineY1+deltaY*u2
            lineX1=lineX1+deltaX*u1
            lineY1=lineY1+deltaY*u1
            if u1==0.0 and u2==1.0:
                break # no change
        self.startPoint=(lineX1,lineY1)
        self.endPoint=(lineX2,lineY2)
        return True

    def _cohenSutherlandClip(self,x1,y1,x2,y2,firstLayer=True):
        """use Cohen-Sutherland algorithm to clip"""
        x1,x2=(min(x1,x2),max(x1,x2))
        y1,y2=(min(y1,y2),max(y1,y2))
        areaCode1=self._areaCode(x1,y1,x2,y2,self.startPoint[0],self.startPoint[1])
        areaCode2=self._areaCode(x1,y1,x2,y2,self.endPoint[0],self.endPoint[1])
        if areaCode1|areaCode2==0: # fully in window
            return True
        if areaCode1&areaCode2>0: # fully outside, end of recursion
            return firstLayer
        if areaCode1==0 or areaCode2==0:
            preserve=True
        else:
            preserve=False
        if areaCode1&8 and not (areaCode2&8): # one beyond upper and one below
            xValue=self._upperIntercept(y2,x1,x2)
            self.startPoint=(xValue,y2)
        elif not (areaCode1&8) and areaCode2&8:
            xValue=self._upperIntercept(y2,x1,x2)
            self.endPoint=(xValue,y2)            
        elif areaCode1&4 and not (areaCode2&4):
            xValue=self._lowerIntercept(y1,x1,x2)
            self.startPoint=(xValue,y1)
        elif not (areaCode1&4) and areaCode2&4:
            xValue=self._lowerIntercept(y1,x1,x2)
            self.endPoint=(xValue,y1)
        elif areaCode1&2 and not(areaCode2&2):
            yValue=self._rightIntercept(x2,y1,y2)
            self.startPoint=(x2,yValue)
        elif not (areaCode1&2) and areaCode2&2:
            yValue=self._rightIntercept(x2,y1,y2)
            self.endPoint=(x2,yValue)
        elif areaCode1&1 and not (areaCode2&1):
            yValue=self._leftIntercept(x1,y1,y2)
            self.startPoint=(x1,yValue)
        else:
            yValue=self._leftIntercept(x1,y1,y2)
            self.endPoint=(x1,yValue)
        return self._cohenSutherlandClip(x1,y1,x2,y2,preserve)

    def clip(self,x1,y1,x2,y2,algorithm):
        """clip the line on [x1.y1]-->[x2.y2]"""
        if algorithm=='Cohen-Sutherland':
            return self._cohenSutherlandClip(x1,y1,x2,y2,firstLayer=False)
        elif algorithm=='Liang-Barsky':
            return self._liangBarskyClip(x1,y1,x2,y2)