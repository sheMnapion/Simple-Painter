#!/bin/usr/env python

# This file implements operations on parsing the input

class Parser(object):
    """Parser class"""
    operations=["resetCanvas","saveCanvas","setColor","drawLine","drawPolygon",
        "drawEllipse","drawCurve","translate","rotate","scale","clip"]
    waitSecondLine=False
    waitFor=-1
    waitPara=-1

    def __init__(self):
       self.clearWaitState() 
    
    def clearWaitState(self):
        """Initialize waiting 2 line state"""
        self.waitSecondLine=False
        self.waitFor=-1
        self.waitPara=-1

    def paraErrorDisplay(self,funcName,funcNeedNum,funcGetNum):
        """Print error information for parameter unmatch"""
        print "\033[31m%s needs %d parameters, %d given\033[0m" % (funcName,funcNeedNum,funcGetNum)

    def paraNotInRangeErrorDisplay(self,paraName,lowerBound,upperBound,getValue):
        """Print error information for not in range parameter"""
        print "\033[31mInvalid parameter! %s should be within [%.2f,%.2f], %.2f given\033[0m" % (paraName, \
            lowerBound, upperBound, getValue)

    def resetCanvasAnalysis(self,lexicals):
        """Analyze input for resetCanvas
            return (state,w,h)
        """
        if len(lexicals)!=3:
            self.paraErrorDisplay("resetCanvas",2,len(lexicals)-1)
            return (False,-1,-1)
        try:
            ints=[int(l) for l in lexicals[1:]]
        except ValueError as e:
            print e
            return (False,-1,-1)
        w,h=ints
        if w<100 or w>1000:
            self.paraNotInRangeErrorDisplay("w",100,1000,w)
            return (False,-1,-1)
        if h<100 or h>1000:
            self.paraNotInRangeErrorDisplay("h",100,1000,h)
            return (False,-1,-1)
        return (True,w,h)

    def saveCanvasAnalysis(self,lexicals):
        """Analyze input for saveCanvas
            return (state,fileName)
        """
        if len(lexicals)!=2:
            self.paraErrorDisplay("saveCanvas",1,len(lexicals)-1)
            return (False,None)
        return (True,lexicals[1])

    def setColorAnalysis(self,lexicals):
        """Analyze input for setColor
            return (state,R,G,B)
        """
        if len(lexicals)!=4:
            self.paraErrorDisplay("setColor",3,len(lexicals)-1)
            return (False,-1,-1,-1)
        try:
            ints=[int(l) for l in lexicals[1:]]
        except ValueError as e:
            print e
            return (False,-1,-1,-1)
        R,G,B=ints
        if R<0 or R>255:
            self.paraNotInRangeErrorDisplay("R",0,255,R)
            return (False,-1,-1,-1)
        if G<0 or G>255:
            self.paraNotInRangeErrorDisplay("G",0,255,G)
            return (False,-1,-1,-1)
        if B<0 or B>255:
            self.paraNotInRangeErrorDisplay("B",0,255,B)
            return (False,-1,-1,-1)
        return (True,R,G,B)

    def drawLineAnalysis(self,lexicals):
        """Analyze input for drawLine
            return (state,id,x1,y1,x2,y2,algorithm)
        """
        algorithms=["DDA","Bresenham","Naive"]
        if len(lexicals)!=7:
            self.paraErrorDisplay("drawLine",6,len(lexicals)-1)
            return (False,-1,-1,-1,-1,-1,-1)
        try:
            id=int(lexicals[1])
            x1,y1,x2,y2=[float(l) for l in lexicals[2:6]]
            algorithm=lexicals[6]
        except ValueError as e:
            print e
            return (False,-1,-1,-1,-1,-1,-1)
        if algorithm not in algorithms:
            print "Unknown algorithm! We only support:",
            for alg in algorithms:
                print alg,
            print
            return (False,-1,-1,-1,-1,-1,-1)
        return (True,id,x1,y1,x2,y2,algorithm)

    def drawPolygonFirstLineAnalysis(self,lexicals):
        """Analyze input for drawPolygon
            Since it takes two lines, the separation process is done 
            for two stages, and this deals with the first
            return (state,id,polyEdgeCount,algorithm)
        """
        algorithms=["DDA","Bresenham","Naive"]
        if len(lexicals)!=4:
            self.paraErrorDisplay("drawPolygon",3,len(lexicals)-1)
            return (False,-1,-1,-1)
        try:
            id=int(lexicals[1])
            polyEdgeCount=int(lexicals[2])
            algorithm=lexicals[3]
        except ValueError as e:
            print e
            return (False,-1,-1,-1)
        if algorithm not in algorithms:
            print "Unknown algorithm! We only support:",
            for alg in algorithms:
                print alg,
            print
            return (False,-1,-1,-1)
        return (True,id,polyEdgeCount,algorithm)

    def drawCurveFirstLineAnalysis(self,lexicals):
        """Analyze input for drawCurve
            Since it takes two lines, the separation process is done 
            for two stages, and this deals with the first
            return (state,id,controlPointCount,algorithm)
        """
        algorithms=["Bezier","B-spline"]
        if len(lexicals)!=4:
            self.paraErrorDisplay("drawCurve",3,len(lexicals)-1)
            return (False,-1,-1,-1)
        try:
            id=int(lexicals[1])
            controlPointCount=int(lexicals[2])
            algorithm=lexicals[3]
        except ValueError as e:
            print e
            return (False,-1,-1,-1)
        if algorithm not in algorithms:
            print "Unknown algorithm! We only support:",
            for alg in algorithms:
                print alg,
            print
            return (False,-1,-1,-1)
        return (True,id,controlPointCount,algorithm)

    def drawPolygonSecondLineAnalysis(self,lexicals):
        """Analyze the second line for drawing polygon
            need to have waitPara points in total
            return (state,points)
        """
        if len(lexicals)!=self.waitPara*2:
            self.paraErrorDisplay("Get polygon points",self.waitPara*2,len(lexicals))
            return (False,None)
        try:
            points=[float(l) for l in lexicals]
        except ValueError as e:
            print e
            return (False,None)
        px=[p for i,p in enumerate(points) if i%2==0]
        py=[p for i,p in enumerate(points) if i%2==1]
        return (True,zip(px,py))

    def drawCurveSecondLineAnalysis(self,lexicals):
        """Analyze the second line for drawing curve
            need to have waitPara points in total
            return (state,points)
        """
        if len(lexicals)!=self.waitPara*2:
            self.paraErrorDisplay("Get curve control points",self.waitPara*2,len(lexicals))
            return (False,None)
        try:
            points=[float(l) for l in lexicals]
        except ValueError as e:
            print e
            return (False,None)
        px=[p for i,p in enumerate(points) if i%2==0]
        py=[p for i,p in enumerate(points) if i%2==1]
        return (True,zip(px,py))

    def drawEllipseAnalysis(self,lexicals):
        """Anayze input for drawEllipse
            return state, id,x,y,rx,ry
        """
        if len(lexicals)!=6:
            self.paraErrorDisplay("drawEllipse",5,len(lexicals)-1)
            return (False,-1,-1,-1,-1,-1)
        try:
            id=int(lexicals[1])
            x=float(lexicals[2])
            y=float(lexicals[3])
            rx=float(lexicals[4])
            ry=float(lexicals[5])
        except ValueError as e:
            print e
            return (False,-1,-1,-1,-1,-1)
        return (True,id,x,y,rx,ry)

    def translateAnalysis(self,lexicals):
        """Analyze input for translate
            return (state,id,dx,dy)
        """
        if len(lexicals)!=4:
            self.paraErrorDisplay("translate",3,len(lexicals)-1)
            return (False,-1,-1,-1)
        try:
            id=int(lexicals[1])
            dx=float(lexicals[2])
            dy=float(lexicals[3])
        except ValueError as e:
            print e
            return (False,-1,-1,-1)
        return (True,id,dx,dy)

    def rotateAnalysis(self,lexicals):
        """Analyze input for rotate
            return (state,id,x,y,r)
        """
        if len(lexicals)!=5:
            self.paraErrorDisplay("rotate",4,len(lexicals)-1)
            return (False,-1,-1,-1,-1)
        try:
            id=int(lexicals[1])
            x=float(lexicals[2])
            y=float(lexicals[3])
            r=float(lexicals[4])
        except ValueError as e:
            print e
            return (False,-1,-1,-1,-1)
        return (True,id,x,y,r)

    def scaleAnalysis(self,lexicals):
        """Analyze input for rotate
            return (state,id,x,y,s)
        """
        if len(lexicals)!=5:
            self.paraErrorDisplay("scale",4,len(lexicals)-1)
            return (False,-1,-1,-1,-1)
        try:
            id=int(lexicals[1])
            x=float(lexicals[2])
            y=float(lexicals[3])
            s=float(lexicals[4])
        except ValueError as e:
            print e
            return (False,-1,-1,-1,-1)
        return (True,id,x,y,s)

    def clipAnalysis(self,lexicals):
        """Analyze input for clip
            return (state,id,x1,y1,x2,y2,algorithm)
        """
        algorithms=["Cohen-Sutherland","Liang-Barsky"]
        if len(lexicals)!=7:
            self.paraErrorDisplay("clip",6,len(lexicals)-1)
            return (False,-1,-1,-1,-1,-1,-1)
        try:
            id=int(lexicals[1])
            points=[float(l) for l in lexicals[2:6]]
            algorithm=lexicals[6]
        except ValueError as e:
            print e
            return (False,-1,-1,-1,-1,-1,-1)
        if algorithm not in algorithms:
            print "Unknown algorithm! We only support:",
            for alg in algorithms:
                print alg,
            print
            return (False,-1,-1,-1)
        x1,y1,x2,y2=points
        return (True,id,x1,y1,x2,y2,algorithm)

    def analyzeLine(self,userLine):
        """Analyze user input
            and return the draw information
        """
        if userLine=='':
            return
        lexicals=userLine.strip('\n').split(' ')
        # print "Leximes:",lexicals
        if self.waitSecondLine is False:
            if lexicals[0] not in self.operations:
                print "\033[32mInvalid input! Operation keywords are:"
                for kop in self.operations:
                    print kop,
                print "\033[0m"
                return
            if lexicals[0]=='resetCanvas':
                state,w,h=self.resetCanvasAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()            
            elif lexicals[0]=='saveCanvas':
                state, name=self.saveCanvasAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
            elif lexicals[0]=='setColor':
                state, R, G, B=self.setColorAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
            elif lexicals[0]=='drawLine':
                state, id, x1, y1, x2, y2, algorithm=self.drawLineAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
            elif lexicals[0]=='drawPolygon':
                state, id, edgeCount, algorithm=self.drawPolygonFirstLineAnalysis(lexicals)
                if state is True:
                    self.waitSecondLine=True
                    self.waitFor="polygon"
                    self.waitPara=edgeCount
            elif lexicals[0]=='drawCurve':
                state, id, pointCount, algorithm=self.drawCurveFirstLineAnalysis(lexicals)
                if state is True:
                    self.waitSecondLine=True
                    self.waitFor="curve"
                    self.waitPara=pointCount            
            elif lexicals[0]=='drawEllipse':
                state, id, x, y, rx, ry=self.drawEllipseAnalysis(lexicals)
                if state is True:
                    print "Accpeted!"
                    self.clearWaitState()
            elif lexicals[0]=='translate':
                state, id, dx, dy=self.translateAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
            elif lexicals[0]=='rotate':
                state, id, x, y, r=self.rotateAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
            elif lexicals[0]=='scale':
                state, id, x, y, s=self.scaleAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
            elif lexicals[0]=='clip':
                state, id, x1, y1, x2, y2, algorithm=self.clipAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
        else:
            if self.waitFor=="polygon":
                state,points=self.drawPolygonSecondLineAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()
            if self.waitFor=="curve":
                state,points=self.drawCurveSecondLineAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()           
            