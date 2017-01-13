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
from time import time

current_milli_time = lambda: time() * 1000

def bogus():
    pass

def Ramp(origin, destination, duration=1000, grain=10):
    """
    Instanciate a thread for Playing a ramp

    step every 10 ms

    Allow to do several ramps in a same project / scenario / event

    :param target:
    """
    start = current_milli_time()
    last = start
    step = float( (destination - origin) / ( float(duration / grain) ))


    while (current_milli_time() < (start + duration)):
        while (current_milli_time() < last + grain):
            pass # wait
        last = current_milli_time()
        origin += step
        print(origin)
    yield float(origin)
