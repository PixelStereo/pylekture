#! /usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os,sys
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)
from pyprojekt import projekt

debug = True
projekt.debug = True
projekt.test = False

# create a project. Note that when creating a project, an output is created
# this default output is protocol 'OSC' and 127.0.0.1:10000
my_project = projekt.new_project()

# create another output with another protocol
second_out = my_project.new_output(protocol='PJLINK')
second_out.name = 'another output'
second_out.ip = socket.gethostbyname(socket.gethostname())
second_out.udp = 1234
#get a list of all outputs for this project
print  'ALL outputs :' , my_project.outputs()
#get a list of PJLINK outputs for this project
print  'PJLINK outputs :' , my_project.outputs('PJLINK')
#get a list of OSC outputs for this project
print  'OSC outputs :' , my_project.outputs('PJLINK')
print '--------------------------------------------------'
# iterate outputs
out_counter = 0
for output in my_project.outputs():
	out_counter += 1
	print 'output n°'+str(out_counter)+' :' , output.name , '/' , output.protocol , '/' , output.ip + ':' + str(output.udp)
print '--------------------------------------------------'
# create a scenario
my_scenario = my_project.new_scenario()
# create an event
my_event = my_scenario.new_event(content=['/zob',232])
pj_event = my_scenario.new_event(content=['AVMUTE',1])
pj_event.output = ['PJLINK',1]
#play first scenario with default output
my_scenario.play()

my_project.path = '/Users/reno/Desktop/testt.json'
my_project.write()


quit()



another_project = projekt.new_project()

#play first scenario with second output
my_scenario.output = 2
"""THE PROBLEM CAN BE SEEN HERE. THE OUTPUT OF SCENARIO IS NOT IN THE SCENARIO LIST. WHO CREATES AN OUTPUT WHICH IS NOT IN THE INSTANCES LIST ????????"""
print my_project.outputs().index(my_scenario.getoutput())
print 'new output' , my_scenario.output , my_scenario.getoutput() , my_project.outputs()
my_scenario.play()

"""when creating a scenario, its default output is 1, the default output of the project
When creating an event, it doesn't have an output. It use output's scenario. But you can assing an output for an event if you want"""
my_event.output = 1
my_scenario.play()

