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


class Event(object):
    """Create an Event
    an Event is like a step of a Scenario.
    It could be a delay, a goto value, a random process,
    a loop process or everything you can imagine """
    def __init__(self, scenario, content=None, name='', description='', output=None):
        self.project = scenario.project
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


    class Play(threading.Thread):
        """docstring for PlayOsc"""
        def __init__(self, out, event):
            threading.Thread.__init__(self)
            self.out = out
            self.content = event.content
            self.event = event
            self.start()

        def join(self):
            threading.Thread.join(self)
            if debug:
                print('event-end: ' + self.event.name + ' in ' + self.name + ' ends - ' + str(datetime.datetime.now()))

        def run(self):
            """play an OSC event"""
            if debug:
                print('event-play: ' + self.event.name + ' in ' + str(threading.current_thread().name) + ' at ' + str(datetime.datetime.now()))
            out = self.out
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
                print('liblo.AddressError' + str(err))
            if (isinstance(args, list) and 'ramp' in args) and (isinstance(args[0], int) == True or isinstance(args[0], float) == True):
                    # this is a ramp, make it in a separate thread
                    ramp = self.Ramp(target, address, args)
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
                if debug:
                    print('ramp starts in ' + self.name + ' at ' + str(datetime.datetime.now()))
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
                    sleep(0.00072)
                    msg.add(value)
                    liblo.send(self.target, msg)

            def join(self):
                threading.Thread.join(self)
                if debug:
                    print('ramp ends in ' + self.name + ' at ' + str(datetime.datetime.now()))

    class Sleep(threading.Thread):
        """docstring for Sleep"""
        def __init__(self, duration):
            threading.Thread.__init__(self)
            self.duration = duration
            self.start()

        def run(self):
            if debug:
                print('sleep starts in ' + self.name + ' at ' + str(datetime.datetime.now()))
            sleep(self.duration)

        def join(self):
            threading.Thread.join(self)
            if debug:
                print('sleep ends in ' + self.name + ' at ' + str(datetime.datetime.now()))
            

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
                if wait <= 1:
                    print('waiting ' + str(wait) + ' second')
                else:
                    print('waiting ' + str(wait) + ' seconds')
            sleeper = self.Sleep(wait)
            return sleeper
        else:
            out = self.getoutput()
            if out:
                if out.getprotocol() == 'OSC':
                    player = self.Play(out, self)
                    return player
                else:
                    print('ERROR 503 - protocol ' + out.getprotocol() + ' is not yet implemented')
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
            try:
                output = self.scenario._project.outputs(protocol)[output]
            except IndexError:
                print('ERROR in getoutput - please clip the value to existing outputs')
                return False
        return output