# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import serial
ser = serial.Serial('/dev/ttyUSB1', 9600)
ser.open()
ser.isOpen()
ser.write('1')
ser.inWaiting()
ser.read(455)
ser.read(ser.inWaiting())
r.close()