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


class Scenario(Event):
    """
    A scenario is always created in a project.
    It contains events and have all the attributes of an event
    (name, description, tags, loop, autoplay, (service))
    """
    def __init__(self, *args, **kwargs):
        super(Scenario, self).__init__(*args, **kwargs)
        if self.name == 'Untitled Event':
            self.name = 'Untitled Scenario'
        if self.description == "I'm an event":
            self.description = "I'm a scenario"
        self.project = self.parent
        self.index = 0
        self._events = []

    def __repr__(self):
        s = "Scenario (name={name}, description={description}, duration={duration}, tags={tags}, autoplay={autoplay}, loop={loop}, " \
            "events={events})"
        return s.format(name=self.name,
                        description=self.description,
                        duration=self.getduration(),
                        tags=self.tags,
                        autoplay=self.autoplay,
                        loop=self.loop,
                        events=len(self.events))

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

    def del_event(self, event):
        """
        Remove an event from the scenario
        It won't delete the event, it just remove it of the scenario
        """
        try:
            self.events.remove(event)
        except ValueError:
            print('ERROR 1122 : No event is selected - cannot delete the event')


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
                        print('wait ',  self.scenario.name, 'during' , self.scenario.wait, 'seconds')
                    sleep(self.scenario.wait)
            else:
                # start from the index, we will skip the pre-wait sleep
                index = self.index
            if debug >= 3:
                dbg = 'scenario-play: {name} from index {index} in {thread} at {time}'
                print(dbg.format(name=self.scenario.name, index=index, thread=threading.current_thread().name, time=datetime.datetime.now()))
            for event in self.scenario.events[index:]:
                # play each event
                player = event.play()
                if player:
                    player.join()
            if debug >= 3:
                dbg = 'scenario-ends: {name} in {thread} at {time}'
                print(dbg.format(name=self.scenario.name, thread=threading.current_thread().name, time=datetime.datetime.now()))
            if self.scenario.post_wait:
                # if there is a wait after the scenario, please wait!!
                if debug >= 3:
                    print('post_wait ' , self.scenario, \
                          ' during ' , self.scenario.post_wait, ' seconds')
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

    def play(self, index=0):
        """
        Play a scenario
        It creates a new object play in a separate thread.
        """
        if self.events == []:
            print('This scenario is empty')
            return None
        else:
            return Player(self)

    def play_from_here(self, index):
        """play scenario from a given index"""
        if not isinstance(index, int):
            index = self.events.index(index)
        self.play(index)
