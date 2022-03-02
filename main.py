from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication
from PyQt5.uic import loadUi
import cv2
from PIL import Image
import tools, time, act
import matplotlib.pyplot as plt
import time

class Widget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("assets/memoir.ui",self)
        self.setWindowTitle("Memoir")

        self.histogram.clicked.connect(self.Histogram)
        self.startTrans.clicked.connect(self.Transformations)
        self.startTrans_Diffusion.clicked.connect(self.Diffusion)
        self.transChoice.currentIndexChanged.connect(self.checkTransOption)
        self.transChoice_Diffusion.currentIndexChanged.connect(self.checkTransOption)
        self.RefreshImg.clicked.connect(self.showimage)
        self.openImg.clicked.connect(self.addimageToview)
        self.SaveImg.clicked.connect(self.save_Image)

    def Diffusion(self):
        tStart = time.time()
        valueDiff = self.transChoice_Diffusion.currentIndex()
        if valueDiff == 0: self.showimage()
        elif valueDiff == 1:
            cr,cg,cb,g = tools.checkNull(self.ciR.text()),tools.checkNull(self.ciG.text()),tools.checkNull(self.ciB.text()),tools.checkNull(self.diffG.text())
            newImg, name = act.FridDeffusion(cv2.cvtColor(cv2.imread(self.imagename), cv2.COLOR_BGR2RGB), int(cr),int(cg),int(cb),int(g))
            self.savedImg = tools.SaveImage(newImg, name)
            self.showimageResult('Images/Saved/'+name+'.png')
        elif valueDiff == 2:
            cr,cg,cb,g = tools.checkNull(self.ciR.text()),tools.checkNull(self.ciG.text()),tools.checkNull(self.ciB.text()),tools.checkNull(self.diffG.text())
            newImg, name = act.FridDecrypt(cv2.cvtColor(cv2.imread(self.imagename), cv2.COLOR_BGR2RGB), int(cr),int(cg),int(cb),int(g))
            self.savedImg = tools.SaveImage(newImg, name)
            self.showimageResult('Images/Saved/'+name+'.png')
        elif valueDiff == 3:
            cr,cg,cb,g = tools.checkNull(self.ciR.text()),tools.checkNull(self.ciG.text()),tools.checkNull(self.ciB.text()),tools.checkNull(self.diffG.text())
            newImg, name,self.chenXi = act.chenDiffusion(cv2.cvtColor(cv2.imread(self.imagename), cv2.COLOR_BGR2RGB), int(cr),int(cg),int(cb))
            self.savedImg = tools.SaveImage(newImg, name)
            self.showimageResult('Images/Saved/'+name+'.png')
        elif valueDiff == 4:
            cr,cg,cb,g = tools.checkNull(self.ciR.text()),tools.checkNull(self.ciG.text()),tools.checkNull(self.ciB.text()),tools.checkNull(self.diffG.text())
            newImg, name = act.chenDecrypt(cv2.cvtColor(cv2.imread(self.imagename), cv2.COLOR_BGR2RGB), int(cr),int(cg),int(cb),self.chenXi)
            self.savedImg = tools.SaveImage(newImg, name)
            self.showimageResult('Images/Saved/'+name+'.png')
        print("Diffusion time: ",round(time.time() - tStart,3))

    def Transformations(self):
        tStart = time.time()
        ValueTrans = self.transChoice.currentIndex()
        if ValueTrans == 0: self.showimage()
        elif ValueTrans == 1:
            factor = tools.checkNull(self.Times.text())
            newImg, name = act.BackedMap(self.pixel, int(factor), ValueTrans)
            #newImg, name = act.stretchImage(self.pixel,int(factor))
            self.savedImg = tools.SaveImage(newImg, name)
            self.showimageResult('Images/Saved/'+name+'.png')
        elif ValueTrans == 2:
            a,b = tools.checkNull(self.Cata.text()),tools.checkNull(self.Catb.text())
            newImg, name = act.catMap(cv2.cvtColor(cv2.imread(self.imagename), cv2.COLOR_BGR2RGB), int(a),  int(b))
            self.savedImg = tools.SaveImage(newImg, name)
            self.showimageResult('Images/Saved/'+name+'.png')
        print("Substitution time: ",round(time.time() - tStart,3))

    def checkTransOption(self):
        ValueTran = self.transChoice.currentIndex()
        valueDiff = self.transChoice_Diffusion.currentIndex()
        if valueDiff == 0 :
            self.ciR.setEnabled(False), self.ciR.setText('')
            self.ciG.setEnabled(False), self.ciG.setText('')
            self.ciB.setEnabled(False), self.ciB.setText('')
            self.diffG.setEnabled(False), self.diffG.setText('')
        elif valueDiff == 1 or valueDiff == 2:
            self.ciR.setEnabled(True), self.ciR.setText('')
            self.ciG.setEnabled(True), self.ciG.setText('')
            self.ciB.setEnabled(True), self.ciB.setText('')
            self.diffG.setEnabled(True), self.diffG.setText('')
        elif valueDiff == 3 or valueDiff == 4:
            self.ciR.setEnabled(True), self.ciR.setText('')
            self.ciG.setEnabled(True), self.ciG.setText('')
            self.ciB.setEnabled(True), self.ciB.setText('')
            self.diffG.setEnabled(False), self.diffG.setText('')
        
        if ValueTran == 0:
            self.Times.setEnabled(False), self.Times.setText('')
            self.Cata.setEnabled(False), self.Cata.setText('')
            self.Catb.setEnabled(False), self.Catb.setText('')
        if ValueTran == 1:
            self.Times.setEnabled(True), self.Times.setText('')
            self.Cata.setEnabled(False), self.Cata.setText('')
            self.Catb.setEnabled(False), self.Catb.setText('')
        if ValueTran == 2:
            self.Cata.setEnabled(True), self.Cata.setText('')
            self.Catb.setEnabled(True), self.Catb.setText('')
            self.Times.setEnabled(False), self.Times.setText('')

    def Histogram(self):

        imageFile = QFileDialog.getOpenFileName(None, "Open image", "./Images", "Image Files (*.png *.jpg *.bmp *.jpeg *.png *.jfif)")
        image1= str(imageFile[0])
        imageFile = QFileDialog.getOpenFileName(None, "Open image", "./Images", "Image Files (*.png *.jpg *.bmp *.jpeg *.png *.jfif)")
        image2= str(imageFile[0])
        histIm1, histIm2 = act.Hist_RGB(tools.getImage(image1)), act.Hist_RGB(tools.getImage(image2))
        fig = plt.figure(figsize=(15, 8))
        ax1 = fig.add_subplot(121)
        plt.title("image 1")
        ax2 = fig.add_subplot(122)
        plt.title("image 2")
        if len(histIm1) == 3:
            ax1.plot(histIm1[0], color = 'red'), ax1.plot(histIm1[1], color = 'green'), ax1.plot(histIm1[2], color = 'blue')
            ax2.plot(histIm2[0], color = 'red'), ax2.plot(histIm2[1], color = 'green'), ax2.plot(histIm2[2], color = 'blue')
        else:
            ax1.plot(histIm1)
            ax2.plot(histIm2)
        plt.show()

    def showimage(self):
        self.codeImg.setPixmap(QtGui.QPixmap(self.imagename))  

    def showimageResult(self, imgNameCode):
        self.codeImg.setPixmap(QtGui.QPixmap(imgNameCode))

    def addimageToview(self):
        try:
            imageFile = QFileDialog.getOpenFileName(None, "Open image", "./Images", "Image Files (*.png *.jpg *.bmp *.jpeg *.png *.jfif)")
            self.imagename= str(imageFile[0])
            self.showimage()
            self.pixel = tools.getImage(self.imagename)
        except: pass    
        
    def save_Image(self):
        try:
            self.imagename = self.savedImg
            self.pixel = tools.getImage(self.imagename)
        except: pass
        
if __name__ == '__main__':
    app = QApplication([])
    window = Widget()
    window.show()
    app.exec_()