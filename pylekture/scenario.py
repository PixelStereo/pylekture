#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Scenario Class
A scenario is always in a project and it (may) contains events
"""

import datetime
import threading
from time import sleep
from pylekture.node import Node
from pylekture.event import Event, OSC
from pylekture.constants import debug


class LektureTypeError(LookupError):
    """docstring for LektureTypeError"""
    def __init__(self, expected, received):
        super(LektureTypeError, self).__init__()
        dbg = 'Wait for an {expected} instance object but receive a {received}'
        print(dbg.format(expected=expected, received=received.__class__))


class Scenario(Node):
    """Create a new scenario"""
    def __init__(self, project, output=None, wait=0, post_wait=0):
        super(Scenario, self).__init__()
        self.project = project
        self._output = output
        self._wait = wait
        self._post_wait = post_wait
        self.index = 0
        self._loop = False
        self._events = []

    @property
    def output(self):
        """
        The port to output this scenario
        Initialised to None if user does not set it.
        """
        if self._output:
            return self._output
        else:
            return self.project.output
    @output.setter
    def output(self, output):
        if str(output.__class__) == "<class 'pylekture.output.OSC'>":
            self._output = output
        elif str(output.__class__) == "<class 'pylekture.output.PJLINK'>":
            self._output = output
        elif str(output.__class__) == "<class 'pylekture.output.MIDI'>":
            self._output = output
        else:
            print()
            print('-------------')
            print(output.__class__)
            print()
            print()
            #raise LektureTypeError('OSC', output)

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

    def play(self, index=0):
        """
        Play a scenario
        It creates a new object play in a separate thread.
        """
        player = self.Play(self, index)
        if player:
            player.join()
        return player

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

    @property
    def events(self):
        """
        All the events of this scenario
        """
        return self._events

    def add_event(self, event, index='last'):
        """
        Add an event to the scenario

        :param event: The event to be add to the events of this scenario
        :type event: Lekture.Event instance
        """
        if index == 'last':
            self._events.append(event)
        else:
            self._events.insert(index, event)

    def del_event(self, index):
        """
        delete an event, by index or with object instance
        """
        if isinstance(index, int):
            index -= 1
            self.events.pop(index)
        else:
            self.events.remove(index)

    def export_events(self):
        """
        export events of the project
        """
        events = []
        for event in self.events:
            events.append({'output':event._output, 'name':event.name,\
                           'description':event.description, 'command':event.command
                            })
        return events


    class Play(threading.Thread):
        """Instanciate a thread for Playing a scenario
        Allow to start twice or more each scenario in the same time"""
        def __init__(self, scenario, index):
            threading.Thread.__init__(self)
            self.scenario = scenario
            self.index = index
            self.start()

        def run(self):
            """play a scenario from the beginning
            play an scenario
            Started from the first event if an index has not been provided"""
            if not self.index:
                # start from the begining
                index = 0
                if self.scenario.wait:
                    # if there is a wait, please wait!!
                    if debug >= 3:
                        print('>>>>> WAIT ',  self.scenario.name, 'DURING' , self.scenario.wait, 'SECONDS')
                    sleep(self.scenario.wait)
            else:
                # start from the index, we will skip the pre-wait sleep
                index = self.index
            if debug >= 3:
                dbg = '>>>>> scenario-play: {scenario} from index {index} in {thread} at {time}'
                print(dbg.format(scenario=self.scenario, index=index, thread=threading.current_thread().name, time=datetime.datetime.now()))
            for event in self.scenario.events[index:]:
                # play each event
                player = event.play()
                if player:
                    player.join()
            #return player
            if self.scenario.post_wait:
                # if there is a wait after the scenario, please wait!!
                if debug >= 3:
                    print('>>>>> POST_WAIT ' , self.scenario, \
                          ' DURING ' , self.scenario.post_wait, ' SECONDS')
                sleep(self.scenario.post_wait)
            # scenario is now finish
            return True

        def join(self, timeout=None):
            if debug >= 3:
                dbg = '>>>>> scenario-ends: {scenario} in {thread} at {time}'
                print(dbg.format(scenario=self.scenario, thread=threading.current_thread().name, time=datetime.datetime.now()))

    def getduration(self):
        """return the duration of the scenario
        Addition the ramp flags with the wait events"""
        duration = 0
        for event in self.events:
            if isinstance(event.command, int) or isinstance(event.command, float):
                # this is a wait
                duration += event.command
            elif isinstance(event.command, list):
                # this is a wait in a list, unicode or string
                if len(event.command) == 1:
                    if isinstance(event.command[0], int) or isinstance(event.command[0], float):
                        duration += int(event.command[0])
                if 'ramp' in event.command:
                    # this is a ramp
                    index = event.command.index('ramp')
                    ramp = event.command[index+1]
                    duration += int(ramp)
        return duration

    def play_from_here(self, index):
        """play scenario from a given index"""
        if not isinstance(index, int):
            index = self.events.index(index)
        self.play(index)
