
#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Node is the Base class of all items in a namespace.
Every Model, Application or Parameter is based on the Node Class
"""

from pydular import debug

class Node(object):
    """Base Class for all item in the namespace"""
    def __init__(self, name, tags=None, priority=None):
        self._name = name
        self._tags = tags
        self._priority = priority
        if debug:
            print ("........... NODE %s Inited  ..........." %name)

    def __repr__(self):
        printer = 'Node (name:{name}, priority:{priority}, tags:{tags})'
        return printer.format(name=self.name, priority=self.priority, tags=self.tags)

    @property
    def name(self):
        "Current name of the model"
        return self._name
    @name.setter
    def name(self, name):
        self._name = name
    @name.deleter
    def name(self):
        pass

    # ----------- TAGS -------------
    @property
    def tags(self):
        "Current tags of the model"
        return self._tags
    @tags.setter
    def tags(self, tags):
        self._tags = tags
    @tags.deleter
    def tags(self):
        pass

    # ----------- PRIORITY -------------
    @property
    def priority(self):
        "Current priority of the model"
        return self._priority
    @priority.setter
    def priority(self, priority):
        self._priority = priority
    @priority.deleter
    def priority(self):
        pass
