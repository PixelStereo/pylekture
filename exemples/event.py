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
my_output.udp = 1234
first_event = my_scenario.new_event(content=['/float',232.232])
second_event = my_scenario.new_event(content=['/int',232])
third_event = my_scenario.new_event(content=['/string','a string'])
forth_event = my_scenario.new_event(content=['/list',[1,2.2,'trois']])

"""NEED TO IMPLEMENT BLOB,DOUBLE,64bit int, colorn Boolean, TileTag and Bundle"""

my_scenario.play()