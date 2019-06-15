#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QLabel, QColorDialog
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QSlider, QLineEdit, QSpinBox
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLCDNumber, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QErrorMessage, QInputDialog
from PyQt5.QtGui import QFont, QPixmap, QImage, QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QSize, pyqtSignal
from panel import *
from displayLabel import DisplayLabel

class CanvasSizeWidget(QWidget):
    """return the size of a new canvas"""
    beforeCloseSignal=pyqtSignal(int)
    def __init__(self,parent=None):
        super(CanvasSizeWidget,self).__init__(parent,Qt.Dialog)
        self.parent=parent
        self.setGeometry(300,300,200,100)
        self.setWindowTitle("New Canvas")
        
        self.widthLabel=QLabel(self)
        self.widthLabel.setText("Canvas Width")
        self.heightLabel=QLabel(self)
        self.heightLabel.setText("Canvas Height")
        self.widthSlide=QSpinBox(self)
        self.widthSlide.setMinimum(100)
        self.widthSlide.setMaximum(1000)
        self.widthSlide.setSingleStep(100)
        self.heightSlide=QSpinBox(self)
        self.heightSlide.setMinimum(100)
        self.heightSlide.setMaximum(1000)
        self.heightSlide.setSingleStep(100)       
        self.yesButton=QPushButton(self)
        self.yesButton.setText("Yes(&Y)")
        self.noButton=QPushButton(self)
        self.noButton.setText("No(&N)")

        self.width=100
        self.height=100
        self.yesClicked=False
        self.noClicked=False

        layout=QFormLayout()
        layout.addRow(self.widthLabel,self.widthSlide)
        layout.addRow(self.heightLabel,self.heightSlide)
        layout.addRow(self.yesButton,self.noButton)
        self.setLayout(layout)

        self.yesButton.clicked.connect(self._onYesClicked)
        self.noButton.clicked.connect(self._onNoClicked)

        self.show()

    def _onYesClicked(self):
        """return the width and height obtained"""
        self.width=self.widthSlide.value()
        self.height=self.heightSlide.value()
        self.yesClicked=True
        self.close()
    
    def _onNoClicked(self):
        """close dialog directly"""
        self.noClicked=True
        self.close()

    def closeEvent(self,event):
        state=self.yesClicked
        self.parent.setCanvasReturn(self.width, self.height, state)

class PanelWindow(QMainWindow):
    """Panel class for interaction"""
    def __init__(self):
        super(PanelWindow,self).__init__()
        self.backPanel=Panel()
        self.backPanel.resetCanvas(400,300)
        self._addActions()
        self.initUI()
        self.show()

    def setCanvasReturn(self,width,height,state):
        """trial"""
        if state==True: # need to reset canvas
            w,h=self.backPanel.canvas.shape[:2]
            self.mainCentralWidget.resize(width,height)
            if width>w or height>h:
                self.resize(width,height)
            self.backPanel.resetCanvas(width,height)
            self.mainCanvas.setPixmap(self._getPic())
            # self.mainCanvas.setPixmap(QPixmap())
            # self.mainCanvas.setPixmap(self._getPic())

    def _addActions(self):
        """add actions for Menu"""
        mainToolBar=self.addToolBar('Main tool bar')
        startMenu=self.menuBar().addMenu("Start(&S)")
        newCanvasAction=startMenu.addAction(QIcon("images/filenew.png"),"New canvas(&N)")
        newCanvasAction.triggered.connect(self._setCanvasSize)

        refreshAction=startMenu.addAction(QIcon("images/gtk-refresh.png"),"Refresh(&R)")
        refreshAction.triggered.connect(self._refreshCanvas)

        exitAction=startMenu.addAction(QIcon("images/exit.png"),"Exit(&E)")
        mainToolBar.addAction(exitAction)
        exitAction.triggered.connect(QCoreApplication.instance().quit)

        saveAction=startMenu.addAction(QIcon("images/filesave.png"),"Save(&S)")
        mainToolBar.addAction(saveAction)
        saveAction.triggered.connect(self._saveCanvas)

        elementMenu=self.menuBar().addMenu("Draw elements(&D)")
        
        setColorAction=elementMenu.addAction(QIcon("images/stock_media-play.png"),"Set color(&C)")
        mainToolBar.addAction(setColorAction)
        setColorAction.triggered.connect(self.getNewColor)

        lineAction=elementMenu.addAction(QIcon("images/chart_line.png"),"Line(&L)")
        mainToolBar.addAction(lineAction)
        lineAction.triggered.connect(self._drawLineTriggered)

        ellipseAction=elementMenu.addAction(QIcon("images/stock_media-rec.png"),"Ellipse(&E)")
        mainToolBar.addAction(ellipseAction)
        ellipseAction.triggered.connect(self._drawEllipseTriggered)

        polygonAction=elementMenu.addAction(QIcon("images/format-text-direction-ltr.png"),"Polygon(&P)")
        mainToolBar.addAction(polygonAction)
        polygonAction.triggered.connect(self._drawPolygonTriggered)

        curveAction=elementMenu.addAction(QIcon("images/pencil.png"),"Curve(&C)")
        mainToolBar.addAction(curveAction)
        curveAction.triggered.connect(self._drawCurveTriggered)

        operationsMenu=self.menuBar().addMenu("Operations(&C)")
        
        clipAction=operationsMenu.addAction(QIcon("images/edit-cut.png"),"Clip(&C)")
        mainToolBar.addAction(clipAction)
        clipAction.triggered.connect(self._clipTriggered)

        rotateAction=operationsMenu.addAction(QIcon("images/gtk-jump-to-ltr.png"),"Rotate(&R)")
        mainToolBar.addAction(rotateAction)
        rotateAction.triggered.connect(self._rotateTriggered)

        translateAction=operationsMenu.addAction(QIcon("images/gtk-go-forward-ltr.png"),"Translate(&T)")
        mainToolBar.addAction(translateAction)
        translateAction.triggered.connect(self._translateTriggered)

        scaleAction=operationsMenu.addAction(QIcon("images/gtk-zoom-in.png"),"Scale(&S)")
        mainToolBar.addAction(scaleAction)
        scaleAction.triggered.connect(self._scaleTriggered)

    def _setCanvasSize(self):
        """open a new widget to set the size of canvas"""
        sizeWidget=CanvasSizeWidget(self)
        sizeWidget.show()

    def _saveCanvas(self):
        """save canvas to a bmp file"""
        fileName, fileFormat=QFileDialog().getSaveFileName(self,"Save Image","untitled","bitmap(*.bmp)")
        if fileName!='': # do save
            print(fileName)
            # fileName=fileName.decode()
            if fileName[-4:]!='.bmp':
                fileName+='.bmp'
            pic=self.backPanel.getPic()
            cv.imwrite(fileName,pic)
            self.statusBar().showMessage(fileName+" saved.")

    def _refreshCanvas(self):
        """refresh canvas by reloading picture"""
        self.mainCanvas.setPixmap(self._getPic())

    def _getPic(self):
        """get picture from self.backPanel to area w*h"""
        pic=self.backPanel.getPic().copy()
        pic=cv.cvtColor(pic,cv.COLOR_BGR2RGB)
        height,width=pic.shape[:2]
        # print("Panel pic shape: %d*%d" % (height,width))
        QImg = QImage(pic.data, width, height, width*3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        return pixmap

    def _dumbPic(self,w,h):
        """get a dumb picture with size w*h*3"""
        pic=np.zeros((w,h,3),dtype=np.uint8)
        QImg=QImage(pic.data,h,w,h*3,QImage.Format_RGB888)
        return QPixmap.fromImage(QImg)

    def initUI(self):
        """initialize UI settings"""
        self.setWindowTitle("Lac Python Simple Painter v1.0")
        self.setWindowIcon(QIcon("trial.ico"))

        self.mainCanvas=DisplayLabel(self)
        self.mainCanvas.setScaledContents(True)
        # mainCanvas.setPixmap(self._getPic())

        self.mainLayout=QVBoxLayout()
        self.mainLayout.addWidget(self.mainCanvas)

        self.mainCentralWidget=QWidget()
        self.setCentralWidget(self.mainCentralWidget)
        self.centralWidget().setLayout(self.mainLayout)

        self.resize(400,300)
        self.moveCenter()

        # now load the picture
        w=self.mainCanvas.size().height()
        h=self.mainCanvas.size().width()
        self.mainCanvas.setPixmap(self._getPic())
        self.statusBar().showMessage("Welcome")

        self.idIndex=0
        self.idList=[]

        self.selectedAlgorithm="NONE"
        self._polygonPressed=False
        self._curvePressed=False
        self.selected=False
        self.centerSet=False
        self.center=[0.0,0.0]
        self.degreeSet=False
        self.degree=0.0
        self.scaleSet=False
        self.scaleRatio=1.0
        self.operationIndex=-1

    def moveCenter(self):
        """make the window to be located at the center of desktop"""
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _RGB(self,color):
        """return the color pacted in QColor"""
        return [color.red(),color.green(),color.blue()]

    def getNewColor(self):
        """get a new color for the canvas"""
        colorDialog=QColorDialog(self)
        color=colorDialog.getColor()
        # print "Set color", self._RGB(color)
        self.color=self._RGB(color)
        self.backPanel.setColor(self.color[0],self.color[1],self.color[2])

    def closeEvent(self,event):
        """deal with close window event"""
        reply=QMessageBox.question(self,'Message','Are you sure to quit?',QMessageBox.Yes|QMessageBox.No,
            QMessageBox.No)
       
        if reply==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def _drawLineTriggered(self):
        """start drawing a line"""
        self.statusBar().showMessage("Drawing line ...")
        self.mainCanvas.startDrawLine()

    def _drawEllipseTriggered(self):
        """start drawing an ellipse"""
        self.statusBar().showMessage("Drawing ellipse ...")
        self.mainCanvas.startDrawEllipse()

    def _drawPolygonTriggered(self):
        """start drawing a polygon"""
        if self._polygonPressed==False:
            self._polygonPressed=True
            self.statusBar().showMessage("Drawing polygon ...")
            self.mainCanvas.startDrawPolygon()
        else:
            self._polygonPressed=False
            self.mainCanvas.endDrawPolygon()
            self.statusBar().showMessage("Finished")

    def _drawCurveTriggered(self):
        """start drawing a curve"""
        if self.selectedAlgorithm=='NONE':
            method, state=QInputDialog.getItem(self,"Curve style","Please select the style of the curve",
                ["B-spline","Bezier"])
            if state==False:
                return
            self.selectedAlgorithm=method
        if self._curvePressed==False:
            self._curvePressed=True
            self.statusBar().showMessage("Drawing curve ...")
            self.mainCanvas.startDrawCurve()
        else:
            self._curvePressed=False
            self.mainCanvas.endDrawCurve()
            self.statusBar().showMessage("Finished")

    def operationInterface(self):
        """go back to doing operations"""
        if self.operationIndex==0:
            self._rotateTriggered()
        elif self.operationIndex==1:
            self._translateTriggered()
        elif self.operationIndex==2:
            self._scaleTriggered()

    def _translateTriggered(self):
        """translate an element"""
        self.operationIndex=1
        if self.selected==False:
            errorHint=QErrorMessage(self)
            errorHint.setWindowTitle("Translation Hint")
            errorHint.showMessage("Nothing selected! Please specify a graph element to translate.")
            return
        self.statusBar().showMessage("Translating ...")
        self.mainCanvas.startTranslation()

    def _clipTriggered(self):
        """clip an element, and if the element selected is not a line, the element is deleted"""
        self.operationIndex=2
        if self.selected==False:
            errorHint=QErrorMessage(self)
            errorHint.setWindowTitle("Clip Hint")
            errorHint.showMessage("Nothing selected! Please specify a graph element to clip.")
            return
        element=self.backPanel.elements[self.selectedID]
        if type(element)!=Line:
            self.backPanel.deleteElement(self.selectedID)
            self.mainCanvas.setPixmap(self._getPic())
            self.statusBar().showMessage("Element deleted")
        else:
            self.statusBar().showMessage("Clipping the line ...")
            self.mainCanvas.startClipLine()   
    
    def _scaleTriggered(self):
        """scale an element"""
        self.operationIndex=2
        if self.selected==False:
            errorHint=QErrorMessage(self)
            errorHint.setWindowTitle("Scaling Hint")
            errorHint.showMessage("Nothing selected! Please specify a graph element to scale.")
            return
        if self.centerSet==False:
            self.statusBar().showMessage("Please specify the center of scaling")
            self.mainCanvas.setCenter=True
        elif self.scaleSet==False:
            self.statusBar().showMessage("Please move your mouse to specify the degree of scaling")
            self.mainCanvas.setScale=True
        else:
            # print "Scaling center:", self.center
            # print "Scaling ratio:", self.scaleRatio
            w,h=self.backPanel.canvas.shape[:2]
            state=self.backPanel.scale(self.selectedID,self.center[0],w-1-self.center[1],self.scaleRatio)
            if state==True:
                self.mainCanvas.setPixmap(self._getPic())
                self.statusBar().showMessage("Scaling finished.")
            else:
                self.statusBar().showMessage("Scaling failed.")
            self.centerSet=self.scaleSet=False # end operation

    def _rotateTriggered(self):
        """rotate an element"""
        self.operationIndex=0
        if self.selected==False:
            errorHint=QErrorMessage(self)
            errorHint.setWindowTitle("Rotation Hint")
            errorHint.showMessage("Nothing selected! Please specify a graph element to rotate.")
            return
        if self.centerSet==False:
            self.statusBar().showMessage("Please specify the center of rotation")
            self.mainCanvas.setCenter=True
        elif self.degreeSet==False:
            self.statusBar().showMessage("Pleases move your mouse to specify the degree of rotation")
            self.mainCanvas.setDegree=True
        else:
            # print "Rotation center:", self.center
            # print "Rotation degree:", self.degree
            w,h=self.backPanel.canvas.shape[:2]
            # print "Transformed rotation center:", self.center[0], w-1-self.center[1]
            state=self.backPanel.rotate(self.selectedID,self.center[0],w-1-self.center[1],self.degree)
            if state==True:
                self.mainCanvas.setPixmap(self._getPic())
                self.statusBar().showMessage("Rotation finished.")
            else:
                self.statusBar().showMessage("Rotation failed.")
            self.centerSet=self.degreeSet=False # end operation
    
    def translate(self,dx,dy):
        """translate the selected graph element"""
        state=self.backPanel.translate(self.selectedID,-dx,dy)
        if state==True:
            self.mainCanvas.setPixmap(self._getPic())
            self.statusBar().showMessage("Translation finished.")
        else:
            self.statusBar().showMessage("Translation failed.")
        self.mainCanvas.endTranslation()

    def clip(self,x1,y1,x2,y2):
        """clip the line selected using the window defined by x1,y1,x2,y2"""
        w,h=self.backPanel.canvas.shape[:2]
        self.backPanel.clip(self.selectedID,x1,w-1-y1,x2,w-1-y2,"Liang-Barsky")
        self.mainCanvas.setPixmap(self._getPic())
        self.statusBar().showMessage("Clip done.")
        self.mainCanvas.endClipLine()

    def resizeEvent(self,event):
        """deal with resize event"""
        event.accept()

    def keyPressEvent(self,e):
        """deal with key pressing event"""
        if e.key()==Qt.Key_Escape:
            self.close()
        elif e.key()==Qt.Key_Plus:
            self.resize(400,400)

    def _whUnderPresentShape(self):
        """return w and h under present shape"""
        h=self.mainCanvas.size().width()
        w=self.mainCanvas.size().height()
        return w,h

    def _pointUnderPresentShape(self,p):
        """return point coordinate under present shape"""
        w1,h1=self.backPanel.canvas.shape[:2]
        w2,h2=self._whUnderPresentShape()
        return [float(p[0]*h1)/h2,float(p[1]*w1)/w2]

    def drawLine(self,p1,p2):
        """interface to draw a line from p1 to p2"""
        w,h=self.backPanel.canvas.shape[:2]
        self.backPanel.drawLine(self.idIndex,p1[0],w-1-p1[1],p2[0],w-1-p2[1],'Bresenham')
        self.mainCanvas.setPixmap(self._getPic())
        self.idList.append(self.idIndex)
        self.idIndex+=1
        self.statusBar().showMessage("Finished.")

    def setSelected(self,eleID):
        """interface to set a selected instance for other usage"""
        element=self.backPanel.elements[eleID]
        if type(element) is Line:
            self.statusBar().showMessage("Line selected")
        elif type(element) is Polygon:
            self.statusBar().showMessage("Polygon selected")
        elif type(element) is Ellipse:
            self.statusBar().showMessage("Ellipse selected")
        elif type(element) is Curve:
            self.statusBar().showMessage("Curve selected")
        else:
            assert(0)
        self.selectedElement=element
        self.selectedID=eleID

    def drawEllipse(self,p1,p2):
        """interface to draw an ellipse in range [p1,p2]"""
        w,h=self.backPanel.canvas.shape[:2]
        centerX=(p1[0]+p2[0])/2.0
        rx=max(p1[0],p2[0])-centerX
        centerY=w-1-(p1[1]+p2[1])/2.0
        ry=max(w-1-p1[1],w-1-p2[1])-centerY
        if rx<1.0 or ry<1.0:
            # print "Too small the distance, cannot draw!"
            self.statusBar().showMessage("Aborted.")
            return
        self.backPanel.drawEllipse(self.idIndex,centerX,centerY,rx,ry)
        self.mainCanvas.setPixmap(self._getPic())
        self.idList.append(self.idIndex)
        self.idIndex+=1
        self.statusBar().showMessage("Finished.")

    def drawPolygon(self,points):
        """interface to draw a polygon with points"""
        w,h=self.backPanel.canvas.shape[:2]
        points=[[p[0],w-1-p[1]] for p in points]
        self.backPanel.drawPolygon(self.idIndex,points,"Bresenham")
        self.mainCanvas.setPixmap(self._getPic())
        self.idList.append(self.idIndex)
        self.idIndex+=1

    def drawCurve(self,points):
        """interface to draw a curve"""
        w,h=self.backPanel.canvas.shape[:2]
        points=[[p[0],w-1-p[1]] for p in points]
        self.backPanel.drawCurve(self.idIndex,points,self.selectedAlgorithm)
        self.mainCanvas.setPixmap(self._getPic())
        self.idList.append(self.idIndex)
        self.idIndex+=1
        self.selectedAlgorithm='NONE'

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=PanelWindow()
    # canvas=CanvasSizeWidget()
    sys.exit(app.exec_())