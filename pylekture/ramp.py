#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ramp Animation is a basic animation
"""

from threading import Thread
from time import time
from pylekture.event import Event
from pylekture.PySignal import ClassSignal

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


class Ramp(Event):
    """
    The Ramp Object
    a ramp is an interpolation with time as input and a function as output
    it has
    - origin (value)
    - destination (value)
    - duration (milliseconds)
    - grain (milliseconds)
    """
    started = ClassSignal()
    new_val = ClassSignal()
    ended = ClassSignal()
    def __init__(self, kwargs):
        super(Ramp, self).__init__()
        self.parameter = None
        self.origin = 0
        self.destination = 1
        self.duration = 1000
        self.grain = 10
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

    @property
    def parameter(self):
        """
        Time to wait after all events played and before the end of this scenario
        unit:
        seconds
        """
        return self._parameter
    @parameter.setter
    def parameter(self, parameter):
        self._parameter = parameter
        return True

    def play(self):
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
            self.ramp.started.emit()
            #ramper = ramp_generator(self.ramp.parameter.value, self.ramp.destination, self.ramp.duration, self.ramp.grain)
            ramper = ramp_generator(self.ramp.origin, self.ramp.destination, self.ramp.duration, self.ramp.grain)
            for val in ramper:
                self.ramp.parameter.value = val
                self.ramp.new_val.emit(val)
            self.ramp.ended.emit()


class Player(Thread):
    """
    A Player that play things
    """
    def __init__(self, parent):
        super(Player, self).__init__()
        self.parent = parent
        self.start()

    def run(self):
        player = self.parent.Play(self.parent)
        if player:
            player.join()

    def stop(self):
        self._stop.set()
