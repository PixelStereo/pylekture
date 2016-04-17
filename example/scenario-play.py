#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

p = new_project()
s = p.new_scenario()
s.name = 'my_scenario'
e = s.new_event('OSC', command=['/polo', 0])
e.name = 'my_event'
e1 = s.new_event('WAIT', command=[1000])
e2 = s.new_event('OSC', command=['/polo', 232, 'ramp', 1000])
e2.name = 'my_event_2'
o = p.new_output('OSC')
# next line should be : s.output = o
s.output = o
p.play()
#s.play()
#e.play()
#e1.play()
#e2.play()

"""
Events might be index as root. Like this, we could refer in differents scenario the same event.
When saving an events, we save a reference to the events list : 
events as a protocol tyep (automatically detect when created), it is the class of the event
scenario[events] => [OSC_1, WAIT_1000, SCENARIO_2, MIDICC_1, OSC_2, OSC_1]
project[scenarios] => [SCENARIO_1, SCENARIO_2]
"""

"""
events['OSC'] => ['/toto', 1, 'ramp', 5000]
events['MIDICC'] => [1, 12, 127, 'ramp' 5000, 'from', 0]
events['MIDICC'] => [1, 12, 127, 'ramp' 5000] (from latest value (will ask for))
events['MIDICC'] => [1, 12, 'random', 10, 64, 'ramp', 1000]  (will generate a random value each second between 10 and 64)
events['MIDICC'] => [1, 12, 'random', 10, 64, 'ramp', 'random', 500, 2000] (will generate a randome value between 10 and 64 each 500/2000 milliseconds)
"""

"""
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
"""