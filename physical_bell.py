import serial
import sys
import time

s = serial.Serial("/dev/ttyUSB0")
s.break_condition = False

def physical_ring():
    s.break_condition = True

def physical_kill():
    s.break_condition = False
