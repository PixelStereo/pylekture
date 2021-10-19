#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pybush import new_device
# A device is a bunch of parameters accessible through a protocol/
# For exemple we're creating an OSC device with 2 parameters, an int and a float

my_device = new_device('Test Device')
my_device.new_output(protocol='OSC', port='127.0.0.1:1234')
my_int = my_device.new_parameter('test/numeric/int', datatype='int', default_value=66, domain=[-100, 100], description='an integer')
my_float = my_device.new_parameter('test/numeric/float', datatype='float', default_value=0.123456, domain=[-2.1, 2.2])

from pylekture.project import new_project

my_project = new_project(name= 'My Supa Name')
a_ramp = my_project.new_event('ramp', parameter=my_int, name='event 1', description='my first event', destination=100, duration=2000)
a_random = my_project.new_event('random', parameter=my_int, name='event 2', description='a second event', destination=10, duration=1000)
another_ramp = my_project.new_event('ramp', parameter=my_float, name='event 3', description='my third event', destination=1, duration=2000)
another_random = my_project.new_event('random', parameter=my_float, name='event 4', description='a forth event', destination=1, duration=1000)
print(a_random)
print(a_ramp)

#a_ramp.play()
#a_random.play()
a_scenario = my_project.new_scenario()

a_scenario.add_event(a_ramp)
a_scenario.add_event(another_random)
a_scenario.add_event(a_random)
a_scenario.add_event(another_ramp)
my_project.play()

