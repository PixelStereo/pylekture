#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Scenario Class
A scenario is always in a project and it (may) contains events
"""

import datetime
import threading
from time import sleep
from pylekture.event import Event
from pylekture.constants import debug


class Scenario(Event):
    """Create a new scenario"""
    def __init__(self, parent, name=None, description='write a comment', output=None, wait=0, post_wait=0):
        super(Scenario, self).__init__(parent, name, description, output, wait, post_wait)
        if self.name == 'Untitled Node':
            self.name = 'Untitled Scenario'
        self.project = self.parent
        self.index = 0
        self._events = []

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
        def __init__(self, scenario, index=0):
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
            if debug >= 3:
                dbg = '>>>>> scenario-ends: {scenario} in {thread} at {time}'
                print(dbg.format(scenario=self.scenario, thread=threading.current_thread().name, time=datetime.datetime.now()))
            if self.scenario.post_wait:
                # if there is a wait after the scenario, please wait!!
                if debug >= 3:
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
            duration += event.getduration()
        duration += self.wait
        duration += self.post_wait
        return duration

    def play_from_here(self, index):
        """play scenario from a given index"""
        if not isinstance(index, int):
            index = self.events.index(index)
        self.play(index)
