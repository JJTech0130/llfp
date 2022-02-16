import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor
import llfp


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 LEAP Controller'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.bridge1 = llfp.Bridge("192.168.0.5")
        print(self.bridge1.login("jjtech", "jjtech0130")) #Replace with your username/password.
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        zone1 = QPushButton('Zone 1', self)
        zone1.setToolTip('Lamp above computer')
        zone1.move(10,10)
        zone1.clicked.connect(self.zone1_clicked)
        zone2 = QPushButton('Zone 2', self)
        zone2.setToolTip('Living Room lamps')
        zone2.move(10,50)
        zone2.clicked.connect(self.zone2_clicked)
        self.show()

    @pyqtSlot()
    def zone1_clicked(self):
        lamp = llfp.Zone(6164, self.bridge1)
        color = QColorDialog.getColor()
        if color.isValid():
            newvalue = (color.value()*100)/255
            newsat = (color.saturation()*100)/255
            print(lamp.goToColorFull(100,newvalue,color.hue(),newsat))
    def zone2_clicked(self):
        lamp = llfp.Zone(1719, self.bridge1)
        color = QColorDialog.getColor()
        if color.isValid():
            newvalue = (color.value()*100)/255
            newsat = (color.saturation()*100)/255
            print(lamp.goToColorFull(100,newvalue,color.hue(),newsat))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
