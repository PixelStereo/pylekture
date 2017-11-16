# pylekture
[![Codacy Badge](https://api.codacy.com/project/badge/coverage/e0076e979dc64ed3b11d5389a0ddd946)](https://www.codacy.com/app/contact_37/pylekture)
[![Build Status](https://travis-ci.org/PixelStereo/pylekture.svg?branch=master)](https://travis-ci.org/PixelStereo/pylekture)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/e0076e979dc64ed3b11d5389a0ddd946)](https://www.codacy.com/app/contact_37/pylekture)

=====
#### Python Scenario framework for real-time inter-media projects

[![PyPI version](https://badge.fury.io/py/pylekture.svg)](https://badge.fury.io/py/pylekture)

**pylekture** can be defined as a framework for real-time intermedia applications.
It is an API for creating and organising Scenario in a Project-based architecture that can be easily accessed through OSC (Open Sound Control) messages.

For the moment, **pylekture** is capable of:

-  Create projects that contains dynamic scenario and events through Open Sound Control Messages
-  Save projects to json files

#### QuickStart
---
##### Install
Here is the way to install the master branch.

    pip install https://github.com/PixelStereo/pylekture/zipball/master    

The tests.py file contains a script to understand what you can do with the package.

[Lekture software](http://github.com/PixelStereo/lekture) is a cross-platform application based on pylekture library.

#### Development
---
Development is made on OSX with python 2.7.11    
Continious integration is made on linux for python 2.7 and 3.3, 3.4, 3.5

#### Documentation
---
Documentation is available online [on this page](http://pixelstereo.github.io/pylekture)    

If you need/want to build the documentation from the repo, here are the steps : 

    pip install sphinx
    cd docs/source
    make html

#### Roadmap
---
##### 0.1 - Late 2016
* ~~Scenario and events sends OSC commands~~
* ~~multiple projects architecture~~
* ~~Python 2 and 3 compatibility~~
* ~~Unit tests and Continious integration~~
* ~~Nice and solid UTF8 Encoding everywhere~~
* ~~project-related commands (auto-play)~~
* ~~Loop for project / scenario / event~~
* Scenario behavior creates nice sequence (aka auto-cue / auto-follow)

##### roadmap
* OSC server for projects, scenario and events access
* OSC listening creates Nodes, Models and Parameters
* Namespace implementation for automagic events creation
* Minuit implementation
* Keyboard customizable shortcuts
* Random generator
* Artnet and MIDI in/out
* PJLink / TCP / Serial support
* Graphic display of projects, scenario and events
