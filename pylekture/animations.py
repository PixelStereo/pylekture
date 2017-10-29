#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Animation's library
"""

import datetime
from threading import Timer, Thread, current_thread
from pylekture.constants import debug
from pylekture.functions import checkType
from time import sleep
from time import time

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
        yield origin


class Ramp(object):
    """
    The Ramp Object
    a ramp is an interpolation with time as input and a function as output
    it has
    - origin (value)
    - destination (value)
    - duration (milliseconds)
    - grain (milliseconds)
    """
    def __init__(self, origin=0, destination=1, duration=1000, grain=10, loop=False):
        super(Ramp, self).__init__()
        self.origin = origin
        self.destination = destination
        self.duration = duration
        self.grain = grain
        self.loop = loop

    def __repr__(self):
        s = "Ramp (origin={origin}, destination={destination}, duration={duration}, grain={grain}, loop={loop}"
        return s.format(origin=self.origin,
                        destination=self.destination,
                        duration=self.duration,
                        grain=self.grain,
                        loop=self.loop)

    @property
    def is_template(self):
        return self._is_template
    @is_template.setter
    def is_template(self, state):
        self._is_template = m_bool(state)


    @property
    def loop(self):
        """
        The loop attribute. If true, the loop plays again when it reach its end.
            :arg: Boolean
        """
        return self._loop
    @loop.setter
    def loop(self, loop):
        loop = checkType(loop)
        if loop == 0:
            loop = False
        elif loop > 0:
            loop = True
        self._loop = loop


    def play(self, output=None):
        """
        Play an event
        It creates a new object play in a separate thread.
        """
        self.current_player = Player(self)
        return self.current_player

    def stop(self):
        """
        Stop an event
        It will destruct the player in the separate thread.
        """
        #print(self.current_player)
        print("stop is not yet implemented")


class Player(Thread):
    """
    A Player that play things
    """
    def __init__(self, ramp):
        super(Player, self).__init__()
        self.ramp = ramp
        print( "thread init")
        self.start()

    def run(self):
        player = self.Play(self.ramp)
        if player:
            player.join()

    def stop(self):
        self._stop.set()


    class Play(Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, ramp):
            Thread.__init__(self)
            self.ramp = ramp
            self.start()

        def run(self):
            print('---  ' + str(current_thread().name) + ' at ' + str(datetime.datetime.now()))
            ramper = ramp_generator(self.ramp.origin, self.ramp.destination, self.ramp.duration, self.ramp.grain)
            for val in ramper:
                print('---  ' + str(round(val, 2)))
            print('---  ' + str(current_thread().name) + ' at ' + str(datetime.datetime.now()))
