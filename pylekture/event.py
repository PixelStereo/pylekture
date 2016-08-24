#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Event Class
An Event is always in a project and it (may) be in one or several scenarios
Event is the baseclass for Scenario and Project.
It inherits from Node, and add some attributes as wait, post_wait, loop, autoplay and output.
It add a few methods too as play(), getduration() and getparent()
Event class is an abstract class.
Create Osc, MidiNote, Wait events with the project.new_event() constructor.
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
    def __init__(self,*args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        if self.name == 'Untitled Node':
            self.name = 'Untitled Event'
        if self.description == "I'm a node":
            self.description = "I'm an event"
        self.wait = 0
        self._output = 0
        self.post_wait = 0
        self._loop = False
        self._autoplay = False
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
            if name == 'Osc' or 'Scenario':
                self._output = output
        elif output_class.__name__ == 'OutputMidi':
            if name == 'MidiNote' or 'MidiControl' or 'MidiBend' or 'Scenario':
                self._output = output
        elif output_class.__name__ == "NoneType":
            self._output = 0
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
    def autoplay(self):
        """
        The autplay attribute. If true, the project plays when finish loading from hard drive
            :arg: Boolean
        """
        return self._autoplay
    @autoplay.setter
    def autoplay(self, autoplay):
        autoplay = checkType(autoplay)
        if autoplay == 0:
            autoplay = False
        elif autoplay > 0:
            autoplay = True
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
            if self.command:
                try:
                    if 'ramp' in self.command:
                        index = self.command.index('ramp')
                        duration += float(self.command[index + 1])
                except Exception:
                    pass
        return duration

    def play(self, output=None):
        """
        Play an event
        It creates a new object play in a separate thread.
        """
        return Player(self, output=output)


class Command(Event):
    """docstring for Command"""
    def __init__(self, project, command, port):
        super(Command, self).__init__(project, command, port)
        self._command = command

    def __repr__(self):
        s = "Command (name={name}, self.parent={parent}, description={description}, command={command} tags={tags}, autoplay={autoplay}, loop={loop}"
        return s.format(name=self.name,
                        parent=self.parent,
                        description=self.description,
                        command=self.command,
                        tags=self.tags,
                        autoplay=self.autoplay,
                        loop=self.loop)

    @property
    def command(self):
        """
        The content of the event
        It is a command that will be executate.
        """
        return self._command
    @command.setter
    def command(self, command):
        name = self.__class__.__name__
        command = checkType(command)
        flag = False
        if name == 'ScenarioPlay':
            if isinstance(command, list) and len(command) == 1:
                self._command = checkType(command[0])
            if isinstance(self._command, int):
                flag = True
            else:
                print(name + '.command for a ScenarioPlay must be an int')
                return False
        elif name == 'Wait':
            if isinstance(command, int) or isinstance(command, float):
                self._command = command
                flag = True
        elif name == 'MidiNote' or 'MidiControl':
            if isinstance(command, list) and len(command) == 3:
                self._command = command
                flag = True
            else:
                print('Error 9876543 -', command)
        if flag:
            return True
        else:
            print(name + '.command must be something else than a ' + str(type(command)))
            return False


class Player(threading.Thread):
    """
    A Player that play things
    """
    def __init__(self, parent, **kwargs):
        super(Player, self).__init__()
        self.parent = parent
        self.kwargs = kwargs
        self.start()

    def run(self):
        player = self.parent.Play(self.parent, self.kwargs)
        if player:
            player.join()


class Osc(Command):
    """
    An OSC event is an Event designed to be outputed via OSC
    """
    def __init__(self, project, command=None, port='127.0.0.1:1234'):
        super(Osc, self).__init__(project, command, port)
        if self._command == None:
            self._command = ['/lekture', 10]

    @property
    def command(self):
        """
        The content of the event
        It is a command that will be executate.
        """
        return self._command
    @command.setter
    def command(self, command):
        command = checkType(command)
        flag = False
        if isinstance(command, list) or isinstance(command, basestring):
            self._command = command
            flag = True
        return flag


    class Play(threading.Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, event, output):
            threading.Thread.__init__(self)
            if output['output']:
                self.output = output['output']
            else:
                self.output = event.output
            self.command = event.command
            self.event = event
            self.start()

        def run(self):
            """play an OSC event"""
            out = self.output
            args = self.command
            if out.port:
                if debug >= 3:
                    print('event-play: ' + self.event.name + ' in ' + str(threading.current_thread().name) + ' at ' + str(datetime.datetime.now()))
                split = out.port.split(':')
                ip = split[0]
                udp = split[1]
                if isinstance(args, list):
                    # address is the first item of the list
                    address = args[0]
                    args = args[1:]
                    if len(args) == 0:
                        args = None
                else:
                    # this is a adress_only without arguments
                    address = args
                    args = None
                try:
                    target = liblo.Address(ip, int(udp))
                    if debug >= 3:
                        print('connect to : ' + ip + ':' + str(udp))
                except liblo.AddressError as err:
                    print('liblo.AddressError' + str(err))
                if args:
                    args[0] = checkType(args[0])
                    if (isinstance(args, list) and 'ramp' in args) and (isinstance(args[0], int) == True or isinstance(args[0], float) == True):
                        # this is a ramp, make it in a separate thread
                        ramp = Ramp(target, address, args)
                        ramp.join()
                    elif isinstance(args, list):
                        # this is just a list of values to send
                        msg = liblo.Message(address)
                        for arg in args:
                            arg = checkType(arg)
                            msg.add(arg)
                        liblo.send(target, msg)
                    else:
                        # what iss this case?????
                        print("DEBUG", len(args), type(args))
                else:
                    msg = liblo.Message(address)
                    liblo.send(target, msg)
                if debug >= 3:
                    print('event-ends: ' + self.event.name + ' in ' + str(threading.current_thread().name) + ' at ' + str(datetime.datetime.now()))


class Wait(Command):
    """
    Play an EventWait
    """
    def __init__(self, project, command=None, port=None):
        super(Wait, self).__init__(project, command, port)
        if self._command == None:
            self._command = 1

    class Play(threading.Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, event, output):
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


class MidiNote(Command):
    """
    An OSC event is an Event designed to be outputed via OSC
    """
    def __init__(self, project, command=None, port=None):
        super(MidiNote, self).__init__(project, command, port)
        if self._command == None:
            self._command = [1, 64, 100]

    class Play(threading.Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, event, output):
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


class ScenarioPlay(Command):
    """
    Play a Scenario
    """
    def __init__(self, project, command=0, port=None):
        super(ScenarioPlay, self).__init__(project, command, port)

    class Play(threading.Thread):
        """
        Event Player
        It plays the event in a separate Thread
        """
        def __init__(self, event, output):
            threading.Thread.__init__(self)
            self.output = event.output
            if isinstance(event.command, int):
                self.command = event.parent.scenarios[checkType(event.command)]
            elif event.command.__class__.__name__ == 'Scenario':
                self.command = event.command
            else:
                print('ERROR 987654345678', event)
            self.event = event
            self.start()

        def run(self):
            if debug >= 3:
                print('ScenarioPlay starts')
            self.command.play()
            if debug >= 3:
                print('ScenarioPlay ends')
