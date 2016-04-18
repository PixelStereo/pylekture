#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project
from pylekture.functions import prop_dict

p = new_project()
print(p, p.name)
midi = p.new_output('MIDI')
print(midi)
osc = p.new_output('OSC')
print(osc)
s = p.new_scenario()
print(s)
e = p.new_event('OSC')
s.add_event(e)
s.add_event(e)



# fill in scenario with events
my_event = p.new_event('OSC', address="/previous", arguments=[232, "ramp", 500])
s.add_event(my_event)
my_second_event = p.new_event('WAIT', duration=200)
s.add_event(my_second_event)

my_third_event = p.new_event('OSC', address="/zob", arguments=[232, "list", "uno", 2])
my_forth_event = p.new_event('WAIT', duration=200)
my_fifth_event = p.new_event('OSC', address="/address_only")
s.add_event(my_forth_event)
s.add_event(my_third_event)
other_event = p.new_event('MidiNote', channel=16, note=64, velocity=100)
s.add_event(other_event)
s.add_event(other_event)


from pprint import pprint
print('------- SCENARIO -------')
pprint(p._export_scenario())
print('------- EVENTS -------')
pprint(p.export_events())
print('------- OUTPUTS -------')
pprint(p._export_outputs())
print('------- EXPORT -------')
print(p.write('/Users/reno/Desktop/'))
#print(s.play())