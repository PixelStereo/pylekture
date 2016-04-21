#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Node Class
It's the base class that every object inherit
Contains name / description
"""

from pylekture.functions import prop_dict

class Node(object):
    """
    A Node is the base class for all objects in pylekture.
    It has at least a parent.
    Only Projects does not have a parent.
    All objects refer to the projects these have created with.
    An optional name, description and tags attributes can be used.
    The service is a read-only value used to check the obect used.
    It should be removed for the version 0.1

    """
    def __init__(self, parent=None, name='Untitled Node', description="I'm a node", tags=[]):
        super(Node, self).__init__()
        self._name = name
        self._description = description
        self._tags = []
        self.parent = parent
        #print('nodeparent', parent)

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

    @property
    def parent(self):
        """
        It is the parent of the node.
        It is None for a project.
        It is the project object for events, scenario and outputs

        :Returns:String
        """
        return self._parent
    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def tags(self):
        """
        a list of string used to create taxonimies.

        :Returns:List of Strings
        """
        return self._tags

    def add_tag(self, tag):
        if tag in self._tags:
            if debug >= 3:
                print('already in')
        else:
            self._tags.append(tag)
    def del_tag(self, tag):
        if tag in self._tags:
            self._tags.remove(tag)
        else:
            if debug >= 3:
                print('not in')

    def export(self):
        """
        export the content 
        """
        export = prop_dict(self)
        export.pop('parent')
        return prop_dict(self)

    def getstate(self):
        # what should I return that will be common for all nodes.
        # item for events, events for scenario...
        pass
