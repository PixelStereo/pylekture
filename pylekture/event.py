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
from pylekture.errors import LektureTypeError


class Event(Node):
    """Create an Event
    an Event is like a step of a Scenario.
    It could be a delay, a goto value, a random process,
    a loop process or everything you can imagine """
    def __init__(self, parent, command=None, name=None, description='A few words about this event', output=None, wait=0, post_wait=0):
        super(Event, self).__init__(parent)
        self.scenario = parent
        if name == None:
            self.name = 'Untitled Event'
        self._command = command
        self._output = output
        self._wait = wait
        self._post_wait = post_wait

    @property
    def command(self):
        """
        The content of the event
        It is a command that will be executate.
        """
        return self._command
    @command.setter
    def command(self, command):
        output = self.output.__class__.__name__
        name = self.__class__.__name__
        if name == 'Osc':
            if isinstance(command, list) or isinstance(command, basestring):
                self._command = command
        elif name == 'Wait':
            if isinstance(command, int):
                self._command = command
        elif name == 'MidiNote' or 'MidiControl':
            if isinstance(command, list) and len(command) == 3:
                self._command = command

    @property
    def output(self):
        """
        The port to output this scenario
        Initialised to None if user does not set it.
        """
        if self._output:
            return self._output
        else:
            return self.parent.output
    @output.setter
    def output(self, output):
        output = output.__class__.__name__
        name = self.__class__.__name__
        if output == "OutputUdp":
            if name == 'Osc':
                self._output = output
        elif output == 'OutputMidi':
            if name == 'MidiNote' or 'MidiControl' or 'MidiBend':
                self._output = output
        else:
            raise LektureTypeError('Output', output)

    @property
    def wait(self):
        """
        Wait time in seconds
        """
        return self._wait
    @wait.setter
    def wait(self, wait):
        self._wait = wait

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
        self._post_wait = post_wait

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
        if classname == 'Ramp':
            duration += self.duration
        return duration
    

class Osc(Event):
    """
    An OSC event is an Event designed to be outputed via OSC
    """
    def __init__(self, scenario, command=None, *args, **kwargs):
        super(Osc, self).__init__(scenario, command, *args, **kwargs)

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
            if debug >= 3:
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
                if debug >= 3:
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


class Wait(Node):
    """
    Play an EventWait
    """
    def __init__(self, parent, duration, *args, **kwargs):
        super(Wait, self).__init__(parent, *args, **kwargs)
        self.duration = duration

    class Play(threading.Thread):
        """docstring for Sleep"""
        def __init__(self, duration):
            threading.Thread.__init__(self)
            self.duration = duration
            self.start()

        def run(self):
            if debug >= 3:
                print('sleep starts in ' + self.name + ' at ' + str(datetime.datetime.now()))
            sleep(self.duration)
            if debug >= 3:
                print('sleep ends in ' + self.name + ' at ' + str(datetime.datetime.now()))

    def play(self):
        """
        Play an EventOSC
        """
        wait = self.Play(self.duration)

    @property
    def duration(self):
        return self._duration
    @duration.setter
    def duration(self, duration):
        self._duration = duration

    def getduration(self):
        return self.duration


class MidiNote(Event):
    """
    An OSC event is an Event designed to be outputed via OSC
    """
    def __init__(self, scenario, command, *args, **kwargs):
        super(MidiNote, self).__init__(scenario, command, *args, **kwargs)
        self.address = command[0]
        if len(command) > 1:
            self.args = command[:1]

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
