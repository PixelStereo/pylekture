#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
print (lib_path)
from pydular import project

debug = True
project.debug = True

# create a project. Note it is an empty box when created.
# It only has project.attributes (author / version / path)
my_project = project.new_project()


# create a scenario
my_scenario = my_project.new_scenario()

# create an output
my_output = my_project.new_output('OSC')

# get available protocols for this projects
print ('protocols available for this project :' , my_project.getprotocols())

# Attribute output to scenario
my_scenario.output = ['OSC' , 1]
print (my_scenario.output)

# Get the current output object for my_scenario
print (my_scenario.getoutput())

# create another output with another protocol
second_out = my_project.new_output('PJLINK')
second_out.name = 'another output'
second_out.ip = socket.gethostbyname(socket.gethostname())
second_out.udp = 1234

third_out = my_project.new_output('OSC')
third_out.udp = 22222
#get a list of all outputs for this project
print (len(my_project.outputs()) , 'outputs :' , my_project.outputs())
#get a list of PJLINK outputs for this project
print (len(my_project.outputs('PJLINK')) , 'PJLINK :' , my_project.outputs('PJLINK'))
#get a list of OSC outputs for this project
print  (len(my_project.outputs('OSC')) , 'OSC :' , my_project.outputs('OSC'))
print ('--------------------------------------------------')
# iterate outputs
out_counter = 0
for output in my_project.outputs():
	out_counter += 1
	print ('output n°'+str(out_counter)+' :' , output.name , '/' , output.getprotocol() , '/' , output.ip + ':' + str(output.udp))
print ('--------------------------------------------------')
# create an event
my_event = my_scenario.new_event(content=['/zob',232])
pj_event = my_scenario.new_event(content=['AVMUTE',1])
pj_event.output = ['PJLINK',1]
#play first scenario with default output
my_scenario.play()

another_project = project.new_project()

#play first scenario with second output
my_scenario.output = ['OSC' , 2]
print (my_project.outputs().index(my_scenario.getoutput()))
my_scenario.play()

"""when creating a scenario, its default output is 1, the default output of the project
When creating an event, it doesn't have an output. It use output's scenario. But you can assing an output for an event if you want"""
my_event.output = ['OSC',1]
my_scenario.play()

my_project.path = 'test.json'
my_project.write()