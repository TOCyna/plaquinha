#!/usr/bin/python3
from __future__ import unicode_literals
# -*- coding: utf-8 -*-

import sys, glob, serial
from PyQt5.QtWidgets import (QWidget, QLabel, 
    QComboBox, QApplication)

class Interface(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):      
        # ports = Interface.scan()
        # # self.lbl = QLabel("Select COM", self)
        # # combo = QComboBox(self)
        # # for next in ports:
        # #     combo.addItem(next)
        # # combo.move(10, 10)
        # # self.lbl.move(10, 150)
        # # combo.activated[str].connect(self.onActivated)
         
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Motor Controller')
        self.show()

    def onActivated(self, text):
        ser = serial.Serial(text, 9600)
        if not ser.isOpen():
            ser.open()
        self.lbl.setText(str(ser.isOpen()))
        self.lbl.adjustSize()


    def scan():
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
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    interface = Interface()
    sys.exit(app.exec_())




