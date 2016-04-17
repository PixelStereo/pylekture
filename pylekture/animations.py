#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Animation's library
"""

import datetime
import threading
from pylekture.constants import debug
from pylekture.functions import checkType
import liblo
from time import sleep

class Ramp(threading.Thread):
    """Instanciate a thread for Playing a ramp
    Allow to do several ramps in a same scenario"""
    def __init__(self, target, address, args):
        threading.Thread.__init__(self)
        self.args = args
        self.address = address
        self.target = target
        self.start()

    def run(self):
        if debug >= 3:
            print('ramp starts in ' + self.name + ' at ' + str(datetime.datetime.now()))
        index = self.args.index('ramp')
        ramp = self.args[index+1]
        dest = self.args[index-1]
        dest = checkType(dest)
        ramp = checkType(ramp)
        value = 0
        delta = dest - value
        delta = float(delta)
        step = delta / ramp
        for millisec in range(ramp):
            msg = liblo.Message(self.address)
            value += step
            sleep(0.00072)
            msg.add(value)
            liblo.send(self.target, msg)