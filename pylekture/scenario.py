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
from pylekture.event import Event
from pylekture.constants import debug


class Scenario(Node):
    """Create a new scenario"""
    def __init__(self, project, output=None, wait=0, post_wait=0):
        super(Scenario, self).__init__()
        self.project = project
        self._output = output
        self._wait = wait
        self._post_wait = post_wait
        self._events = []
        self.index = 0
        self._loop = False

    @property
    def output(self):
        """
        Output of the scenario
        """
        if self._output:
            return self._output
        else:
            outputs = self.project.outputs()
            if outputs:
                output = outputs[0]
                return output
            else:
                return False
    @output.setter
    def output(self, output):
        self._output = output

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
    @events.setter
    def events(self, events):
        self._events = events


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
                    if debug:
                        print('------ WAIT ',  self.scenario.name, 'DURING' , self.scenario.wait, 'SECONDS')
                    sleep(self.scenario.wait)
            else:
                # start from the index, we will skip the pre-wait sleep
                index = self.index
            if debug:
                dbg = '------ scenario-play: {scenario} from index {index} in {thread} at {time}'
                print(dbg.format(scenario=self.scenario, index=index, thread=threading.current_thread().name, time=datetime.datetime.now()))
            for event in self.scenario.events[index:]:
                # play each event
                player = event.play()
                if player:
                    player.join()
            #return player
            if self.scenario.post_wait:
                # if there is a wait after the scenario, please wait!!
                if debug:
                    print('>>>>> POST_WAIT ' , self.scenario, \
                          ' DURING ' , self.scenario.post_wait, ' SECONDS')
                sleep(self.scenario.post_wait)
            # scenario is now finish
            return True

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

    def new_event(self, *args, **kwargs):
        """create a new event for this scenario"""
        taille = len(self.events)
        the_event = None
        self.events.append(the_event)
        self.events[taille] = Event(self, args)
        for key, value in kwargs.items():
            setattr(self.events[taille], key, value)
        return self.events[taille]

    def del_event(self, index):
        """delete an event, by index or with object instance"""
        if isinstance(index, int):
            index -= 1
            self.events.pop(index)
        else:
            self.events.remove(index)

    def play_from_here(self, index):
        """play scenario from a given index"""
        if not isinstance(index, int):
            index = self.events.index(index)
        self.play(index)

    def export_events(self):
        """export events of the project"""
        events = []
        for event in self.events:
            events.append({'output':event._output, 'name':event.name,\
                           'description':event.description, 'command':event.command
                            })
        return events
