#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the Project Class, which is the base of our document.

To start with pylekture, you just need to import 2 functions

Here is an example to create a project.
    from pylekture.project import new_project, projects
    my_project = new_project()

Then, you can create an output and a scenario
    my_out = my_project.new_output('OSC')
    my_scenario = my_project.new_scenario()


You can here create a project, or make a list of projects available.
"""

import os
import weakref
import threading
from time import sleep
import simplejson as json

import datetime
from pylekture import __version__
from pylekture.scenario import Scenario
from pylekture.output import Output
from pylekture.constants import debug

def new_project():
    """Create a new project"""
    return Project()

def projects():
    """return a list of projects available"""
    project_list = []
    for proj in Project.getinstances():
        project_list.append(proj)
    return project_list

class Project(object):
    """
    A project handles everything you need. Ouputs and scenarios are all project-relative
    :param <version>: Version of the pylekture lib that created the project. Read-Only value
    :param <lastopened>: Datetime of the last opened date of this project. Default is None
    """

    # used  to make a list of projects
    _instances = []

    def __init__(self):
        super(Project, self).__init__()
        self._instances.append(weakref.ref(self))
        self._version = __version__
        self._path = None
        self.lastopened = None
        self._autoplay = False
        self._loop = False
        self._created = str(datetime.datetime.now())
        self._output_list = []
        self._scenario_list = []

    def __repr__(self):
        s = 'Project (path={path}, autoplay={autoplay}, loop={loop}, ' \
            'scenarios={scenarios})'
        return s.format(path=self.path,
                        autoplay=self.autoplay,
                        loop=self.loop,
                        scenarios=len(self.scenarios))

    @property
    def scenarios(self):
        """
        Return a list of scenarios for this project
        """
        return self._scenario_list

    @property
    def version(self):
        return self._version

    @property
    def path(self):
        return self._path
    @path.setter
    def path(self, value):
        self._path = value

    @property
    def autoplay(self):
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

    @classmethod
    def getinstances(cls):
        """retuurn a list with all project instances"""
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        for de in dead:
            cls._instances.remove(de)

    def reset(self):
        """reset a project by deleting project.attributes, scenarios, outputs and events related"""
        # reset project attributes
        self._version = None
        self._path = None
        # reset outputs
        self._output_list = []
        # reset scenarios and events
        self._scenario_list = []

    def read(self, path):
        """
        Read a lekture-project file from hard drive
            :arg: file to load. Filepath must be provided as a string/unicode.
                                Filepath will be checked, if valid it will be loaded
                                Otherwise, it will return False

            :rtype:True if the project has been correctly loaded, False otherwise
        """
        path = os.path.abspath(path)
        if not os.path.exists(path):
            print("ERROR 901 - THIS PATH IS NOT VALID " + path)
            return False
        else:
            print('loading project in ' + path)
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
            print('ERROR 906 - project not loaded, this is not a lekture-project file')
            return False
        self._path = path
        if self._autoplay:
            self.play()
        return flag

    def fillin(self, loaded):
        """
        Creates Outputs, Scenario and Events obects
            :rtype:True if file formatting is correct, False otherwise
        """
        try:
            for key in loaded.keys():
                if key == 'scenario':
                    for scenario in loaded['scenario']:
                        events = scenario['attributes'].pop('events')
                        scenar = self.new_scenario(**scenario['attributes'])
                        for event in events:
                            scenar.new_event(**event['attributes'])
                elif key == 'attributes':
                    for attribute, value in loaded['attributes'].items():
                        if attribute == 'created':
                            self._created = value
                        if attribute == 'version':
                            self._version = value
                        if attribute == 'autoplay':
                            self.autoplay = value
                        if attribute == 'loop':
                            self.loop = value
                    self.lastopened = str(datetime.datetime.now())
                elif key == 'outputs':
                    for protocol in loaded['outputs']:
                        for out in loaded['outputs'][protocol]:
                            self.new_output(protocol, **out['attributes'])
            print('project loaded')
            return True
        # catch error if file is not valid or if file is not a lekture project
        except (IOError, ValueError):
            if debug:
                print('ERROR 907 - project not loaded, this is not a lekture-project file')
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
            if not savepath.endswith('.json'):
                savepath = savepath + '.json'
            try:
                # create / open the file
                out_file = open((savepath), 'wb')
            except IOError:
                # path does not exists
                print('ERROR 909 - path is not valid, could not save project - ' + savepath)
                return False
            project = {}
            project.setdefault('scenario', self._export_scenario())
            project.setdefault('attributes', self._export_attributes())
            project.setdefault('outputs', self._export_outputs())
            out_file.write(json.dumps(project, sort_keys=True, indent=4,\
                                      ensure_ascii=False).encode('utf8'))
            print("file has been written : ", savepath)
            return True
        else:
            return False

    def play(self):
        """
        shortcut to run thread
        """
        if self.scenarios:
            self.Play(self)
        else:
            if debug:
                print('This project is empty')


    class Play(threading.Thread):
        """
        Instanciate a thread for Playing a whole project
        Allow to start twice or more each projects at the same time
        """
        def __init__(self, project):
            self.project = project
            threading.Thread.__init__(self)
            self.start()

        def run(self):
            for scenario in self.project.scenarios:
                # compute time in seconds (getduration is in milliseconds)
                wait = scenario.getduration() / 1000
                # add wait and post_wait to duration
                wait = wait + scenario.wait + scenario.post_wait
                if debug:
                    print('play', scenario, 'during', wait, 'seconds')
                # play the scenario
                scenario.play()
                # wait during the scenario
                sleep(wait)
            # all scenario have been played
            if self.project.loop:
                self.project.play()


    def scenarios_set(self, old, new):
        """Change order of a scenario in the scenario list of the project"""
        s_temp = self._scenario_list[old]
        self._scenario_list.pop(old)
        self._scenario_list.insert(new, s_temp)

    def outputs(self, protocol='all'):
        """return a list of available output for this project"""
        outs = []
        if protocol == 'all' or protocol == None:
            return Output.getinstances(self)
        else:
            for out in self._output_list:
                if out:
                    if protocol == out.getprotocol():
                        outs.append(out)
            return outs

    def getprotocols(self):
        """return the protocols available for this project"""
        protocols = []
        for out in self.outputs():
            proto = out.getprotocol()
            if not proto in protocols:
                protocols.append(proto)
        if protocols == []:
            return None
        else:
            return protocols

    def new_scenario(self, **kwargs):
        """
        Create a new scenario for this Project
            args:Optional args are every attributes of the scenario, associated with a keyword
            rtype:Scenario object
        """
        taille = len(self._scenario_list)
        scenario = Scenario(self)
        self._scenario_list.append(scenario)
        for key, value in kwargs.items():
            setattr(self._scenario_list[taille], key, value)
        return scenario

    def new_output(self, protocol, **kwargs):
        """
        Create a new output for this project
        args:Mandatory argument is the protocol that you want to use for this output
        (OSC, MIDI, serial, ArtNet)
        rtype:Output object
        """
        taille = len(self._output_list)
        the_output = None
        self._output_list.append(the_output)
        self._output_list[taille] = Output(self, protocol)
        for key, value in kwargs.items():
            setattr(self._output_list[taille], key, value)
        return self._output_list[taille]

    def del_scenario(self, scenario):
        """
        delete a scenario of this project
        This function will delete events of the scenario
        """
        if scenario in self.scenarios:
            # delete events of this scenario
            for event in scenario.events():
                scenario.del_event(event)
            # delete the scenario itself
            self._scenario_list.remove(scenario)
            if debug:
                print('delete scenario', scenario, len(self._scenario_list))
        else:
            if debug:
                print('ERROR - trying to delete a scenario which not exists \
                      in self._scenario_list', scenario)

    def _export_attributes(self):
        """export attributes of the project"""
        attributes = {'created':self._created, 'version':self.version, \
                      'lastopened':self.lastopened, 'loop':self._loop, 'autoplay':self._autoplay}
        return attributes

    def _export_scenario(self):
        """export scenario of the project"""
        scenarios = []
        for scenario in self.scenarios:
            scenarios.append({'attributes':{'output':scenario.output, \
                                            'name':scenario.name, \
                                            'description':scenario.description, \
                                            'events':scenario.export_events()}})
        return scenarios

    def _export_outputs(self):
        """export outputs of the project"""
        outputs = {}
        for output in self.outputs():
            protocol = output.getprotocol()
            if not protocol in outputs:
                outputs.setdefault(protocol, [])
            outputs[protocol].append({'attributes':{}})
            index = len(outputs[protocol])
            index -= 1
            for attr in output.vars_():
                if not attr.startswith('_'):
                    outputs[protocol][index]['attributes'].setdefault(attr, getattr(output, attr))
        return outputs
