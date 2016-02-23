#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os,sys
from time import sleep
# for 
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

st = liblo.ServerThread(1235)
if project.debug :
    print("Created Server Thread on Port", st.port)


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
my_scenario.wait = 0.1
my_scenario.post_wait = 0.05

"""create an output"""
my_output = my_project.new_output('OSC')
# Attribute output to scenario
my_scenario.output = ['OSC', 1]
my_other_scenario.output = ['MIDI', 1]
# create another output with another protocol
second_out = my_project.new_output('PJLINK')
second_out.name = 'another output'
second_out.udp = 1234
third_out = my_project.new_output('OSC')
third_out.udp = 22222
forth_out = my_project.new_output('MIDI')

# failed in poython3
#assert(my_output.vars_() ==['ip', 'udp', 'name'])
assert(my_output.getprotocol()=='OSC')
assert(second_out.getprotocol()=='PJLINK')
assert(third_out.getprotocol()=='OSC')
assert(forth_out.getprotocol()=='MIDI')
assert(project.Output.protocols()==['OSC'])
assert(len(project.Output.getinstances(my_project))==4)
assert(my_output.getproject().version=='0.1.0')

assert(my_scenario.getoutput().getprotocol() == 'OSC')
assert(my_scenario.getoutput().ip == '127.0.0.1')
assert(my_scenario.getoutput().udp ==1234)
assert(my_scenario.getoutput().name=='no-name')


"""fill in scenario with events"""
first_event = my_scenario.new_event(content=['/previous', 232, 'ramp', 500])
second_event = my_scenario.new_event(content=200)
third_event = my_scenario.new_event(content=['/zob', 232, 'list', 'uno', 2])
fourth_event = my_scenario.new_event(content='/address_only')
midi_event = my_other_scenario.new_event(content=['CC', 16, 1, 64])

"""test scenario file"""
assert(my_scenario.getduration()==700)
assert(len(my_scenario.events())==4)
my_scenario.play()
sleep(1)
my_scenario.play_from_here(third_event)
sleep(0.5)
my_scenario.play_from_here(2)
my_other_scenario.play(index=1)
sleep(0.01)
my_project.play()
sleep(0.5)
my_scenario.del_event(4)

"""test_timestamp"""
the_timestamp = timestamp()

"""test_checkType"""
a_string = u'popo2'
a_float = u'122.2'
a_list = [u'2.2', u'renaud', u'22']
an_int = u'122'
string_int = '2'
string_float = '2.2'
simple_int = 2
simple_float = 2.2
simple_int = checkType(simple_int)
simple_float = checkType(simple_float)
string_int = checkType(string_int)
string_float = checkType(string_float)
the_none = None
a_float = checkType(a_float)
a_list = checkType(a_list)
an_int = checkType(an_int)
the_none = checkType(the_none)
# test functions file
#assert(type(list(string_dict)[0])==unicode)
#assert(type(string_list[0])==unicode)
#assert(type(a_string)==unicode)
#assert(type(an_int)==int)
#assert(type(a_list)==list)
#assert(type(a_list[0])==unicode)
#assert(type(a_list[0])==unicode)
#assert(type(a_list[1])==unicode)
#assert(type(a_list[2])==unicode)
assert(type(a_float)==float)
assert(type(the_none)==type(None))
assert(type(string_float)==float)
assert(type(string_int)==int)
assert(type(simple_float)==float)
assert(type(simple_int)==int)


assert(len(projects())==2)
assert(my_project.author== "Renaud Rubiano")
assert(my_project.version== "0.1.0")
assert(my_project.getprotocols()==['OSC', 'PJLINK', 'MIDI'])
assert(my_project.scenarios()[0].name=='the scenario test')
my_project.scenarios_set(0, 1)
assert(my_project.scenarios()[0].name=='the other scenario')
my_project.del_scenario(my_scenario)
assert(len(my_project.scenarios())==1)
assert(len(my_project.outputs())==4)
assert(len(my_project.outputs('PJLINK'))==1)
assert(len(my_project.outputs('OSC'))==2)
my_project.path = 'my_file'
my_project.write()
assert(my_project.read('my_file.json')==True)
sleep(0.5)
assert(my_project.read('test_pydular.py')==False)
assert(my_project.read('bogus')==False)
my_project.reset()
assert(my_project.outputs()==[])
assert(my_project.scenarios()==[])
del my_project
