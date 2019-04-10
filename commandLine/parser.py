#!/bin/usr/env python

# This file implements operations on parsing the input

class Parser(object):
    """Parser class"""
    operations=["resetCanvas","saveCanvas","setColor","drawLine","drawPolygon",
        "drawEllipse","drawCurve","translate","rotate","clip"]
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
        print "%s needs %d parameters, %d given" % (funcName,funcNeedNum,funcGetNum)

    def paraNotInRangeErrorDisplay(self,paraName,lowerBound,upperBound,getValue):
        """Print error information for not in range parameter"""
        print "Invalid parameter! %s should be within [%.2f,%.2f], %.2f given" % (paraName, \
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

    def drawPolygonSecondLineAnalysis(self,lexicals):
        """Analyze the second line for drawing polygon
            need to have waitPara points in total
            return (state,points)
        """
        if len(lexicals)!=self.waitPara*2:
            self.paraErrorDisplay("Get polygon points",self.waitPara*2,len(lexicals)-1)
            return (False,None)
        try:
            points=[float(l) for l in lexicals]
        except ValueError as e:
            print e
            return (False,None)
        px=[p for i,p in enumerate(points) if i%2==0]
        py=[p for i,p in enumerate(points) if i%2==1]
        return (True,zip(px,py))

    def analyzeLine(self,userLine):
        """Analyze user input
            and return the draw information
        """
        if userLine=='':
            return
        lexicals=userLine.strip('\n').split(' ')
        print "Leximes:",lexicals
        if lexicals[0] not in self.operations:
            print "Invalid input! Operation keywords are:"
            for kop in self.operations:
                print kop,
            print
            return
        if self.waitSecondLine is False:
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
        else:
            if self.waitFor=="polygon":
                state,points=self.drawPolygonSecondLineAnalysis(lexicals)
                if state is True:
                    print "Accepted!"
                    self.clearWaitState()