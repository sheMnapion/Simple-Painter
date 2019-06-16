import numpy as np
import cv2 as cv
# import matplotlib.pyplot as plt

class Ellipse(object):
    def __init__(self,id,x,y,rx,ry,color):
        """store the basical information of an ellipse"""
        self.id=id
        self.centerX=x
        self.centerY=y
        self.a=rx
        self.b=ry
        self.color=color
        self.points=[]

    def _standardDraw(self,pic,actuallyDraw=False):
        """try to draw supposing that rx>ry"""
        xStart=int(np.round(self.centerX))
        yStart=int(np.round(self.centerY+self.b))
        a=self.a
        b=self.b
        xEnd=int(xStart+float(a*a)/np.sqrt(a*a+b*b))
        p=b*b+(a*a/4.0)-a*a*b
        # print(p)
        if actuallyDraw==True:
            pic[xStart][yStart]=self.color
        y=yStart
        # print('XStart: %d YStart: %d' % (xStart, yStart))
        # print("Truly drawing: %d" % (actuallyDraw))
        points=[(xStart,yStart)] # record the drawn points
        for x in range(xStart+1,xEnd+1):
            # print "P value now: %.3f" % p
            if p<0:
                if actuallyDraw==True:
                    pic[x][y]=self.color
                points.append([x,y])
                p=p+3*b*b+2*b*b*int(x-xStart)
            else:
                y-=1
                if actuallyDraw==True:
                    pic[x][y]=self.color
                points.append([x,y])
                p=p+3*b*b+2*b*b*int(x-xStart)+2*a*a-2*a*a*(y-self.centerY+1)
        # plt.imshow(pic); plt.show()
        assert(x==xEnd)
        # print("Now at (%d.%d)" % (x,y))
        p=b*b*(x-self.centerX+0.5)**2+a*a*(y-self.centerY)**2-a*a*b*b     
        yEnd=int(self.centerY)
        yStart=y-1
        # print("YRange now: (%d->%d)" % (yStart,yEnd))
        # print('P at pivot: %.3f' % p)
        for y in range(yStart,yEnd-1,-1):
            # print('P at y %d: %.3f' % (y,p))
            if p<0:
                x+=1
                if actuallyDraw==True: 
                    pic[x][y]=self.color
                points.append([x,y])
                p=p+3*a*a-2*a*a*(y-self.centerY)+2*b*b+2*b*b*(x-self.centerX-1)
            else:
                if actuallyDraw==True: 
                    pic[x][y]=self.color
                points.append([x,y])
                p=p+3*a*a-2*a*a*(y-self.centerY+1)
        # plt.imshow(pic); plt.show()
        return points

    def draw(self,pic):
        """draw the ellipse on pic"""
        # By solving the boundary equation, we have x=a**2/sqrt(a**2+b**2)
        # print "Drawing an ellipse"  
        self.points=[]      
        if self.a>self.b:
            # first go from x axis
            points=self._standardDraw(pic,actuallyDraw=True)
        else:
            # change x and y axis to enable standard drawing process
            self.a, self.b=(self.b,self.a)
            points=self._standardDraw(pic,actuallyDraw=False)
            points=[(self.centerX+p[1]-self.centerY,self.centerY+p[0]-self.centerX) for p in points]
            for p in points:
                x=int(p[0])
                y=int(p[1])
                pic[x][y]=self.color
            self.a, self.b=(self.b,self.a)
        self.points=[p for p in points]
        self._duplicate(pic,points)

    def _duplicate(self,pic,points):
        """duplicate what has been drawn in first dimension to other dimensions"""
        for p in points:
            rx=p[0]-self.centerX
            ry=p[1]-self.centerY
            x1=int(np.round(self.centerX-rx))
            x2=int(np.round(self.centerX+rx))
            y1=int(np.round(self.centerY-ry))
            y2=int(np.round(self.centerY+ry))
            pic[x1][y2]=self.color
            pic[x1][y1]=self.color
            pic[x2][y1]=self.color
            self.points.extend([[x1,y2],[x1,y1],[x2,y1]])

    def translate(self,dx,dy,w,h):
        """translate the ellipse on a given panel"""
        newCenterX=self.centerX+dx
        newCenterY=self.centerY+dy
        # print newCenterX, newCenterY
        # print w,h
        if newCenterX<0 or newCenterX+self.a>=h or newCenterY<0 or newCenterY+self.b>=w:
            print("Out of bound after translating!")
            return False
        self.centerX=newCenterX
        self.centerY=newCenterY
        return True
    
    def rotate(self,x,y,r,w,h):
        """rotation of an ellipse, not supported now"""
        print("Cannot rotate an ellipse now!")
        return False
    
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

    def scale(self,x,y,s,w,h):
        """scaling of an ellipse"""
        # print "JUDGING HERE"
        relaX=self.centerX-x
        relaY=self.centerY-y
        homoPoint=np.array([relaX,relaY,1.0]).reshape(3,1)
        homoTrans=np.zeros((3,3))
        homoTrans[2][2]=1.0
        homoTrans[0][0]=homoTrans[1][1]=s
        transPoint=np.dot(homoTrans,homoPoint)
        transPoint[0]+=x
        transPoint[1]+=y
        if transPoint[0]<0 or transPoint[0]>=h or transPoint[1]<0 or transPoint[1]>=w:
            print("Scaling out of bound!")
            return False
        beforeX,beforeY=self.centerX,self.centerY
        self.centerX=transPoint[0][0]
        self.centerY=transPoint[1][0]
        # print transPoint
        if self.centerX+self.a*s>=w or self.centerX-self.a*s<0:
            print("Scaling x-axis out of bound!")
            self.centerX,self.centerY=beforeX,beforeY
            return False          
        if self.centerY+self.b*s>=h or self.centerY-self.b*s<0:
            print("Scaling y-axis out of bound!")
            self.centerX,self.centerY=beforeX,beforeY
            return False            
        self.a*=s
        self.b*=s
        return True