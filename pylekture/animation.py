#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Player for animation as ramp or random
"""

import datetime
from time import sleep
from pylekture.event import Event
from pylekture.constants import debug
from PySide6.QtCore import Signal, QThread, Slot
from time import time
current_milli_time = lambda: time() * 1000


class Animation(Event, QThread):
    """
    The Animation Object
    an animation is the base class for any animation
    it emit several signals
    - started
    - new_val
    it has several attributes
    - destination
    - duration
    - grain
    """
    new_val = Signal(int)
    timing = Signal(int)
    def __init__(self, kwargs):
        super(Animation, self).__init__()
        self.parameter = None
        self.destination = 1
        self.duration = 1000
        self.grain = 10
        self.origin = 0
        self.started.connect(self.print_start)
        self.finished.connect(self.print_finished)
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

    @Slot()
    def print_start(self):
        if debug >= 3:
            dbg = 'event-start: {name} at {time}'
            print(dbg.format(name=self.name, time=datetime.datetime.now()))

    @Slot()
    def print_finished(self):
        if debug >= 3:
            dbg = 'event-finished: {name} at {time}'
            print(dbg.format(name=self.name, time=datetime.datetime.now()))

    def play(self):
        """
        Play an event
        It creates a new object play in a separate thread.
        """
        self.start()
        return self

    def stop(self):
        """
        Stop an event
        It will destruct the player in the separate thread.
        """
        self._stop()

    def run(self):
        """
        the thread runner
        """
        start = current_milli_time()
        last = start
        for val, timing in self.animation:
            while (current_milli_time() - start) < timing:
                pass # wait
            self.timing.emit(timing)
            self.parameter.value = val
            self.new_val.emit(val)
