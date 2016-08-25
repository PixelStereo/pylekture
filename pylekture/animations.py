#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Animation's library
"""

import datetime
from threading import Timer
from pylekture.constants import debug
from pylekture.functions import checkType
import liblo
from time import sleep

def bogus():
    pass

def Ramp(start, destination, duration):
    """
    Instanciate a thread for Playing a ramp

    step every 10 ms

    Allow to do several ramps in a same project / scenario / event

    :param target:
    """
    steps = duration / 10
    delta = float(destination) - float(start)
    step = delta / steps
    value = start
    print(start)
    for i in xrange(int(steps)):
        # 200 fps
        value = float(value) + step
        timer = Timer(0.0095, bogus, ())
        timer.start()
        timer.join()
        yield float(value)
