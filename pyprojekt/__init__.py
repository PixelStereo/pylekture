#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains a project manager for writing inter/multi-media scenario.

===============================================================================
pyprojekt
===============================================================================

First, you create a project. In this project you can add Scenario and Outputs.

A scenario contains an ordered list of Events.

A scenario outputs its event to a choosen Output.

If an output is given for an event, it will overwrite the scenario output for this event.

-------------------------------------------------------------------------------

    Copyright (c) 2015 Pixel Stereo

-------------------------------------------------------------------------------
Changelog:
-------------------------------------------------------------------------------
- v0.1.3  - 3 Jan. 2016
	Revamp projects() and scenarios() method
	Remove a few horribles global variables that existed
	some attributes are now private and must be change only with dedicated methods such as output.getprotocol() 
	Ougetprotocols

- v0.1.2  - 31 Dec. 2015
    New design for Outputs
    various fixes
    
- v0.1.1  - 27 Dec. 2015
    ADD new Class Design. Project / Scenario / Event
    FIX outputs
    
- v0.1  - 25 Dec. 2015
    First draft"""