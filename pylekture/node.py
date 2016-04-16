#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Node Class
It's the base class that every object inherit
Contains name / description
"""


class Node(object):
    """Create a new scenario"""
    def __init__(self, name='no-name', description='write a comment'):
        super(Node, self).__init__()
        self._name = name
        self._description = description

    @property
    def name(self):
        """
        It acts as a nick name.
        You can have several nodes with the same name
        Read-Only

        :Returns:String
        """
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        """
        Description of this node
        You could here send a few words explainig this node.

        :Args:String
        :Returns:String
        """
        return self._description
    @description.setter
    def description(self, description):
        self._description = description
