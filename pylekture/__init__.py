#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""pylekture is a python package that provide an API to create scenario for intermedia projects.

The API is designed around the concept of a project, that handles Events.
A Scenario is a bunch of events.
An Event contain one or a thousand of Command
A Command is a Parameter Value + an animation

- Project: this is a bunch of Scenario and Events
- Scenario: This is a bunch of Events
- Event: This is a bunch of commands

In details:
    - A project contains a Scenario, Events.
    - A scenario contains an ordered list of Events.
    - An Event conains Commands.
    - Commands are Parameter State with a Way to go there
    - Event, Scenario and Project can have wait, post_wait, loop, autoplay.

Project has a few attributes:
    - version(read-only):the version of pylekture used to create this Project
    - lastopened(read-only):timestamp of the last time pylekture opened this file
    - created:timestamp of the creation of this file
    - autoplay:enable/disable play when file is loaded

Project / Scenario / Event attributes:
    - loop:enable/disable play when project file reach ends of a play
    - wait:time in seconds to wait before start when triggered
    - post_wait:time in seconds to wait when finished before sending finish-message

-------------------------------------------------------------------------------

                Copyright (c) 2015 - 2019 Pixel Stereo

-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
Changelog
-------------------------------------------------------------------------------
- v0.4.0 - work in progress
    - No more output concept. Parameters outputs value, pylekture deals with parameters, not protocols
    	- pylekture will be test with pybush (pure python) and pyossia (libossia python binding)
    - Scenario is now just a bunch of events
    - Events might be:
    	- a ramp animation
    	- a random generation
    - add PySignal to generate PyQt-like signals
    	- https://github.com/dgovil/PySignal

- v0.3.1 - Aug. 8 2016
    - Fix output menu now display the right output in scenario & events tables
    - output 0 means "use parent" and output > 0 represents the index in the outputs list of the project
    - Fix OSC message without arguments
    - Fix events header

- v0.3 - Apr. 24 2016
    - Fix output hierarchy. parent is the default output. Project default output is the first one
    - redefine str() buildtin to unicode() for python 2
    - add export method to all nodes return a dict. Might be a json string in the future
    - all outputs now have a port attribute. Midi port for Midi, ip:udp for Udp
    - all events now have a command attribute which hosts the command of the event

- v0.2.2 - Apr. 19 2016
    - Massive Revamp
        - outputs is now attribute of project
        - events is now attributes of scenario
        - command is now atrributes of event (instead of content)
        - remove all useless nodes called 'attributes' in the json export file
    - Revamp Output link to project / scenario / events
    - Revamp events. there is now a event.protocol value(OSC/MidiNote/PJLINK)
    - A scenario is now just a group of events
    - Revamp new_event method. It must be attached to the project and it is now
    - You specify protocol. For lekture, it formats the type of args.

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
