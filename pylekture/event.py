#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
The Event Class
An Event is always in a project and it may be in one or several scenario.
Event is the baseclass for Scenario and Project.
It inherits from Node, and add some attributes as wait, post_wait, loop and autoplay.
It adds a few methods too as play(), getduration() and getparent()
"""

from pylekture.functions import prop_dict
from pylekture.functions import checkType
from pylekture import is_string

class Event(object):
    """
    An Event is the base class for all events
    It has at least a parent.
    Only Projects does not have a parent.
    All objects refer to the projects these have created with.
    An optional name, description and tags attributes can be used.
    The service is a read-only value used to check the obect used.
    It should be removed for the version 0.1

    """
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__()
        self._name = 'Untitled Node'
        self._description = 'Node without a description'
        self._tags = ['No Tags', 'notag']
        self._is_template = False
        self.wait = 0
        self.post_wait = 0
        self._loop = False
        self._autoplay = False
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        s = "Event (name={name}, parent={parent}, description={description}, is_template={is_template} \
             duration={duration}, tags={tags}, autoplay={autoplay}, loop={loop}"
        return s.format(name=self.name,
                        description=self.description,
                        is_template=self.is_template,
                        duration=self.getduration(),
                        tags=self.tags,
                        autoplay=self.autoplay,
                        loop=self.loop)
    @property
    def name(self):
        """
        It acts as a nick name.
        You can have several nodes with the same name
        Read-Only

        :Returns:String
        """
        # be sure to return a string
        if not is_string(self._name):
            self._name = str(self._name)
        return self._name
    @name.setter
    def name(self, name):
        if isinstance(name, list):
            name_maker = ""
            for item in name:
                name_maker = name_maker + " " +  str(item)
            name = name_maker
        if name:
            if name.startswith(" "):
                name = name[1:]
        self._name = name

    @property
    def description(self):
        """
        Description of this node
        You could here send a few words explainig this node.

        :Args:String
        :Returns:String
        """
        return str(self._description)
    @description.setter
    def description(self, description):
        self._description = description

    @property
    def parent(self):
        """
        It is the parent of the node.
        It is None for a project.
        It is the project object for events and scenarios

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
    def is_template(self):
        return self._is_template
    @is_template.setter
    def is_template(self, state):
        self._is_template = state


    @property
    def wait(self):
        """
        Wait time in seconds
        """
        return self._wait
    @wait.setter
    def wait(self, wait):
        if isinstance(wait, int) or isinstance(wait, float):
            self._wait = wait
            return True

    @property
    def post_wait(self):
        """
        Time to wait after all events played and before the end of this scenario
        unit:
        seconds
        """
        return self._post_wait
    @post_wait.setter
    def post_wait(self, post_wait):
        if isinstance(post_wait, int) or isinstance(post_wait, float):
            self._post_wait = post_wait
            return True

    @property
    def autoplay(self):
        """
        The autplay attribute. If true, the project plays when finish loading from hard drive
            :arg: Boolean
        """
        return self._autoplay
    @autoplay.setter
    def autoplay(self, autoplay):
        self._autoplay = autoplay

    @property
    def loop(self):
        """
        The loop attribute. If true, the loop plays again when it reach its end.
            :arg: Boolean
        """
        return self._loop
    @loop.setter
    def loop(self, loop):
        self._loop = loop

    @property
    def service(self):
        """
        Return the class name as a string
        """
        return self.__class__.__name__

    def getduration(self):
        """
        Computed duration of the event
        Read-Only

        :returns: Duration of the item
        :rtype: integer
        """
        duration = 0
        duration += self.wait
        duration += self.post_wait
        classname = self.__class__.__name__
        if classname == 'Wait':
            duration += self.command
        else:
            if self.command:
                try:
                    if 'ramp' in self.command:
                        index = self.command.index('ramp')
                        duration += float(self.command[index + 1])
                except Exception:
                    pass
        return duration

    def export(self):
        """
        export the content
        """
        # create a dict to export the content of the node
        export = {}
        # this is the dictionary of all props
        props = prop_dict(self)
        # just the keys please
        keys = props.keys()
        for key in keys:
            if key == 'events':
                # for an event, we just need the index, not the event object
                export.setdefault('events', [])
                if props['events']:
                    for event in props['events']:
                        if event.__class__.__name__ == "ScenarioPlay":
                            export.setdefault('events', [])
                        else:
                            export['events'].append(self.parent.events.index(event))
                else:
                    export.setdefault('events', [])
            else:
                # this is just a property, dump them all !!
                export.setdefault(key, props[key])
        # Itarate a second time to link ScenarioPlay obkects with Scenario
        for key in keys:
            if key == 'events':
                if props['events']:
                    for event in props['events']:
                        if event.__class__.__name__ == "ScenarioPlay":
                            export['events'].append(self.parent.events.index(event))
        # we don't need parent in an export, because the JSON/dict export format do that
        export.pop('parent')
        return export

    def getstate(self):
        # what should I return that will be common for all nodes.
        # item for events, events for scenario...
        pass
