#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""pylekture is a python package that provide an API to create scenario for intermedia projects.

The API is designed around the concept of a project, that handles scenario and outputs.
Each scenario contains events.

- Project: this is a bunch of Outputs and Scenario
- Output: This is frome here that you output Events
- Scenario:This is a bunch of Events
- Event:This is a command for a device, or a wait for the the Scenario


An output is associated to the project. But you can redirect each scenario to a different output
and even more. If an output is specified for an event, it will be use to output this event.
Even if it is different that the output associated with the parent scenario.

In details:
    - A project contains a list of Scenario and Outputs.
    - A scenario contains an ordered list of Events.
    - A scenario outputs its events to a choosen Output.
    - An output is a in/out protocol such as OSC, MIDI, Serial, Artnet etc…

Project has a few attributes:
    - version(read-only):the version of pylekture used to create this Project
    - lastopened:timestamp of the last time pylekture opened this file
    - created:timestamp of the creation of this file
    - autoplay:enable/disable play when file is loaded
    - loop:enable/disable play when project file reach ends of a play

-------------------------------------------------------------------------------

                Copyright (c) 2015 - 2016 Pixel Stereo

-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Changelog
-------------------------------------------------------------------------------

- v0.2.2 - ??
    - Massive Revamp
        - outputs is now attribute of project
        - events is now attributes of scenario
        - command is now atrributes of event (instead of content)
        - remove all useless nodes called 'attributes' in the json export file
    - Revamp Output link to project / scenario / events

- v0.2.1 - Apr. 12th 2016
    - Introduce .lekture extension instead of .json extension
    - Revamp Project Attributes
        - Remove author attribute
        - Version attribute is now the version of pylekture used to create this project
        - Fix created/lastopened attributes
        - Name attribute (might be file name)
    - Enhance unit-testing
    - Use Thread.join() as mechanism to be notified when the previous event/scenario has been sent

- v0.2.0 - Apr. 6th 2016
    - Use versioneer to take care of versionning
        - https://github.com/warner/python-versioneer

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
    - First draft"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
__release__ = __version__
