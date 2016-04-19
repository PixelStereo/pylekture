#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project
from pylekture.functions import prop_dict

p = new_project()
#print(p, p.name)
midi = p.new_output('OSC')
#print(midi)
osc = p.new_output('MIDI')
#print(osc)
s = p.new_scenario()
#print(s)
e = p.new_event('Osc')
#s.add_event(e)
#s.add_event(e)



# fill in scenario with events
my_event = p.new_event('Osc', command=["/previous", 232, "ramp", 0.5])
my_second_event = p.new_event('Wait', command=2)
my_third_event = p.new_event('Osc', command=["/zob", 232, "list", "uno", 2.7])
my_forth_event = p.new_event('Wait', command=2)
my_fifth_event = p.new_event('Osc', command="/address_only")
other_event = p.new_event('MidiNote', command=[16, 64, 100])


#s.add_event(other_event)
s.add_event(my_third_event)
s.add_event(my_forth_event)
s.add_event(my_third_event)
s.add_event(my_second_event)
s.add_event(my_third_event)
s.add_event(my_event)
#s.add_event(other_event)



from pprint import pprint
print('------- SCENARIO -------')
pprint(p._export_scenario())
print('------- EVENTS -------')
pprint(p.export_events())
print('------- OUTPUTS -------')
pprint(p._export_outputs())
print('------- EXPORT -------')
print(p.write('/Users/reno/Desktop/'))
print(len(s.events), s.getduration())
print(s.play())