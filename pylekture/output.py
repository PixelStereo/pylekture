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
    def __init__(self, parent):
        super(Output, self).__init__(parent)
        if self.name == 'Untitled Node':
            self.name = 'Untitled Output'


class OutputMidi(Output):
    """
    Creates an output port for Midi Device.
    A Midi Device can handle all type of Midi messages
    """
    def __init__(self, parent, port=None):
        super(OutputMidi, self).__init__(parent)
        self._port = port
        if self.name == 'Untitled Output':
            self.name = 'Untitled Midi Output'

    @property
    def port(self):
        return self._port
    @port.setter
    def port(self, port):
        self._port = port


class OutputUdp(Output):
    """
    OutputUdp is a based class for all UDP based output
    You can use it if you want to send raw UDP.
    If you want to send OSC through UDP, please use OutputOsc as it checks if your OSC messages
    are correctly formatted.
    We might create a new class : OutputOsc as a subclass of OutputUdp.
    It should be used to double check that you send a correct OSC format message/bundle.
    """
    def __init__(self, parent, ip='127.0.0.1', udp=1234):
        super(OutputUdp, self).__init__(parent)
        self._udp = udp
        self._ip = ip
        if self.name == 'Untitled Output':
            self.name = 'Untitled Udp Output'

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
