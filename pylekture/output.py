#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements output for scenario-events
An ouput is an object that can send-out commands.
Maybe we might use some plug in pybush to have in/out access for a bunch of nodes (pybush / a bush)
"""

from pylekture.node import Node

class Output(Node):
    """
    Create a new output
    Need to be revamped - protocol miqht be an attribute
    => and protocol-parameters might be in a dict inside the attributes dict?
    """
    def __init__(self):
        super(Output, self).__init__()

    @staticmethod
    def getinstances(project):
        """
        return a list of outputs for a given project
        """
        return project._output_list

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


class MIDI(Output):
    """Create a MIDI output"""
    def __init__(self, port=0, channel=0, midi_type='CC'):
        super(MIDI, self).__init__()
        self._port = port
        self._channel = channel
        self._type = midi_type

    @property
    def protocol(self):
        """
        get the protocol for this output
        """
        return 'MIDI'


class OutputIP(Output):
    """docstring for IP"""
    def __init__(self, ip='127.0.0.1', udp=1234):
        super(OutputIP, self).__init__()
        self._udp = udp
        self._ip = ip

    @property
    def udp(self):
        return self._udp
    @udp.setter
    def udp(self, port):
        self._udp = port

    @property
    def ip(self):
        return self._ip
    @ip.setter
    def ip(self, ip):
        self._ip = ip


class OSC(OutputIP):
    """Create an OSC output"""
    def __init__(self):
        super(OSC, self).__init__()

    @property
    def protocol(self):
        """
        get the protocol for this output
        """
        return 'OSC'


class PJLINK(OutputIP):
    """Create a PJLINK output"""
    def __init__(self):
        super(PJLINK, self).__init__()
        self.udp = 4352

    @property
    def protocol(self):
        """
        get the protocol for this output
        """
        return 'PJLINK'
