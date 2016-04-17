#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Scenario Class
A scenario is always in a project and it (may) contains events
"""

import liblo
import datetime
import threading
from time import sleep
from pylekture.node import Node
from pylekture.constants import debug
from pylekture.functions import checkType
from pylekture.animations import Ramp


class Event(Node):
    """Create an Event
    an Event is like a step of a Scenario.
    It could be a delay, a goto value, a random process,
    a loop process or everything you can imagine """
    def __init__(self, scenario, command=None, output=None):
        super(Event, self).__init__()
        self._command = command
        self._output = output
        self.scenario = scenario

    @property
    def output(self):
        if self._output:
            return self._output
        else:
            return self.scenario.output
    @output.setter
    def output(self, output):
        self._output = output

    @property
    def command(self):
        return self._command
    @command.setter
    def command(self, command):
        self._command = command


class OSC(Event):
    """
    An OSC event is an Event designed to be outputed via OSC
    """
    def __init__(self, scenario, command, *args, **kwargs):
        super(OSC, self).__init__(scenario, command, *args, **kwargs)
        self.address = command[0]
        if len(command) > 1:
            self.args = command[:1]
            self.protocol = 'OSC'

    class Play(threading.Thread):
        """docstring for PlayOsc"""
        def __init__(self, event):
            threading.Thread.__init__(self)
            self.output = event.output
            self.command = event.command
            self.event = event
            self.start()

        def run(self):
            """play an OSC event"""
            if debug:
                print('event-play: ' + self.event.name + ' in ' + str(threading.current_thread().name) + ' at ' + str(datetime.datetime.now()))
            out = self.output
            args = self.command
            if isinstance(args, list):
                # address is the first item of the list
                address = args[0]
                args = args[1:]
            else:
                # this is a adress_only without arguments
                address = args
                args = None
            try:
                target = liblo.Address(out.ip, int(out.udp))
                if debug:
                    print('connect to : ' + out.ip + ':' + str(out.udp))
            except liblo.AddressError as err:
                print('liblo.AddressError' + str(err))
            if (isinstance(args, list) and 'ramp' in args) and (isinstance(args[0], int) == True or isinstance(args[0], float) == True):
                    # this is a ramp, make it in a separate thread
                    ramp = Ramp(target, address, args)
                    ramp.join()
            elif isinstance(args, list):
                msg = liblo.Message(address)
                for arg in args:
                    arg = checkType(arg)
                    msg.add(arg)
                liblo.send(target, msg)
            else:
                msg = liblo.Message(address)
                if args:
                    msg.add(args)
                liblo.send(target, msg)

    def play(self):
        """
        Play an EventOSC
        """
        player = self.Play(self)
        return player


class Wait(Event):
    """
    Play an EventWait
    """
    def __init__(self, duration, *args, **kwargs):
        super(Wait, self).__init__(duration, *args, **kwargs)
        self.duration = duration
        self.protocol = 'WAIT'

    class Play(threading.Thread):
        """docstring for Sleep"""
        def __init__(self, duration):
            threading.Thread.__init__(self)
            self.duration = duration
            self.start()

        def run(self):
            if debug:
                print('sleep starts in ' + self.name + ' at ' + str(datetime.datetime.now()))
            sleep(self.duration)
            if debug:
                print('sleep ends in ' + self.name + ' at ' + str(datetime.datetime.now()))

    def play(self):
        """
        Play an EventOSC
        """
        wait = Wait(self.duration)


class MidiNote(Event):
    """
    An OSC event is an Event designed to be outputed via OSC
    """
    def __init__(self, scenario, command, *args, **kwargs):
        super(MidiNote, self).__init__(scenario, command, *args, **kwargs)
        self.address = command[0]
        if len(command) > 1:
            self.args = command[:1]
        self.protocol = 'MidiNote'

    class Play(threading.Thread):
        """docstring for PlayOsc"""
        def __init__(self, out, event):
            threading.Thread.__init__(self)
            self.out = out
            self.command = event.command
            self.event = event
            self.start()

        def run(self):
            """
            Play the MidiNote
            """
            pass

    def play(self):
        """
        Play an EventOSC
        """
        pass