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
from pylekture.node import Node
from pylekture.scenario import Scenario
from pylekture.output import OSC, MIDI, PJLINK
from pylekture.constants import debug, _projects
from pylekture.functions import prop_dict
from pylekture.event import OSC as EventOSC
from pylekture.event import Event
from pylekture.event import Wait as EventWait
from pylekture.event import MidiNote as EventMidiNote

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


class Project(Node):
    """
    A project handles everything you need.
    Ouputs and scenarios are all project-relative
    """
    def __init__(self):
        super(Project, self).__init__()
        self._version = __version__
        self._path = None
        self._lastopened = None
        self._autoplay = False
        self._loop = False
        self._created = str(datetime.datetime.now())
        self._output = None
        self._outputs = []
        self._scenarios = []
        self._events = []

    def __repr__(self):
        s = "Project (path={path}, autoplay={autoplay}, loop={loop}, " \
            "scenarios={scenarios})"
        return s.format(name=self.name,
                        path=self.path,
                        autoplay=self.autoplay,
                        loop=self.loop,
                        scenarios=len(self.scenarios))

    @property
    def output(self):
        """
        The port to output this project
        Initialised to the first output (created when creating a project)
        """
        if self._output:
            return self._output
        else:
            if self._outputs:
                return self._outputs[0]
            else:
                raise OutputZeroError('This project has no output')
    @output.setter
    def output(self, output):
        if output.__class__ == 'Output':
            self._output = output
        else:
            raise LektureTypeError('Wait for an Output but receive a', output.__class__, output)

    @property
    def lastopened(self):
        """
        Datetime of the last opened date of this project. Default is None

        :getter: datetime object
        :type getter: string
        """
        return self._lastopened

    @property
    def version(self):
        """
        The version of pylekture used to create this project
        Read-Only

        :return: version (tag + number of commits since tag + sha of commit)
        :rtype: string
        """
        return self._version

    @property
    def path(self):
        """
        This is the filepath of the project.
        It's initialised at None when created, and can be set to any valid path.

        :param path: valid filepath. Return True if valid, False otherwise.
        :type path: string
        """
        return self._path
    @path.setter
    def path(self, value):
        self._path = value

    @property
    def autoplay(self):
        """
        If True, it will play the project when it is opened
        """
        return self._autoplay
    @autoplay.setter
    def autoplay(self, value):
        self._autoplay = value

    @property
    def loop(self):
        """
        If enable, the project play again when it reaches the end of the scenarios

        :getter:    Returns the status of the loop flag
        :setter:    Sets this loop flag
        :type:      Boolean
        """
        return self._loop
    @loop.setter
    def loop(self, value):
        self._loop = value

    def _export_attributes(self):
        """export attributes of the project"""
        attributes = {"name":self._name, "created":self._created, "version":self.version, \
                      "lastopened":self.lastopened, "loop":self._loop, "autoplay":self._autoplay}
        return attributes

    def reset(self):
        """reset a project by deleting project.attributes, scenarios, outputs and events related"""
        # reset project attributes
        self._version = None
        self._path = None
        # reset outputs
        self._outputs = []
        # reset scenarios and events
        self._scenarios = []

    def read(self, path):
        """
        Read a lekture-project file from hard drive. Must be valid.
        if valid it will be loaded and return True, otherwise, it will return False

            :param path: Filepath to read from.
            :type path: string
            :returns: Boolean
            :rtype: True if the project has been correctly loaded, False otherwise
        """
        path = os.path.abspath(path)
        if not os.path.exists(path):
            print("ERROR 901 - THIS PATH IS NOT VALID " + path)
            return False
        else:
            print("loading project in " + path)
            return self.load(path)

    def load(self, path):
        """
        Load a lekture-project from a file from hard drive
        It will play the file after loading, according to autoplay attribute value

            :arg: file to load. Filepath must be valid when provided, it must be checked before.

            :rtype:True if the project has been correctly loaded, False otherwise
        """
        try:
            with open(path) as in_file:
                # clear the project
                loaded = json.load(in_file)
                in_file.close()
                # reset project
                self.reset()
                # create objects from loaded file
                flag = self.fillin(loaded)
        # catch error if file is not valid or if file is not a lekture project
        except (IOError, ValueError):
            print("ERROR 906 - project not loaded, this is not a lekture-project file")
            return False
        self._path = path
        if self._autoplay:
            self.play()
        return flag

    def fillin(self, loaded):
        """
        Creates Outputs, Scenario and Events obects
        First, dump attributes, then outputs, scenario and finish with events.

        :returns: True if file formatting is correct, False otherwise
        :rtype: boolean
        """
        try:
            # dump attributes
            attributes = loaded.pop('attributes')
            for attribute, value in attributes.items():
                if attribute == "created":
                    self._created = value
                if attribute == "version":
                    self._version = value
                if attribute == "autoplay":
                    self.autoplay = value
                if attribute == "loop":
                    self.loop = value
                if attribute == "name":
                    self.name= value
            self._lastopened = str(datetime.datetime.now())
            # dump outputs
            outputs = loaded.pop('outputs')
            for out in outputs:
                self.new_output(**out)
            scenarios = loaded.pop('scenarios')
            # dump scenario
            for scenario in scenarios:
                output = scenario['output']
                if output != None:
                    # refer to the corresponding output instance object
                    scenario['output'] = self.outputs[output]
                    scenar = self.new_scenario(**scenario)
            # dump events after scenario, because event can reference a scenario
            events = loaded.pop("events")
            for event in events:
                self.new_event(event['protocol'], **event)
            if loaded == {}:
                # project has been loaded, lastopened date changed
                # we have a path because we loaded a file from somewhere
                print("project loaded")
                self.write()
                return True
            else:
                print('ERROIR 906 - loaded file has not been totally loaded', loaded )
                return False
        # catch error if file is not valid or if file is not a lekture project
        except (IOError, ValueError) as Error:
            if debug:
                print(Error, "ERROR 907 - project not loaded, this is not a lekture-project file")
            return False

    def write(self, path=None):
        """
        Write a project on the hard drive.
        """
        if path:
            savepath = path
        else:
            savepath = self._path
        if savepath:
            # make sure we will write a file with json extension
            if not savepath.endswith(".lekture"):
                savepath = savepath + ".lekture"
            try:
                # create / open the file
                out_file = open((savepath), "wb")
            except IOError:
                # path does not exists
                print("ERROR 909 - path is not valid, could not save project - " + savepath)
                return False
            project = {}
            project.setdefault("scenarios", self._export_scenario())
            project.setdefault("attributes", self._export_attributes())
            project.setdefault("outputs", self._export_outputs())
            project.setdefault("events", self.export_events())
            out_file.write(json.dumps(project, sort_keys=True, indent=4,\
                                      ensure_ascii=False).encode("utf8"))
            print("file has been written in " + savepath)
            return True
        else:
            return False

    def play(self):
        """
        shortcut to run thread
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
            if debug:
                dbg = "project-play: {project} in {thread} - it is {time}"
                print(dbg.format(project=self.project.name, thread=str(threading.current_thread().name), time=str(datetime.datetime.now())))
            self.start()

        def run(self):
            for scenario in self.project.scenarios:
                # compute time in seconds (getduration is in milliseconds)
                wait = scenario.getduration() / 1000
                # add wait and post_wait to duration
                wait = wait + scenario.wait + scenario.post_wait
                # play the scenario
                scenario.play()

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
                if protocol == out.protocol:
                    outputs.append(out)
            return outputs
        else:
            return None

    def getprotocols(self):
        """return the protocols available for this project"""
        protocols = []
        for out in self.outputs:
            proto = out.protocol
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
        if protocol == "OSC":
            output = OSC()
        elif protocol == "MIDI":
            output = MIDI()
        elif protocol == "PJLINK":
            output = PJLINK()
        else:
            output = None
        if output:
            self._outputs.append(output)
        for key, value in kwargs.items():
            setattr(self._outputs[taille], key, value)
        return self._outputs[taille]

    def _export_outputs(self):
        """export outputs of the project"""
        outputs = []
        for output in self.outputs:
            outputs.append(prop_dict(output))
        return outputs

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
            args:Optional args are every attributes of the scenario, associated with a keyword
            rtype:Scenario object
        """
        taille = len(self._scenarios)
        scenario = Scenario(self)
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
        This function will delete events of the scenario
        """
        if scenario in self.scenarios:
            # delete events of this scenario
            for event in scenario.events:
                scenario.del_event(event)
            # delete the scenario itself
            self._scenarios.remove(scenario)
            if debug:
                print("delete scenario", scenario, len(self._scenarios))
        else:
            if debug:
                print("ERROR - trying to delete a scenario which not exists \
                      in self._scenarios", scenario)

    def _export_scenario(self):
        """export scenario of the project"""
        scenarios = []
        events = []
        for scenario in self.scenarios:
            for event in self.events:
                events.append(self.events.index(event))
            scenarios.append({"output":self.outputs.index(scenario.output), \
                              "name":scenario.name, "description":scenario.description, \
                              "events":events
                              })
        return scenarios

    @property
    def events(self):
        """
        All the events of this scenario
        """
        return self._events

    def new_event(self, event_type, command, **kwargs):
        """
        create a new event for this scenario
        """
        taille = len(self.events)
        the_event = None
        self.events.append(the_event)
        if event_type == 'OSC':
            self.events[taille] = EventOSC(self, command)
        elif event_type == 'WAIT':
            self.events[taille] = EventWait(self, command)
        elif event_type == 'MidiNote':
            self.events[taille] = EventMidiNote(self, command)
        for key, value in kwargs.items():
            setattr(self.events[taille], key, value)
        return self.events[taille]

    def del_event(self, index):
        """
        delete an event, by index or with object instance
        """
        if isinstance(index, int):
            index -= 1
            self.events.pop(index)
        else:
            self.events.remove(index)

    def export_events(self):
        """
        export events of the project
        """
        events = []
        for event in self.events:
            events.append({'output':event._output, 'name':event.name,\
                           'description':event.description, 'command':event.command, \
                           'protocol':event.protocol
                          })
        return events
