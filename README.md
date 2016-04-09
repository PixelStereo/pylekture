# pylekture
=====
#### Python Scenario framework for real-time inter-media projects

**pylekture** can be defined as a framework for real-time intermedia applications.
It is an API for creating and organising Scenario in a Project-based architecture that can be easily accessed through OSC (Open Sound Control) messages.

It uses **pybush** that offers a way to organise your application hierarchicaly.

For the moment, **pylekture** iscapable of:

-  Create projects that contains dynamic scenario and events through Open Sound Control Messages
-  Save projects to json files

#### QuickStart
---
The tests.py file contains a script to understand what you can do with the package.

[Lekture software](http://github.com/PixelStereo/lekture) is a cross-platform application based on pylekture library.

#### Development
---
Development is made on OSX with python 2.7.11    
Continious integration is made on linux for python 2.6, 2.7 and 3.3, 3.4, 3.5

[![Code Climate](https://codeclimate.com/github/PixelStereo/pylekture/badges/gpa.svg)](https://codeclimate.com/github/PixelStereo/pylekture)
[![Coverage Status](https://coveralls.io/repos/github/PixelStereo/pylekture/badge.svg?branch=master)](https://coveralls.io/github/PixelStereo/pylekture?branch=master)
[![Issue Count](https://codeclimate.com/github/PixelStereo/pylekture/badges/issue_count.svg)](https://codeclimate.com/github/PixelStereo/pylekture)
[![Build Status](https://travis-ci.org/PixelStereo/pylekture.svg?branch=master)](https://travis-ci.org/PixelStereo/pylekture)

#### Documentation
---
Documentation is available online [on this page](http://pixelstereo.github.io/pylekture)    

If you need/want to build the documentation from the repo, here are the steps : 

    pip install sphinx
    cd docs/source
    make html

#### Roadmap
---
##### 0.1 - Dec. 2015 -> March. 2016
* ~~Scenario and events sends OSC commands~~
* ~~multiple projects architecture~~
* ~~Python 2 and 3 compatibility~~
* ~~Unit tests and Continious integration~~
* ~~Nice and solid UTF8 Encoding everywhere~~
* ~~project-related commands (auto-play)~~
* ~~Loop for project / scenario / event~~

##### 0.2 - Apr. 2016 -> June. 2016
* Scenario behavior creates nice sequence (aka auto-cue / auto-follow)
* OSC server for projects, scenario and events access
* OSC listening creates Nodes, Models and Parameters
* Namespace implementation for automagic events creation
* Minuit implementation

##### 0.3 - Jul. 2016 -> Dec. 2017
* Graphic display of projects, scenario and events
* Random generator
* Artnet and MIDI in/out
