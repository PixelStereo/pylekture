#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Random Animation is a basic animation
"""

from threading import Thread
from time import time
from pylekture.event import Event
import random
current_milli_time = lambda: time() * 1000

def random_generator(origin=0, destination=1, duration=1000, grain=10):
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
        frand = round(random.uniform(origin, destination), 6)
        yield frand


class Random(Event):
    """
    The Random Object
    a random is a pseudo random generation
    it has
    - parameter (parameter.value)
    - destination (value)
    - duration (milliseconds)
    - grain (milliseconds)
    """
    def __init__(self, kwargs):
        super(Random, self).__init__()
        self.parameter = None
        self.destination = 1
        self.duration = 1000
        self.grain = 10
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

    @property
    def parameter(self):
        """
        The parameter to control
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
        def __init__(self, random):
            Thread.__init__(self)
            self.random = random
            self.start()

        def run(self):
            randomer = random_generator(self.random.parameter.value, self.random.destination, self.random.duration, self.random.grain)
            for val in randomer:
                self.random.parameter.value = val


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

