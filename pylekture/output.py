#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements output for scenario-events
An ouput is an object that can send-out commands.
Maybe we might use some plug in pybush to have in/out access for a bunch of nodes (pybush / a bush)
"""

from pylekture.constants import debug

class Output(object):
    """
    Create a new output
    Need a 
    """
    def __init__(self, project, protocol='OSC', name='no-name'):
        self._protocol = protocol
        self._project = project
        self.name = name
        if debug:
            print('new output with protocol : ' + protocol)
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
        """
        return a list of outputs for a given project
        """
        return project._output_list

    @staticmethod
    def protocols():
        """
        return a list of protocols available
        """
        #return ['OSC','MIDI','PJLINK']
        return ['OSC']

    def getprotocol(self):
        """
        get the protocol for this output
        """
        return self._protocol

    def getproject(self):
        """
        return the project of this output
        """
        return self._project

    def vars_(self):
        """
        return a list of attributes for this output
        """
        # make a copy
        attrs = list(vars(self).keys())
        for attr in attrs:
            if attr.startswith('_'):
                attrs.remove(attr)
        return attrs


class OSC(Output):
    """Create an OSC output"""
    def __init__(self, ip='127.0.0.1', udp=1234):
        self.udp = udp
        self.ip = ip

class PJLINK(Output):
    """Create a PJLINK output"""
    def __init__(self, ip='10.0.0.10', udp=4352):
        self.udp = udp
        self.ip = ip

class MIDI(Output):
    """Create a MIDI output"""
    def __init__(self, port=0, channel=0, midi_type='CC'):
        self.port = port
        self.channel = channel
        self.type = midi_type
