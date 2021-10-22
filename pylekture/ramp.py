#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ramp Animation is a basic animation
"""

from threading import Thread
from time import time
from pylekture.animation import Animation
from pylekture.event import Event

current_milli_time = lambda: time() * 1000


def ramp_generator(origin=0, destination=1, duration=1000, grain=10):
    """
    The Ramp Generator
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
        timing = int(last-start)
        yield origin, timing

class Ramp(Animation):
    """
    The Ramp Object
    a ramp is an interpolation with time as input and a function as output
    it has
    - origin (value)
    - destination (value)
    - duration (milliseconds)
    - grain (milliseconds)
    """
    def __init__(self, *args, **kwargs):
        super(Ramp, self).__init__(*args, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        s = "Ramp (parameter={parameter}, origin={origin}, destination={destination}, duration={duration}, grain={grain}), wait={wait}, post_wait={post_wait})"
        return s.format(parameter=self.parameter,
                        origin=self.origin,
                        destination=self.destination,
                        duration=self.duration,
                        grain=self.grain,
                        wait=self.wait,
                        post_wait=self.post_wait)


    def run(self):
        self.start()
        self.started.emit(1)
        ramper = ramp_generator(self.ramp.origin, self.ramp.destination, self.ramp.duration, self.ramp.grain)
        for val, timing in randomer:
            self.parameter.value = val
            self.timing.emit(timing)
            self.new_val.emit(val)
        self.ended.emit(1)
