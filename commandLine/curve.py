import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

class Curve(object):
    """Curve class, support drawing curve using Bezier and B-spline"""
    def __init__(self,color,id,n,points,algorithm):
        """store the basical information of an ellipse"""
        # print "New curve: %d" % id
        self.id=id
        self.n=n
        self.points=points
        self.algorithm=algorithm
        self.color=color
        self.drawnPoints=[]
        self.parameterArea=np.linspace(0,1,num=n+3+1)
        # print self.parameterArea

    def _uVec(self,n,u):
        ret=np.zeros(n)
        for i in range(n):
            ret[i]=u**(n-1-i)
        return ret

    def B_i_k(self,i,k,u):
        """calculate B(i,k) using Cox-deBoor recursion equation"""
        # assert(i>=0 and i<=self.n)
        assert(k>=1)
        if k==1:
            if u>=self.parameterArea[i] and u<self.parameterArea[i+1]:
                return 1.0
            else:
                return 0.0
        assert(k>1)
        l1=self.parameterArea[i+k-1]-self.parameterArea[i]
        l2=self.parameterArea[i+k]-self.parameterArea[i+1]
        if u==self.parameterArea[i]:
            l1=1.0 # 0/0=0
            # print "special set 1"
        if u==self.parameterArea[i+k]:
            l2=1.0
            # print "special set 2"
        term1=(u-self.parameterArea[i])*self.B_i_k(i,k-1,u)/l1
        term2=(self.parameterArea[i+k]-u)*self.B_i_k(i+1,k-1,u)/l2
        # print "----------------------------------"
        # print u,l1,l2
        # print "B_%d_%d(%.3f)=%.3f+%.3f=%.3f" % (i,k,u,term1,term2,term1+term2)
        # print "----------------------------------"
        return term1+term2

    def _bezierDraw(self,pic):
        """using Bezier curve to draw the curve"""
        n=self.n
        # n control points, n-1 order results
        pascalTriangle=np.zeros((n,n))
        pascalTriangle[0][0]=pascalTriangle[1][0]=pascalTriangle[1][1]=1
        for i in range(2,n):
            pascalTriangle[i][0]=pascalTriangle[i][i]=1.0
            for j in range(1,i):
                pascalTriangle[i][j]=pascalTriangle[i-1][j]+pascalTriangle[i-1][j-1]
        # print(pascalTriangle)    
        bezierMatrix=np.zeros((n,n))
        offset=n%2
        for i in range(n):
            for j in range(n-i):
                bezierMatrix[i][j]=pascalTriangle[n-1-i][j]*(-1)**(j+i+offset+1)
        for i in range(n):
            bezierMatrix[i]*=pascalTriangle[n-1][i]
        self.drawnPoints=[]
        u=0.0
        Px=np.array([p[0] for p in self.points]).reshape(-1,1)
        Py=np.array([p[1] for p in self.points]).reshape(-1,1)
        for u in np.arange(0,1,0.0005):
            uVec=self._uVec(n,u)
            tempX=np.dot(uVec,np.dot(bezierMatrix,Px))
            tempY=np.dot(uVec,np.dot(bezierMatrix,Py))
            # print(tempX,tempY)
            self.drawnPoints.append([tempX,tempY])
            pic[int(np.round(tempX))][int(np.round(tempY))]=self.color

    def _bSplineDraw(self,pic):
        """using B-spline to draw the curve"""
        u=0.0
        self.drawnPoints=[]
        Px=np.array([p[0] for p in self.points])
        Py=np.array([p[1] for p in self.points])
        # print np.arange(self.parameterArea[2],self.parameterArea[self.n],0.001)
        # exit(0)
        for u in np.arange(self.parameterArea[2],self.parameterArea[self.n],0.0005):
            tempX=0.0
            tempY=0.0
            # print u, self.id
            for j in range(self.n):
                temp=self.B_i_k(j,3,u)
                # print "B_%d_3(%.3f): %.3f" % (j,u,temp)
                tempX+=Px[j]*temp # draw 3-order curve
                tempY+=Py[j]*temp
            self.drawnPoints.append([tempX,tempY])
            pic[int(np.round(tempX))][int(np.round(tempY))]=self.color
                    
    def draw(self,pic):
        """draw interface, draw on a given picture"""
        if self.algorithm=="Bezier":
            self._bezierDraw(pic)
        elif self.algorithm=="B-spline":
            self._bSplineDraw(pic)
    
    def euclidDist(self,p1,p2):
        return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
        
    def dist(self,p):
        """calculate the distance of a point p to this curve
            need not to be too precise
        """
        if len(self.drawnPoints)==0:
            return 1e6
        dists=[self.euclidDist(p,point) for point in self.drawnPoints]
        return min(dists)

    def translate(self,dx,dy,w,h):
        """translate the curve on a given canvas with shape w*h"""
        newPoints=[]
        for point in self.points:
            x1=point[0]+dx
            y1=point[1]+dy
            if x1<0 or x1>=h or y1<0 or y1>=w:
                print("\033[31mOut of bound after translating! Please check the value\033[0m")
                return False
            newPoints.append((x1,y1))
        self.points=newPoints
        return True

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
            print("\033[31mScaling out of bound!\033[0m")
            return False, transPoint[0][0], transPoint[1][0]
        return True, transPoint[0][0], transPoint[1][0]

    def scale(self,x,y,s,w,h):
        """scale the curve according to s centered at (x,y) in canvas w*h"""
        newPoints=[]
        for point in self.points:
            x1=point[0]
            y1=point[1]
            state, xx1, yy1=self._scalePoint(x1,y1,x,y,s,w,h)
            if state==False:
                return False
            newPoints.append((xx1,yy1))
        self.points=newPoints
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
            print("\033[31mRotation out of bound!\033[0m")
            # print transPoint
            return False, transPoint[0][0], transPoint[1][0]
        return True, transPoint[0][0], transPoint[1][0]
    
    def rotate(self,x,y,r,w,h):
        """rotate the curve according to degree[r] centered at (x,y) in pic w*h"""
        newPoints=[]
        for point in self.points:
            x1=point[0]
            y1=point[1]
            state, x1, y1=self._rotatePoint(x1,y1,x,y,r,w,h)
            if state==False:
                return False
            newPoints.append((x1,y1))
        self.points=newPoints
        return True