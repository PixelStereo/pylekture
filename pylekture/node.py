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
    @tags.setter
    def tags(self, tags):
        self._tags = tags

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

    @property
    def service(self):
        """
        Return the class name as a string
        """
        return self.__class__.__name__

    def export(self):
        """
        export the content 
        """
        # create a dict to export the content of the node
        export = {}
        # this is the dictionary of all props (output is already processed)
        props = prop_dict(self)
        # just the keys please
        keys = props.keys()
        for key in keys:
            # for an output, we just need the index, not the output object
            if key == 'output':
                if props['output']:
                    if props['output'] in self.parent.outputs:
                        export.setdefault('output', self.parent.outputs.index(props['output']))
                else:
                    export.setdefault('output', None)
            elif key == 'events':
                # for an event, we just need the index, not the event object
                export.setdefault('events', [])
                if props['events']:
                    for event in props['events']:
                        export['events'].append(self.parent.events.index(event))
                else:
                    export.setdefault(['events'], [])
            else:
                # this is just a property, dump them all !!
                export.setdefault(key, props[key])
        # we don't need parent in an export, because the JSON/dict export format do that
        export.pop('parent')
        return export

    def getstate(self):
        # what should I return that will be common for all nodes.
        # item for events, events for scenario...
        pass
