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
        self._loop = False

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
        command = checkType(command)
        flag = False
        if name == 'Osc':
            if isinstance(command, list) or isinstance(command, basestring):
                self._command = command
                flag = True
        elif name == 'Wait':
            if isinstance(command, int) or isinstance(command, float):
                self._command = command
                flag = True
        elif name == 'MidiNote' or 'MidiControl':
            if isinstance(command, list) and len(command) == 3:
                self._command = command
                flag = True
        if flag:
            return True
        else:
            print(name + '.command must be something else than a ' + str(type(command)))
            return False

    @property
    def output(self):
        """
        The port to output this scenario
        Initialised to None if user does not set it.
        """
        if self._output:
            return self._output
        else:
            parent = self.getparent()
            if parent:
                return self.parent.output
            else:
                return self.parent.output

    @output.setter
    def output(self, output):
        output_class = output.__class__
        name = self.__class__.__name__
        if output_class.__name__ == "OutputUdp":
            if name == 'Osc' or 'scenario':
                print(output, self._output)
                self._output = output
        elif output_class.__name__ == 'OutputMidi':
            if name == 'MidiNote' or 'MidiControl' or 'MidiBend' or 'scenario':
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
            if 'ramp' in self.command:
                index = self.command.index('ramp')
                duration += float(self.command[index + 1])
        return duration

    def play(self):
        """
        Play an event
        It creates a new object play in a separate thread.
        """
        player = self.Play(self)
        if player:
            player.join()
        return player


class Osc(Event):
    """
    An OSC event is an Event designed to be outputed via OSC
    """
    def __init__(self, scenario, command=None, *args, **kwargs):
        super(Osc, self).__init__(scenario, command, *args, **kwargs)

    class Play(threading.Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
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
            args[0] = checkType(args[0])
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


class Wait(Event):
    """
    Play an EventWait
    """
    def __init__(self, parent, duration=1, *args, **kwargs):
        super(Wait, self).__init__(parent, *args, **kwargs)
        self._command = duration

    def play(self, index=0):
        """
        Play a scenario
        It creates a new object play in a separate thread.
        """
        player = self.Play(self)
        if player:
            player.join()
        return player

    class Play(threading.Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, event):
            threading.Thread.__init__(self)
            self.output = event.output
            self.command = event.command
            self.event = event
            self.start()

        def run(self):
            if debug >= 3:
                print('sleep starts in ' + self.name + ' at ' + str(datetime.datetime.now()))
            sleep(self.command)
            if debug >= 3:
                print('sleep ends in ' + self.name + ' at ' + str(datetime.datetime.now()))


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
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, event):
            threading.Thread.__init__(self)
            self.output = event.output
            self.command = event.command
            self.event = event
            self.start()

        def run(self):
            """
            Play the MidiNote
            """
            print('MidiNote is not ready for now… please wait a few months')
