#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import random
import weakref
import devicemanager
from time import sleep
from functions import timestamp
from functions import unicode2_list
from functions import unicode2string_dict
from functions import unicode2string_list
from OSC import OSCMessage , OSCClientError
from socket import socket
from socket import error as socket_error
from pjlink import Projector
from devicemanager import OSCClient as OSCClient
client = OSCClient()

debug = True

class Output(object):
    """Create a new output"""
    def __init__(self,project,protocol='OSC',name='no-name'):
        if debug == 2:
            print
            print "........... OUTPUT created ..........."
            print
        self._protocol = protocol
        self._project = project
        self.name = name
        if protocol == 'OSC':
            osc = OSC()
            self.ip = osc.ip
            self.udp = osc.udp
        if protocol == 'PJLINK':
            pjlink = PJLINK()
            self.ip = pjlink.ip
            self.udp = pjlink.udp
        if protocol == 'MIDI':
            midi = MIDI()
            self.port = midi.port
            self.channel = midi.channel
            self.type = midi.type

    @staticmethod
    def getinstances(project):
        """return a list of outputs for a given project"""
        return project.output_list

    @staticmethod
    def protocols():
        return ['OSC','MIDI','PJLINK']

    def getprotocol(self):
        return self._protocol

    def getproject(self):
        return self._project

    def vars_(self):
        # make a copy
        attrs = list(vars(self).keys())
        for attr in attrs:
            if attr.startswith('_'):
                attrs.remove(attr)
        return attrs


class OSC(Output):
    """Create an OSC output"""
    def __init__(self,ip='127.0.0.1',udp =10000):
        if debug == 2:
            print
            print "........... OSC OUTPUT created ..........."
            print
        self.udp = udp
        self.ip=ip

class PJLINK(Output):
    """Create a PJLINK output"""
    def __init__(self,ip='10.0.0.10',udp =4352):
        if debug == 2:
            print
            print "........... PJLINK OUTPUT created ..........."
            print
        self.udp = udp
        self.ip=ip

class MIDI(Output):
    """Create a MIDI output"""
    def __init__(self,port=0,channel=0,midi_type='CC'):
        if debug == 2:
            print
            print "........... MIDI OUTPUT created ..........."
            print
        self.port = port
        self.channel=channel
        self.type = midi_type