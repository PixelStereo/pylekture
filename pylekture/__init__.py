#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
pylekture is a python package that provide an API to create scenario for intermedia projects.

The project is designed around the concept of a project, that handles scenario, 
which itself contains events.

An events can be a command or a wait for now, but we should extendending the concept
 later during the implementation.

In details : 
    - A project contains Scenario and Outputs.
        - A scenario contains an ordered list of Events.
        - A scenario outputs its events to a choosen Output.
        - An output is a in/out protocol such as OSC, MIDI, Serial, Artnet etc…

An output is associated to the project. But you can redirect each scenario to a different output
and even more.
If an output is given for an event, it will overwrite the scenario output for this event.

-------------------------------------------------------------------------------

    Copyright (c) 2015 - 2016 Pixel Stereo

-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Changelog
-------------------------------------------------------------------------------

- v0.1.9 - Apr. 6th 2016
    - New name. Now known as pylekture, for python lekture framework.

- v0.1.8  - Apr. 5th 2016
    - nice and robust utf-8 encoding everywhere. That means using unicode for any string.
    - add project.play() method (bunch of scenario)
    - add project.autoplay attribute
    - add project.loop attribute
    - transform project.path as property
    - transform scenarios from method to property

- v0.1.7  -  Jan. 25th 2016
    - New name. Now known as pydular, for python modular implementation
    - enhance tests

- v0.1.4  -  Jan. 6th 2016
    - Split Modular file into Node, Application, Model and Parameter different files
    - Split Projekt file into Project, Output and Scenario different files
    - Rename projekt into project

- v0.1.3  - Jan. 3th 2016
	- Revamp projects() and scenarios() method
	- Remove a few horribles global variables that existed
	- same attributes are now private and use methods for access. e.g. such as output.getprotocol()

- v0.1.2  - Dec. 31th 2015
    - New design for Outputs
    - various fixes

- v0.1.1  - Dec. 27th 2015
    - ADD new Class Design. Project / Scenario / Event
    - FIX output

- v0.1  - Dec. 25th 2015
    - First draft
"""

_applications = []

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
__release__ = __version__
