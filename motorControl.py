#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys, glob, serial, re
from PyQt5.QtWidgets import (QWidget, QLabel, 
    QComboBox, QApplication, QPushButton)
from PyQt5.QtCore import (Qt, pyqtSignal, QObject, QSize, QPoint, 
    QTime, QTimer)
from PyQt5.QtGui import QColor, QPainter, QPolygon
from random import randint

class Communication(QObject):
    """docstring for Communication"""
    serial = serial.Serial()
    def __init__(self, baud):
        super().__init__()
        self.baud = baud

    def getPorts(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    
    def connect(self,text):
        port = text
        self.serial = serial.Serial(port, self.baud)
        if not self.serial.isOpen():
            self.serial.open()
            self.serial.flushInput()
        

    def randomAngle():
        return randint(0,360)

    def read(self):
        text = ''
        if self.serial.isOpen():
            if self.serial.inWaiting() > 0:
                text = self.serial.read(self.serial.inWaiting())
                print(text)
        return text

class MotorControl(QObject):
    """docstring for MotorControl"""
    def __init__(self):
        super().__init__()
        
        self.com = Communication(9600)
        ports = self.com.getPorts()
        
        app = QApplication(sys.argv)
        
        self.interface = Interface(ports)
        self.interface.selectedPort[str].connect(self.com.connect)
        self.interface.refresh.connect(self.refreshPorts)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.read)
        self.timer.start(1000)

        sys.exit(app.exec_())

    def refreshPorts(self):
        ports = self.com.getPorts()
        print (ports)
        self.interface.setPorts(ports)

    def read(self):
        angle = self.com.read()
        if angle:
            s = angle.decode().strip('\n\r')
            print ("decode",s)
            re.findall('OK', s)
            print ("re",s)
            s = s.split('\n')
            print ("split",s)
            if s != '' and s != ' ':
                for next in s:
                    print(next)
                    if next != '':
                        next = int(next)
                        self.interface.setAngle(next)
        self.timer.start(1000)

class Interface(QWidget):
    ports = []
    selectedPort = pyqtSignal(str)
    refresh = pyqtSignal()
    def __init__(self, ports):
        super().__init__()
        self.ports = ports
        self.initUI()

    def initUI(self):      
        self.lbl = QLabel("Select COM", self)
        self.lbl.move(10, 150)
        
        self.combo = QComboBox(self)
        self.combo.move(10, 10)
        self.combo.activated[str].connect(self.onActivated)
        
        refresh = QPushButton('Refresh', self)
        refresh.move(10, 40)
        refresh.clicked.connect(self.refreshClicked)
        
        self.positionGraph = AnalogPosition()
        self.positionGraph.show()

        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Motor Controller')

        self.combo.addItem("Connect/Refresh")
        self.show()
        self.addPorts()

    def refreshClicked(self):
        self.refresh.emit()

    def onActivated(self, text):
        self.selectedPort.emit(text)
        # ser = serial.Serial(text, 9600)
        # if not ser.isOpen():
        #     ser.open()
        # self.lbl.setText(str(ser.isOpen()))
        # self.lbl.adjustSize()
    
    def addPorts(self):
        # self.removeWidget(combo)
        # self.combo.deleteLater()
        # self.combo = QComboBox(self)
        self.combo.clear()
        for next in self.ports:
            self.combo.addItem(next)
    
    def setPorts(self, ports):
        self.ports = ports
        self.addPorts()

    def setAngle(self, angle):
        self.positionGraph.setAngle(angle)

class AnalogPosition(QWidget):

    positionHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -70)
    ])

    positionHandColor = QColor(0, 127, 127, 191)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Position")
        self.resize(300, 300)
        self.angle = 0.1

    def mousePressEvent(self, event):
        self.angle = AnalogPosition.randomAngle()
        print(event.pos(), "Angle: ", self.angle)
        self.update()
    
    def paintEvent(self, event):
        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogPosition.positionHandColor)

        painter.save()
        painter.rotate(self.angle)

        painter.drawConvexPolygon(AnalogPosition.positionHand)
        painter.restore()

        painter.setPen(AnalogPosition.positionHandColor)

        for j in range(32):
            painter.drawLine(92, 0, 96, 0)
            painter.rotate(11.25)

    def setAngle(self, angle):
        self.angle = angle
        self.update()

    def randomAngle():
        return randint(0,360)

if __name__ == '__main__':
    
    motorControl = MotorControl()
    




