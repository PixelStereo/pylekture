#! /usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
from pyprojekt import project

debug = True
project.debug = True

my_project = project.new_project()
my_project.name = 'pouette'

my_other_project = project.new_project()
my_other_project.name = 'other'
my_other_project.author = 'me and I'
my_other_project.version = '2.2.1'

my_output = my_project.new_output('OSC')
another_output = my_project.new_output('PJLINK')
my_scenario = my_project.new_scenario()
my_scenario.output = ['OSC' , 1]
my_project.name = 'toto-la-roulette'
print ('name' , my_scenario.name)
print ('description' , my_scenario.description)
print ('output' , my_scenario.output)
for event in my_scenario.events():
	print ('event-name' ,event.name)
	print ('event-name' ,event.content)
another_scenario = my_project.new_scenario()
another_scenario.output = ['OSC',1]
print ('Events in Another Scenario :' , len(another_scenario.events()))
first_event = another_scenario.new_event(content=['/previous',232])
second_event = another_scenario.new_event(content=1000)
third_event = another_scenario.new_event(content=['/zob',232])
print ('Events in Another Scenario :' , len(another_scenario.events()))

first_event.play()
first_event.content = ['/current' , 32]
print (first_event.content)
first_event.play()
another_scenario.play()

for proj in project.projects():
	print ('project path :' ,  proj.path)
	print ('project version :' ,  proj.version)
	print ('project author :' , proj.author)
	for scenario in proj.scenarios():
		print ('scenario name :' , scenario.name)
	print ()

if project.projects():
	print ('PLAY ALL EVENTS')
	print ('--------------')
	for scenario in my_project.scenarios():
		print ('play scenario :' , scenario.name)
		scenario.play()
		
if my_project.scenarios():
	print ('PLAY ALL EVENTS')
	print ('--------------')
	for scenario in my_project.scenarios():
		print ('play scenario :' , scenario.name)
		scenario.play()

print ('how many scenario :' , len(my_project.scenarios()) , my_project.scenarios())
#my_project.del_scenario(my_scenario)
print ('how many scenario :' , len(my_project.scenarios()) , my_project.scenarios())

my_project.path = 'test_project.json'
my_project.write()


