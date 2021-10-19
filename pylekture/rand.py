#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Random Animation is a basic animation
"""

from threading import Thread
from time import time
from pylekture.event import Event
import random
from pylekture.animation import Animation
from pylekture.PySignal import ClassSignal

current_milli_time = lambda: time() * 1000

def random_generator(datatype=float, origin=0, destination=1, duration=1000, grain=10):
    """
    The Random Generator
    step every 10 ms (default)
    Allow to do several random in a same project / scenario / event
    :param target:
    """
    start = current_milli_time()
    last = start
    while (current_milli_time() < (start + duration)):
        while (current_milli_time() < last + grain):
            pass # wait
        last = current_milli_time()
        # uniform gives you a floating-point value
        if not origin:
            origin=0
        if datatype == 'float':
            frand = round(random.uniform(origin, destination), precision)
        elif datatype == 'int':
            frand = round(random.randrange(origin, destination), grain)
        else:
            print('error - random only works with float or int')
            return None
        timing = int(last-start)
        yield frand, timing


class Random(Animation):
    """
    The Random Object
    a random is a pseudo random generation
    it has
    - parameter (parameter.value)
    - destination (value)
    - duration (milliseconds)
    - grain (milliseconds)
    """
    def __init__(self, *args, **kwargs):
        super(Random, self).__init__(*args, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        s = "Random (parameter={parameter}, destination={destination}, duration={duration}, grain={grain}, wait={wait}, post_wait={post_wait})"
        return s.format(parameter=self.parameter,
                        destination=self.destination,
                        duration=self.duration,
                        grain=self.grain,
                        wait=self.wait,
                        post_wait=self.post_wait)


    class Play(Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, random):
            Thread.__init__(self)
            self.random = random
            self.start()

        def run(self):
            self.random.started.emit()
            randomer = random_generator(datatype=self.random.parameter.datatype, origin=self.random.parameter.value, destination=self.random.destination, duration=self.random.duration, grain=self.random.grain)
            for val, timing in randomer:
                self.random.parameter.value = val
                self.random.timing.emit(timing)
                self.random.new_val.emit(val)
            self.random.ended.emit()
