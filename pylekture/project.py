#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the Project Class, which is the base of our document.

To start with pylekture, you just need to import 2 functions

Here is an example to create a project.
    from pylekture.project import new_project, projects
    my_project = new_project()

Then, you can create a scenario
    my_scenario = my_project.new_scenario()


You can here create a project, or make a list of projects available.
"""

import os
import threading
import simplejson as json

import datetime
from pylekture import __version__
from pylekture.scenario import Scenario
from pylekture.constants import debug, _projects
from pylekture.functions import prop_dict
from pylekture.ramp import Ramp
from pylekture.random import Random
from pylekture.errors import LektureTypeError

def new_project(*args, **kwargs):
    """
    Create a new project
    :
    """
    try:
        size = len(_projects)
        _projects.append(Project(*args, **kwargs))
        return _projects[size]
    except Exception as problem:
        print('ERROR 22' + str(problem))
        return False

def projects():
    """
    List of all projects available
    """
    return _projects


class Project(object):
    """
    A project handles everything you need.
    Scenarios and Events are all project-relative
    """
    def __init__(self, *args, **kwargs):
        super(Project, self).__init__()
        self.name = 'Untitled Project'
        self.description = "I'm a project"
        self._version = __version__
        self._path = None
        self.service = self.__class__.__name__
        self._lastopened = None
        self._created = str(datetime.datetime.now())
        self._scenarios = []
        self._autoplay = None
        self._events = []
        for key, value in kwargs.items():
            setattr(self, key, value)


    def __repr__(self):
        s = "Project (name={name}, path={path}, description={description}, autoplay={autoplay}, " \
            "scenarios={scenarios}, events={events})"
        return s.format(name=str(self.name).encode('utf-8'),
                        path=self.path,
                        description=self.description,
                        autoplay=self.autoplay,
                        scenarios=len(self.scenarios),
                        events=len(self.events))

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

    def reset(self):
        """reset a project by deleting project.attributes, scenarios and events related"""
        # reset project attributes
        self._version = None
        self._path = None
        # reset scenarios
        self._scenarios = []
        # reset  events
        self._events = []

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
            if self.load(path):
                self._path = path
                self.write(path)
                if self._autoplay:
                    self.play()
                return True
            else:
                return False

    def load(self, path):
        """
        Load a lekture-project from a file from hard drive
        It will play the file after loading, according to autoplay attribute value

            :arg: file to load. Filepath must be valid when provided, it must be checked before.

            :rtype:True if the project has been correctly loaded, False otherwise
        """
        flag = False
        try:
            with open(path) as in_file:
                # clear the project
                loaded = json.load(in_file)
                flag = True
        # catch error if file is not valid or if file is not a lekture project
        except (IOError, ValueError):
            print("ERROR 906 - project not loaded, this is not a lekture-project file")
            return False
        if flag:
            # create objects from loaded file
            flag = self.fillin(loaded)
        return flag

    def fillin(self, loaded):
        """
        Creates Scenario and Events obects
        First, dump attributes, then scenario and finish with events.

        :returns: True if file formatting is correct, False otherwise
        :rtype: boolean
        """
        try:
            # reset project
            self.reset()
            # dump attributes
            attributes = loaded.pop('attributes')
            for attribute, value in attributes.items():
                if attribute == "created":
                    self._created = value
                elif attribute == "version":
                    self._version = value
                elif attribute == "autoplay":
                    self.autoplay = value
                elif attribute == "loop":
                    self.loop = value
                elif attribute == "name":
                    self.name= value
            self._lastopened = str(datetime.datetime.now())
            # dump scenarios
            scenarios = loaded.pop('scenarios')
            # dump events before scenario, because a scenario contains events
            events = loaded.pop("events")
            for event in events:
                # remove the service name. We are in the event dict, so we are sure that it is an event
                service = event.pop('service')
                self.new_event(service, **event)
            # dump scenario
            for scenario in scenarios:
                service = scenario.pop('service')
                self.new_scenario(**scenario)
            if loaded == {}:
                # project has been loaded, lastopened date changed
                # we have a path because we loaded a file from somewhere
                print("project loaded")
                return True
            else:
                print('ERROIR 906 - loaded file has not been totally loaded', loaded)
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
            if savepath.endswith("/"):
                savepath = savepath + self.name
            # make sure we will write a file with json extension
            # TODO : deal with a constant in the constants file
            if not savepath.endswith(".lekture"):
                savepath = savepath + ".lekture"
            try:
                # create / open the file
                out_file = open((savepath), "wb")
            except IOError:
                # path does not exists
                # TODO : make rules and list for all errors
                print("ERROR 909 - path is not valid, could not save project - " + savepath)
                return False
            project = self.export()
            try:
                the_dump = json.dumps(project, sort_keys=True, indent=4,\
                                      ensure_ascii=False).encode("utf8")
            except TypeError as Error:
                print('ERROR 98 ' + str(Error))
                return False
            try:
                out_file.write(the_dump)
                print("file has been written in " + savepath)
                out_file.close()
                self.path = os.path.realpath(savepath)
                return True
            except TypeError as Error:
                print('ERROR 99 ' + str(Error))
                return False
        else:
            print('no filepath. Where do you want I save the project?')
            return False

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
            elif key == 'scenarios':
                scenarios = []
                for scenario in value:
                    scenarios.append(scenario.export())
                export.setdefault('scenarios', scenarios)
            else:
                export['attributes'].setdefault(key, value)
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
        size = len(self._scenarios)
        scenario = Scenario(parent=self)
        self._scenarios.append(scenario)
        for key, value in kwargs.items():
            if key == 'events':
                for event in value:
                    scenario.add_event(self.events[event])
            else:
                setattr(self._scenarios[size], key, value)
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

    def new_ramp(self, *args, **kwargs):
        """
        create a ramp object, that refer to a Parameter object
        it has also a destination (value), a duration and a grain.
        """
        size = len(self.events)
        the_event = None
        self.events.append(the_event)
        ramp = Ramp(*args, **kwargs)
        if ramp:
            self.events[size] = ramp
            for key, value in kwargs.items():
                # set all attributes provided of the new event
                setattr(self.events[size], key, value)
                # put the new event in the list of existing events for this project
            return self.events[size]
        else:
            return None

    def del_ramp(self, index):
        """
        delete an event, by index or with object instance
        """
        used = False
        for scenario in self.scenarios:
            if index in scenario.events:
                print('WARNING 2 - this ramp is still referenced in scenario ' + scenario.name)
                used = True
        if not used:
            index = self.events.index(index)
            self.events.pop(index)
            return True
        else:
            return False

    def new_random(self, *args, **kwargs):
        """
        create a random object, that refer to a Parameter object
        it has also a destination (value), a duration and a grain.
        """
        size = len(self.events)
        the_event = None
        self.events.append(the_event)
        ramp = Random(*args, **kwargs)
        if ramp:
            self.events[size] = ramp
            for key, value in kwargs.items():
                # set all attributes provided of the new event
                setattr(self.events[size], key, value)
                # put the new event in the list of existing events for this project
            return self.events[size]
        else:
            return None

    def del_random(self, index):
        """
        delete an event, by index or with object instance
        """
        used = False
        for scenario in self.scenarios:
            if index in scenario.events:
                print('WARNING 2 - this random is still referenced in scenario ' + scenario.name)
                used = True
        if not used:
            index = self.events.index(index)
            self.events.pop(index)
            return True
        else:
            return False
