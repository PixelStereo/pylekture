#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""implements a Scenario Class that contains events"""

import liblo
import threading
from time import sleep
from pylekture.constants import debug
from pylekture.functions import checkType
import datetime


class Scenario(object):
    """Create a new scenario"""
    def __init__(self, project, name=None, description='', output=None, wait=0, post_wait=0):
        """create an scenario"""
        self.project = project
        if debug == 2:
            print("........... SCENARIO created ...........")
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

    def play(self, index=0):
        """shortcut to run thread"""
        self.Play(self, index)


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
                print('PLAY', self.scenario.name, 'FROM INDEX', index)
            for event in self.scenario.events()[index:]:
                # play each event
                event.play()
            if self.scenario.post_wait:
                # if there is a wait after the scenario, please wait!!
                if debug:
                    print('POST_WAIT', self.scenario.name, \
                          'DURING', self.scenario.post_wait, 'SECONDS')
                sleep(self.scenario.post_wait)
            if debug:
                print('SCENARIO DONE', self.scenario.name)
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


class Event(object):
    """Create an Event
    an Event is like a step of a Scenario.
    It could be a delay, a goto value, a random process,
    a loop process or everything you can imagine """
    def __init__(self, scenario, content=None, name='', description='', output=None):
        self.project = scenario.project
        if debug == 2:
            print("........... Event created ...........")
        if description == '':
            description = "event's description"
        if name == '':
            name = 'untitled event'
        if not content:
            content = "no content for this event"
        self.name = name
        self.scenario = scenario
        self.description = description
        self.content = content
        if not output:
            self.output = 'parent'

    @staticmethod
    def getinstances(scenario):
        """return a list of events for a given scenario"""
        return scenario.event_list

    def play_osc(self,out):
        """play an OSC event"""
        args = self.content
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
            print(err)
        if isinstance(args, list) and 'ramp' in args:
            # this is a ramp, make it in a separate thread
            self.Ramp(target, address, args)
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


    class Ramp(threading.Thread):
        """Instanciate a thread for Playing a ramp
        Allow to do several ramps in a same scenario"""
        def __init__(self, target, address, args):
            threading.Thread.__init__(self)
            self.args = args
            self.address = address
            self.target = target
            self.start()

        def run(self):
            index = self.args.index('ramp')
            ramp = self.args[index+1]
            dest = self.args[index-1]
            dest = checkType(dest)
            ramp = checkType(ramp)
            value = 0
            delta = dest - value
            delta = float(delta)
            step = delta / ramp
            for millisec in range(ramp):
                msg = liblo.Message(self.address)
                value += step
                sleep(0.0008)
                msg.add(value)
                liblo.send(self.target, msg)
        

    def play(self):
        """play an event"""
        wait = 0
        if isinstance(self.content, list):
            if len(self.content) == 1 and str(self.content[0]).isdigit():
                wait = float(self.content[0])
        elif isinstance(self.content, int):
            wait = float(self.content)
        if wait:
            wait = wait/1000
            if debug:
                print('waiting', wait)
            sleep(wait)
        else:
            out = self.getoutput()
            if out:
                if out.getprotocol() == 'OSC':
                    self.play_osc(out)
                else:
                    print('ERROR XXX - protocol ' + out.getprotocol() + ' is not yet implemented')
            else:
                print('there is no output for this event / scenario')

    def getoutput(self):
        """rerurn the current output for this event.
        If no output is set for this event,
        parent scenario output will be used"""
        if self.output == 'parent':
            output = self.scenario.output
        else:
            output = self.output
        if output:
            protocol = output[0]
            output = output[1] - 1
            output = self.scenario._project.outputs(protocol)[output]
        return output
