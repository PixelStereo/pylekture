#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Event Class
An Event is always in a project and it may be in one or several scenario.
Event is the baseclass for Scenario and Project.
It inherits from Node, and add some attributes as wait, post_wait, loop and autoplay.
It adds a few methods too as play(), getduration() and getparent()

"""

from threading import Thread
from pylekture.node import Node
from pylekture.ramp import Ramp
from pylekture.errors import LektureTypeError


class Event(Node):
    """
    Create an Event
    an Event is like a step of a Scenario.
    It could be a delay, a goto value, a random process,
    a loop process or everything you can imagine
    An event is an address, a value, and optionally an animation
    """
    def __init__(self,*args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.name = 'Untitled Event'
        self.description = "I'm an event"
        self._is_template = None
        self.wait = 0
        self.post_wait = 0
        self._loop = False
        self._autoplay = False
        self._parent = None
        self._parameter = None
        self.value = None
        self.animation = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        s = "Event (name={name}, parent={parent}, description={description}, \
             duration={duration}, tags={tags}, autoplay={autoplay}, loop={loop}"
        return s.format(name=self.name,
                        description=self.description,
                        duration=self.getduration(),
                        tags=self.tags,
                        autoplay=self.autoplay,
                        loop=self.loop)

    @property
    def is_template(self):
        return self._is_template
    @is_template.setter
    def is_template(self, state):
        self._is_template = state


    @property
    def wait(self):
        """
        Wait time in seconds
        """
        return self._wait
    @wait.setter
    def wait(self, wait):
        if isinstance(wait, int) or isinstance(wait, float):
            self._wait = wait
            return True

    @property
    def post_wait(self):
        """
        Time to wait after all events played and before the end of this scenario
        unit:
        seconds
        """
        return self._post_wait
    @post_wait.setter
    def post_wait(self, post_wait):
        if isinstance(post_wait, int) or isinstance(post_wait, float):
            self._post_wait = post_wait
            return True

    @property
    def autoplay(self):
        """
        The autplay attribute. If true, the project plays when finish loading from hard drive
            :arg: Boolean
        """
        return self._autoplay
    @autoplay.setter
    def autoplay(self, autoplay):
        self._autoplay = autoplay

    @property
    def loop(self):
        """
        The loop attribute. If true, the loop plays again when it reach its end.
            :arg: Boolean
        """
        return self._loop
    @loop.setter
    def loop(self, loop):
        self._loop = loop

    def getparent(self):
        """
        Who is your parent bro?
        """
        # determine if it is in a scenario or not
        for scenario in self.parent.scenarios:
            if self in scenario.events:
                return scenario
        # it is not in a scenario, so it has no parent. Return False
        return None

    def getduration(self):
        """
        Computed duration of the event
        Read-Only

        :returns: Duration of the item
        :rtype: integer
        """
        duration = 0
        duration += self.wait
        duration += self.post_wait
        classname = self.__class__.__name__
        if classname == 'Wait':
            duration += self.command
        else:
            if self.command:
                try:
                    if 'ramp' in self.command:
                        index = self.command.index('ramp')
                        duration += float(self.command[index + 1])
                except Exception:
                    pass
        return duration

    def play(self, parameter=None):
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
    def __init__(self, parent, **kwargs):
        super(Player, self).__init__()
        self.parent = parent
        self.kwargs = kwargs
        #self.player = self.parent.Play(self.parent, self.kwargs)
        print( "thread init")
        self.start()

    def run(self):
        player = self.parent.Play(self.parent, self.kwargs)
        if player:
            player.join()

    def stop(self):
        self._stop.set()
