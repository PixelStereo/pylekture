#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from time import sleep
from threading import Timer


import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.parameter import Parameter

def bogus():
    #print datetime.now()
    pass

def ramp(duration):
    steps = duration / 10
    start = 0
    value = 0
    end = 1
    delta = float(end) - float(start)
    step = delta / steps
    #print(delta)
    for i in xrange(int(steps)):
        # 200 fps
        value = float(value) + step
        timer = Timer(0.0092, bogus, ())
        timer.start()
        timer.join()
        yield float(value)

print datetime.now()
a_ramp = ramp(2000)
for value in a_ramp:
    print(value)
print datetime.now()
