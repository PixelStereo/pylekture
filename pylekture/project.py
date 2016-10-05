#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the Project Class, which is the base of our document.

To start with pylekture, you just need to import 2 functions

Here is an example to create a project.
    from pylekture.project import new_project, projects
    my_project = new_project()

Then, you can create an output and a scenario
    my_out = my_project.new_output("OSC")
    my_scenario = my_project.new_scenario()


You can here create a project, or make a list of projects available.
"""

import os
import threading
import simplejson as json

import datetime
from pylekture import __version__
from pylekture.scenario import Scenario
from pylekture.output import OutputUdp, OutputMidi
from pylekture.constants import debug, _projects
from pylekture.functions import prop_dict
from pylekture.event import Osc, MidiNote, Event, Wait, ScenarioPlay
from pylekture.errors import NoOutputError, LektureTypeError

def new_project():
    """
    Create a new project
    :
    """
    try:
        size = len(_projects)
        _projects.append(Project())
        return _projects[size]
    except Exception as problem:
        print('ERROR 22' + str(problem))
        return False

def projects():
    """
    List of all projects available
    """
    return _projects


class Project(Event):
    """
    A project handles everything you need.
    Ouputs and scenarios are all project-relative
    """
    def __init__(self):
        super(Project, self).__init__(parent=None)
        if self.name == 'Untitled Event':
            self.name = 'Untitled Project'
        if self.description == "I'm an event":
            self.description = "I'm a project"
        self._version = __version__
        self._lastopened = None
        self._created = str(datetime.datetime.now())
        self._outputs = []
        self._scenarios = []
        self._events = []


    def __repr__(self):
        s = "Project (name={name}, path={path}, description={description}, tags={tags}, autoplay={autoplay}, loop={loop}, " \
            "scenarios={scenarios}, events={events})"
        return s.format(name=self.name,
                        path=self.path,
                        description=self.description,
                        tags=self.tags,
                        autoplay=self.autoplay,
                        loop=self.loop,
                        scenarios=len(self.scenarios),
                        events=len(self.events))

    @property
    def output(self):
        """
        The port to output this project
        Initialised to the first output
        """
        if self._output:
            return self._output
        else:
            if self._outputs:
                return self._outputs[0]
            else:
                raise NoOutputError()
    @output.setter
    def output(self, out):
        if out.__class__.__name__ == 'OutputUdp' or out.__class__.__name__ == 'OutputMidi':
            self._output = out
        else:
            raise LektureTypeError('Wait for an Output but receive a', out.__class__)

    @property
    def lastopened(self):
        """
        Datetime of the last opened date of this project. Default is None

        :getter: datetime object
        :type getter: string
        """
        return self._lastopened

    @property
    def created(self):
        """
        Datetime of the creation of the project

        :getter: datetime object
        :type getter: string
        """
        return self._created

    @property
    def version(self):
        """
        The version of pylekture used to create this project
        Read-Only

        :return: version (tag + number of commits since tag + sha of commit)
        :rtype: string
        """
        return self._version

    def reset(self):
        """reset a project by deleting project.attributes, scenarios, outputs and events related"""
        # reset project attributes
        self._version = None
        self._path = None
        # reset outputs
        self._outputs = []
        # reset scenarios
        self._scenarios = []
        # reset  events
        self._events = []

    def export(self):
        """
        export a project into a dict/json string
        """
        export = {}
        export.setdefault('attributes', {})
        for key, value in prop_dict(self).items():
            if key == 'events':
                events = []
                for event in value:
                    events.append(event.export())
                export.setdefault('events', events)
            elif key == 'outputs':
                outputs = []
                for output in value:
                    outputs.append(output.export())
                export.setdefault('outputs', outputs)
            elif key == 'scenarios':
                scenarios = []
                for scenario in value:
                    scenarios.append(scenario.export())
                export.setdefault('scenarios', scenarios)
            else:
                export['attributes'].setdefault(key, value)
        export['attributes'].pop('parent')
        return export

    def play(self, index=0):
        """
        Play the whole project from the beginning.
        If you provide index argument, you can specify where to start the project playing.
        project.play(index=4) will start from the forth scenario of the project.
        If if does not exist, it will return False.

        :param index: Optional
        :type index: integer
        """
        if self.scenarios:
            player = self.Play(self)
            player.join()
            # all scenario have been played
            if self.loop:
                self.play()
        else:
            if debug:
                print("This project is empty")


    class Play(threading.Thread):
        """
        Instanciate a thread for Playing a whole project
        Allow to start twice or more each projects at the same time
        """
        def __init__(self, project):
            self.project = project
            threading.Thread.__init__(self)
            if debug >= 3:
                dbg = "project-play: {name} in {thread} - it is {time}"
                print(dbg.format(name=self.project.name, thread=str(threading.current_thread().name), time=str(datetime.datetime.now())))
            self.start()

        def run(self):
            for scenario in self.project.scenarios:
                # compute time in seconds (getduration is in milliseconds)
                wait = scenario.getduration() / 1000
                # add wait and post_wait to duration
                wait = wait + scenario.wait + scenario.post_wait
                # play the scenario
                scenario.play()
            if debug >= 3:
                dbg = "project-ends: {name} in {thread} - it is {time}"
                print(dbg.format(name=self.project.name, thread=str(threading.current_thread().name), time=str(datetime.datetime.now())))

    def scenarios_set(self, old, new):
        """Change order of a scenario in the scenario list of the project"""
        s_temp = self._scenarios[old]
        self._scenarios.pop(old)
        self._scenarios.insert(new, s_temp)

    @property
    def outputs(self):
        """
        return a list of outputs of this project
        """
        return self._outputs

    def getoutputs(self, protocol):
        """
        return a list of available output for this protocol
        """
        if self.outputs:
            outputs = []
            for out in self.outputs:
                if protocol == out.__class__.__name__:
                    outputs.append(out)
            return outputs
        else:
            return None

    def getprotocols(self):
        """return the protocols available for this project"""
        protocols = []
        for out in self.outputs:
            proto = out.__class__.__name__
            if not proto in protocols:
                protocols.append(proto)
        if protocols == []:
            return None
        else:
            return protocols

    def new_output(self, protocol="OSC", **kwargs):
        """
        Create a new output for this project
        args:Mandatory argument is the protocol that you want to use for this output
        (OSC, MIDI, serial, ArtNet)
        rtype:Output object
        """
        taille = len(self._outputs)
        if protocol == "OSC" or protocol == 'OutputUdp':
            output = OutputUdp(parent=self)
        elif protocol == "MIDI" or protocol == 'OutputMidi':
            output = OutputMidi(parent=self)
        else:
            output = None
        if output:
            for key, value in kwargs.items():
                setattr(output, key, value)
            self._outputs.append(output)
            return self._outputs[taille]
        else:
            return False

    @property
    def scenarios(self):
        """
        Report existing scenarios

        :return: All Scenario of this project
        :rtype: list
        """
        return self._scenarios

    def new_scenario(self, **kwargs):
        """
        Create a new scenario for this Project
            :args: Optional args are every attributes of the scenario, associated with a keyword
            :rtype: Scenario object
        """
        taille = len(self._scenarios)
        scenario = Scenario(parent=self)
        self._scenarios.append(scenario)
        for key, value in kwargs.items():
            if key == 'events':
                for event in value:
                    scenario.add_event(self.events[event])
            else:
                setattr(self._scenarios[taille], key, value)
        return scenario

    def del_scenario(self, scenario):
        """
        delete a scenario of this project
        This function won't delete events of the scenario
        """
        if scenario in self.scenarios:
            # delete the scenario
            self._scenarios.remove(scenario)
        else:
            if debug:
                print("ERROR - trying to delete a scenario which not exists \
                      in self._scenarios", scenario)
    @property
    def events(self):
        """
        All the events of this scenario
        """
        return self._events

    def new_event(self, event_type, command=None, **kwargs):
        """
        create a new event for this scenario
        """
        taille = len(self.events)
        the_event = None
        self.events.append(the_event)
        if isinstance(command, Scenario):
            command = self.scenarios.index(command)
        event = self.new_event_create(event_type, command)
        if event:
            self.events[taille] = event
            for key, value in kwargs.items():
                # set all attributes provided of the new event
                setattr(self.events[taille], key, value)
                # put the new event in the list of existing events for this project
            return self.events[taille]
        else:
            return None

    def new_event_create(self, event_type, command):
        event = None
        if event_type == 'Osc':
            event = Osc(self, command=command)
        elif event_type == 'Wait':
            event = Wait(self, command=command)
        elif event_type == 'MidiNote':
            event = MidiNote(self, command=command)
        elif event_type == 'ScenarioPlay':
            event = ScenarioPlay(self, command=command)
        elif event_type == 'PjLink':
            if command == None:
                command = ['shutter', True]
            event = PjLink(self, command=command)
        return event


    def del_event(self, index):
        """
        delete an event, by index or with object instance
        """
        used = False
        for scenario in self.scenarios:
            if index in scenario.events:
                print('WARNING 2 - this event is still referenced in scenario ' + scenario.name)
                used = True
        if not used:
            index = self.events.index(index)
            self.events.pop(index)
            return True
        else:
            return False

    def del_output(self, output):
        """
        delete an output of this project
        This function will delete  of the scenario
        """
        if output in self.outputs:
            # delete the output
            self._outputs.remove(output)
        else:
            if debug:
                print("ERROR - trying to delete an output which not exists \
                      in self._outputs", output)