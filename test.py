#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In the example, we draw randomly 1000 red points 
on the window.

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys, random
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.setGeometry(600, 600, 600, 600)
        self.setWindowTitle('Points')
        self.show()
        

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
        
    def drawPoints(self, qp):
      
        pen = QPen()
        pen.setWidth(1)
        pen.setBrush(Qt.red)
        pen.setCapStyle(Qt.RoundCap)
        qp.setPen(pen)
        size = self.size()
        size = 5
        r = 100
        r2 = r ** 2
        for x in range(0, r*2):
            x = x - r
            y = (r2 - x ** 2) ** (0.5) + 0.5
            qp.drawPoint(150+x, 150+y)
            qp.drawPoint(150+x, 150-y)

    def drawPoint2():
        pass
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

    # public void circleSimple(int xCenter, int yCenter, int radius, Color c)
    # {
    #     int pix = c.getRGB();
    #     int x, y, r2;
        
    #     r2 = radius * radius;
    #     for (x = -radius; x <= radius; x++) {
    #         y = (int) (Math.sqrt(r2 - x*x) + 0.5);
    #         raster.setPixel(pix, xCenter + x, yCenter + y);
    #         raster.setPixel(pix, xCenter + x, yCenter - y);
    #     }
    # }