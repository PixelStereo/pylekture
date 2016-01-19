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
my_output = my_project.new_output('OSC')
my_scenario = my_project.new_scenario()
my_scenario.output = ['OSC' , 1]
first_event = my_scenario.new_event(content=['/previous',232])
second_event = my_scenario.new_event(content=1000)
third_event = my_scenario.new_event(content=['/zob',232])
first_event.play()
#second_event.play()
#third_event.play()

my_scenario.play()

#for event in my_scenario.events():
#	print event.content