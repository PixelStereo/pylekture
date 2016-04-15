#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Node Class
It's the base class that every object inherit
Contains name / description
"""


class Node(object):
    """Create a new scenario"""
    def __init__(self, name='no-name', description='write a comment', \
                 output=None, wait=0, post_wait=0):
        super(Node, self).__init__()
        self._name = name
        self._description = description

    @property
    def name(self):
        """
        Name of the scenario
        """
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        """
        Description of the scenario
        """
        return self._description
    @description.setter
    def description(self, description):
        self._description = description
