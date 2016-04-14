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
from pylekture.constants import debug
from pylekture.functions import checkType
from pylekture.event import Event


class Scenario(object):
    """Create a new scenario"""
    def __init__(self, project, name=None, description='', output=None, wait=0, post_wait=0):
        """create an scenario"""
        self.project = project
        if description == '':
            description = "write a comment"
        if not name:
            name = str(datetime.datetime.now())
        self.name = name
        self._project = project
        self.output = output
        self.description = description
        self.wait = wait
        self.post_wait = post_wait
        self.event_list = []
        self.index = 0
        self._loop = False

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
        player.join()
        return player


    class Play(threading.Thread):
        """Instanciate a thread for Playing a scenario
        Allow to start twice or more each scenario in the same time"""
        def __init__(self, scenario, index):
            self.project = scenario.project
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
                        print('WAIT', self.scenario.name, \
                              'DURING', self.scenario.wait, 'SECONDS')
                    sleep(self.scenario.wait)
            else:
                # start from the index, we will skip the pre-wait sleep
                index = self.index
            if debug:
                dbg = 'scenario-play: {scenario} from index {index} in {thread} at {time}'
                print(dbg.format(scenario=self.scenario.name, index=index, thread=str(threading.current_thread().name), time=str(datetime.datetime.now())))
            for event in self.scenario.events()[index:]:
                # play each event
                player = event.play()
                player.join()
            #return player
            if self.scenario.post_wait:
                # if there is a wait after the scenario, please wait!!
                if debug:
                    print('POST_WAIT', self.scenario.name, \
                          'DURING', self.scenario.post_wait, 'SECONDS')
                sleep(self.scenario.post_wait)
            # scenario is now finish
            return True

    def getduration(self):
        """return the duration of the scenario
        Addition the ramp flags with the wait events"""
        duration = 0
        for event in self.events():
            if isinstance(event.content, int) or isinstance(event.content, float):
                # this is a wait
                duration += event.content
            elif isinstance(event.content, list):
                # this is a wait in a list, unicode or string
                if len(event.content) == 1:
                    if isinstance(event.content[0], int) or isinstance(event.content[0], float):
                        duration += int(event.content[0])
                if 'ramp' in event.content:
                    # this is a ramp
                    index = event.content.index('ramp')
                    ramp = event.content[index+1]
                    duration += int(ramp)
        return duration

    def events(self):
        """return a list of events for this scenario"""
        return Event.getinstances(self)

    def new_event(self, *args, **kwargs):
        """create a new event for this scenario"""
        taille = len(self.event_list)
        the_event = None
        self.event_list.append(the_event)
        self.event_list[taille] = Event(self, args)
        for key, value in kwargs.items():
            setattr(self.event_list[taille], key, value)
        return self.event_list[taille]

    def del_event(self, index):
        """delete an event, by index or with object instance"""
        if isinstance(index, int):
            index -= 1
            self.event_list.pop(index)
        else:
            self.event_list.remove(index)

    def play_from_here(self, index):
        """play scenario from a given index"""
        if not isinstance(index, int):
            index = self.event_list.index(index)
        self.play(index)

    def getoutput(self):
        """get the output object for this scenario"""
        if self.output:
            out_protocol = self.output[0]
            out_index = self.output[1] - 1
            out_list = []
            for out in self._project.outputs():
                if out.getprotocol() == out_protocol:
                    out_list.append(out)
            if len(out_list) > out_index:
                output = out_list[out_index]
            else:
                output = None
        else:
            output = None
        return output

    def export_events(self):
        """export events of the project"""
        events = []
        for event in self.events():
            events.append({'attributes':{'output':event.output,\
                                         'name':event.name,\
                                         'description':event.description,\
                                         'content':event.content\
                                         }})
        return events
