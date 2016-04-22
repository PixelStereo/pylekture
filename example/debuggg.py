#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

from pylekture.project import new_project

from pprint import pprint

p = new_project()
osc = p.new_output('OSC')
export = p.export()
pprint(export)
quit()


s = p.new_scenario()

#pprint(p.export())
#print(p, p.name)
midi = p.new_output('MIDI')
#print(midi)

#print(osc)

#print(s)
e = p.new_event('Osc')

#s.add_event(e)
#s.add_event(e)

#pprint(e.__dict__)


#for key, value in e.__dict__.items():
#	print key, value

#print('COMMAND : ' + str(e.command))





# fill in scenario with events
my_event = p.new_event('Osc', ["/previous", 232, "ramp", 0.5])
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


my_event.output = osc


from pprint import pprint
print('------------------------ EVENTS ------------------------------')
for event in p.events:
	print('------EVENT--------')
	#pprint(event.export())
print('----------------------------- OUTPUTS ------------------------------')
#pprint(osc.export())
print('------------------------------ SCENARIO ------------------------------')
#pprint(s.export())
print('------- EXPORT -------')
print(p.write('/Users/reno/Desktop/'))
print(len(s.events))
print(s.getduration())
print(s.play())
