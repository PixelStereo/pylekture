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
TODO
-------------------------------------------------------------------------------

- Revamp new_event method. It must be attached to the project
    - You specify protocol. For lekture, it formats the type of args.
    - Code Review of export. It must do ref to the index of the event/scenario. Event has a name, a description, an output.
- A scenario is now just a group of events
Lekture will represent 


In this kind of representation, we must compute the scenario to display the view we want : 
no selection, display the whole project/story
one selection, display the scenario with events for this output highlighted
multiple selection, compute the whole data

We need a visualisation with curves for each events/outputs
We need to adapt the lenght to display to what we display
pylekture must provided the computation. You can save a computation as a scenario. It is a kind of encapsulate.
---------------------------------------------------------
        |   scenario 1  |   scenario 2  |   scenario 3  |
---------------------------------------------------------
out 1   |               |               |               |
---------------------------------------------------------
out 2   |               |               |               |
---------------------------------------------------------
out 3   |               |               |               |
---------------------------------------------------------
out 4   |               |               |               |
---------------------------------------------------------

-------------------------------------------------------------------------------
OVERVIEW
-------------------------------------------------------------------------------
A project/story has a few attributes and contains scenarios and plugins
A plugin is devided into an Event Subclass, an Input and an Output Subclass
In pylekture, we import plugins module, and it will import each plugin.

Events might be index as root. Like this, we could refer in differents scenario the same event.
When saving an events, we save a reference to the events list : 
events as a protocol tyep (automatically detect when created), it is the class of the event
scenario[events] => [OSC_1, WAIT_1000, SCENARIO_2, MIDICC_1, OSC_2, OSC_1]
project[scenarios] => [SCENARIO_1, SCENARIO_2]

events['OSC'] => ['/toto', 1, 'ramp', 5000]
events['MIDICC'] => [1, 12, 127, 'ramp' 5000, 'from', 0]
events['MIDICC'] => [1, 12, 127, 'ramp' 5000] (from latest value (will ask for))
events['MIDICC'] => [1, 12, 'random', 10, 64, 'ramp', 1000]  (will generate a random value each second between 10 and 64)
events['MIDICC'] => [1, 12, 'random', 10, 64, 'ramp', 'random', 500, 2000] (will generate a randome value between 10 and 64 each 500/2000 milliseconds)

We should implement several class of Events
These class might be automatically detected and new_event method will create the appropriate class
- SCENARIO / EVENT
    - How to describe that we want to play an event or a scenaio which already exists?
    - PLAY
- OSC
    - if we have a / as first character
- WAIT
    - if we have a single float/integer (float is in seconds and integer in milliseconds)
- MIDI
    - if we have 3 numbers in a row (Channel btw 0/15, Controler btw 0/127 and Value btw 0/127)
    - we might create a sub-class for MidiNote, MidiCC, etc…
- PJLINK
    - if we have a command without ???
- UDP
    - send a raw UDP command
- OLA
    - a DMX command to be executed in python -> OLA

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
