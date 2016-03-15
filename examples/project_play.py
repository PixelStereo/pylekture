#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os,sys
from time import sleep
# for running locally
lib_path = os.path.abspath('./../')
sys.path.append(lib_path)

# for Travis CI
lib_path = os.path.abspath('./../pydular')
sys.path.append(lib_path)


from pydular import project
from pydular.project import new_project, projects
from pydular.functions import timestamp, checkType
import datetime

project.debug = 2

import liblo
import time

"""create a project"""
my_project = new_project()
my_project.author = 'Renaud Rubiano'
my_project.version = version='0.1.0'
# create another project
my_other_project =  new_project()

"""create a scenario"""
my_scenario = my_project.new_scenario()
my_other_scenario = my_project.new_scenario()
my_scenario.name = 'the scenario test'
my_other_scenario.name = 'the other scenario'

"""create an output"""
my_output = my_project.new_output('OSC')

my_scenario.output = ['OSC',1]
my_other_scenario.output = ['OSC',1]

my_scenario.post_wait = 1
my_other_scenario.post_wait = 1
"""fill in scenario with events"""
first_event = my_scenario.new_event(content=['/previous', 232, 'ramp', 10])
second_event = my_scenario.new_event(content=2000)
third_event = my_scenario.new_event(content=['/zob', 232, 'list'])
midi_event = my_other_scenario.new_event(content=['/lolo', 232, 'list'])

print my_project.scenarios()
my_project.write("/path/that/does/not/exist")
my_project.play()
#my_scenario.play()
