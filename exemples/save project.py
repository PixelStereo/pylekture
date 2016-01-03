#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
from pyprojekt import projekt

debug = True
projekt.debug = False

my_project = projekt.new_project()
my_project.name = 'my_first_project'
my_project.author = 'me and I'
my_project.version = '0.0.1'

my_project.new_output('OSC')
my_scenario = my_project.new_scenario()
my_scenario.name = 'first'
my_event = my_scenario.new_event()
my_event.content = [['/pouett/no/yfughk',54678654]]


my_poulscenario = my_project.new_scenario()
my_poulscenario.name = 'second'
toto_event = my_poulscenario.new_event()
toto_event.content = [['zob',22]]


print my_poulscenario
my_project.del_scenario(my_poulscenario)
print my_poulscenario

another_scenario = my_project.new_scenario()
another_scenario.name = 'third'
another_scenario.content = [['/plouf' , 32]]


my_other_project = projekt.new_project()
my_other_scenario = my_other_project.new_scenario()
my_other_scenario.name = 'scenar From other project'

print 'default-protocol is the first one :' , projekt.Output.protocols()[0]
print 

proj = 1
for project in projekt.projects():
	print 'project n°'+str(proj)+':' 
	proj += 1
	scenar = 1
	out = 1
	for output in project.outputs():
		print 'output n°'+str(out)+':' , output.getprotocol()
		out += 1
	for scenario in project.scenarios():
		print 'scenario n°'+str(scenar)+':' , scenario.name
		scenar += 1
		for event in scenario.events():
			print 'event :', event.content

my_project.path = 'test.json'
my_project.write()