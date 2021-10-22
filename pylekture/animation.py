#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player for animation as ramp or random
"""

import threading
import datetime
from time import sleep
from pylekture.event import Event
from pylekture.constants import debug

from PySide6.QtCore import Signal


class Player(threading.Thread):
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
            self.parent.current_player

    def stop(self):
        self._stop()
        self.parent.current_player = None

class Animation(Event):
    """
    The Animation Object
    an animation is the base class for any animation
    it emit several signals
    - started
    - new_val
    - ended
    it has several attributes
    - destination
    - duration
    - grain
    """
    started = Signal(int)
    new_val = Signal(int)
    print('creating a signal')
    timing = Signal(int)
    ended = Signal(int)
    def __init__(self, kwargs):
        super(Animation, self).__init__()
        self.parameter = None
        self.destination = 1
        self.duration = 1000
        self.grain = 10
        self.origin = 0
        self.current_player = None
        for key, value in kwargs.items():
            setattr(self, key, value)

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
        """
        if self.current_player:
            self.stop()
            self.play()
        else:
            self.current_player = Player(self)
            return self.current_player
        """
        self.current_player = Player(self)
        if debug >= 3:
            dbg = 'event-play: {name} in {thread} at {time}'
            print(dbg.format(name=self.name, thread=threading.current_thread().name, time=datetime.datetime.now()))
        return self.current_player

    def stop(self):
        """
        Stop an event
        It will destruct the player in the separate thread.
        """
        #print(self.current_player)
        print("stop is not yet implemented")
        sleep(1)
